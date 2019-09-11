# pip install flask
from flask import Flask,render_template

app= Flask(__name__)

@app.route('/plot/')
def plot(): # all the code we did in jupyter notebook to show the chart locally, should now be inside this function.
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN 

    start_time= datetime.datetime(2015,11,2)
    end_time= datetime.datetime(2016,3,10)

    df=data.DataReader(name="GOOG",data_source="yahoo",start=start_time, end=end_time) 

    def incr_decr(cl, op):
        if cl> op:
            value= "Increase"
        elif cl<op:
            value= "Decrease"
        else:
            value= "Equal"
            
        return value
        
    df["Status"]= [incr_decr(cl, op) for cl,op in zip(df.Close, df.Open)]
    df["Middle"]= (df.Open+ df.Close)/2
    df["Height"]= abs(df.Open-df.Close)

    p=figure(x_axis_type="datetime", width=800, height=600, sizing_mode= "stretch_both", title= "Candlestick chart") 
    p.grid.grid_line_alpha= 0.5

    hours_12 = 12*60*60*1000 
    p.segment(df.index, df.High, df.index, df.Low, color= "#4c4d4c" ) # segment has 4 parament, highest x, 

    p.rect(df.index[df.Status== "Increase"], df.Middle[df.Status== "Increase"], hours_12, df.Height[df.Status== "Increase"], fill_color="#33a6cc", line_color="#4fb7e3")

    p.rect(df.index[df.Status== "Decrease"], df.Middle[df.Status== "Decrease"], hours_12, df.Height[df.Status== "Decrease"], fill_color="#e0435b", line_color="#eb3854")

    script1, div1 = components(p)
    cdn_js= CDN.js_files[0]

    return render_template("plot.html", script1=script1, div1=div1, cdn_js=cdn_js )

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)