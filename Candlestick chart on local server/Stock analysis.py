from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN # 'CDN' --> content delivery network, will grab the contents(js,css) to later used in flask. 

start_time= datetime.datetime(2015,11,2)
end_time= datetime.datetime(2016,3,10)

df=data.DataReader(name="GOOG",data_source="yahoo",start=start_time, end=end_time) # AAPL is the stock symbol of apple, other company info can be found online


# df.index

# df.Open 
#df['Open']
# days_increased= df.index[df.Close> df.Open]
# days_decreased= df.index[df.Close< df.Open]


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



p=figure(x_axis_type="datetime", width=800, height=500, sizing_mode= "stretch_both", title= "Candlestick chart") # sizing_mode is used for making it responsive.
p.grid.grid_line_alpha= 0.5

hours_12 = 12*60*60*1000 # converting 12 hours in milliseconds, as 12 h will be the width of the rect and it accepts only ms.

p.segment(df.index, df.High, df.index, df.Low, color= "#4c4d4c" ) 

p.rect(df.index[df.Status== "Increase"], df.Middle[df.Status== "Increase"], hours_12, df.Height[df.Status== "Increase"], fill_color="#33a6cc", line_color="#4fb7e3")

p.rect(df.index[df.Status== "Decrease"], df.Middle[df.Status== "Decrease"], hours_12, df.Height[df.Status== "Decrease"], fill_color="#e0435b", line_color="#eb3854")

# type(components(p))

script1, div1 = components(p)

# script1
# div1

cdn_js= CDN.js_files
cdn_css= CDN.css_files 
# --> css files are no longer required to to grab as js can do the job single handedly.



# cdn_js[0] # for this project, we need the first item off the list that has 3 js files in total

# cdn_css

output_file("Candlestick.html")
show(p)