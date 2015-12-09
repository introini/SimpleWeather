'''
Created on Nov 18, 2015

@author: mintroini
'''

from flask import Flask
from flask import render_template,request
import urllib2, urllib, json
import math


app = Flask(__name__)

def getHex(mainTemp):
    if str(mainTemp)[1] == 3:
        mainTemp = int(round(mainTemp,-1) / 5) *5
    elif str(mainTemp)[1] == 8:
        mainTemp = int(round(mainTemp,-1) / 5) *5
    else:
        mainTemp = int(round(mainTemp,1) / 5) *5
    colors = {-5:'75,51,145',0:'55,62,155',5:'37,87,176',10:'22,119,200',15:'10,149,218',20:'1,167,223',25:'0,169,211',30:'0,169,187',35:'0,165,155',40:'0,159,123',45:'0,158,96',50:'14,162,78',55:'58,180,67',60:'114,204,60',65:'173,226,55',70:'223,233,50',75:'253,229,43',80:'255,198,35',85:'255,150,25',90:'255,94,16',95:'255,43,8',100:'255,10,3'}
    for i,v in colors.iteritems():
        r = str(colors[i]).split(',')[0]
        g = str(colors[i]).split(',')[1]
        b = str(colors[i]).split(',')[2]
    return colors[mainTemp]

@app.route('/')
def simpleweather():
    return render_template('weather.html')

@app.route('/search', methods=['POST','GET'])
def search():
    if request.method == 'POST':
        zip = request.form['zip']
        baseurl = "http://api.openweathermap.org/data/2.5/weather?zip=" + zip + "&units=imperial&APPID=45dd9de404ef246619a921a6bc566818"
        result = urllib2.urlopen(baseurl).read()
        data = json.loads(result)

        #Get State by ZIP
        # >>>> http://maps.googleapis.com/maps/api/geocode/json?address=33325&sensor=true

        search_results = {
                "City Name": data['name'],
                "Weather" : str(data['weather'][0]['description']).title(),
                "Low" : data['main']['temp_min'],
                "High" : data['main']['temp_max'],
                "Current Temp" : data['main']['temp']
        }
        rgb_values = {
            "mainT" : getHex(search_results["Current Temp"]),
            "highT" : getHex(search_results["High"]),
            "lowT" : getHex(search_results["Low"])
        }
    return render_template('search.html', rgb=rgb_values, results=search_results)
if __name__ == '__main__':
    app.debug = False
    app.run()