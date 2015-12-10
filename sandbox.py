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

def getLocationData(zipCode):
    ##Get Location info from Google
    baseurl = "http://maps.googleapis.com/maps/api/geocode/json?address=" + str(zipCode)
    response = urllib2.urlopen(baseurl).read()
    data = json.loads(response)
    location_data = data['results'][0]
    lat = location_data['geometry']['location']['lat']
    lng = location_data['geometry']['location']['lng']
    return location_data

app.route('/', zipCode = 11209)
def search(zipCode):
    loc = getLocationData(zipCode)
    ##Collate Results
    search_results = {
        "City Name": loc['formatted_address'],
        "Today's Weather" : "Weather",
        "Low" : 54.13,
        "High" : 65.12,
        "Current Weather" : "Weather",
        "Current Temp" : 75.23
    }
    rgb_values = {
        "mainT" : getHex(search_results["Current Temp"]),
        "highT" : getHex(search_results["High"]),
        "lowT" : getHex(search_results["Low"])
    }

    return render_template()

if __name__ == '__main__':
    app.debug = False
    app.run()


