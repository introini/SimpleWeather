'''
Created on Nov 18, 2015

@author: mintroini
'''
from flask import Flask
from flask import render_template,request
import urllib2, urllib, json
import forecastio
import math
import psycopg2
import urlparse


url = urlparse.urlparse("postgres://dhmwzmprkdkskg:iOwZtBFJop3CULXtyJf3CCN0sN@ec2-54-204-35-207.compute-1.amazonaws.com:5432/dak67ocsf369hg")

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
conn.close()
api_key = "d35b97ae1e651cb4ff5e7fd7c608f29f"
app = Flask(__name__)
searchId = 0


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
    baseurl = "https://maps.googleapis.com/maps/api/geocode/json?address=" + str(urllib2.quote(zipCode, safe='/'))
    response = urllib2.urlopen(baseurl).read()
    data = json.loads(response)
    location_data = data['results'][0]
    lat = location_data['geometry']['location']['lat']
    lng = location_data['geometry']['location']['lng']
    return location_data, lat, lng

def getWeatherData(api, loc, id):

      ##Get weather forecast from forecast.io
        forecast = forecastio.load_forecast(api, loc[1], loc[2])
        current = forecast.currently()
        daily = forecast.daily().data[0]

        ##Collate Results
        search_results = {
            "id": id,
            "CityName": loc[0]['formatted_address'],
            "TodaysWeather" : daily.summary,
            "Low" : int(math.ceil(daily.apparentTemperatureMin)),
            "High" : int(math.ceil(daily.apparentTemperatureMax)),
            "CurrentWeather" : current.summary,
            "CurrentTemp" : int(math.ceil(current.temperature)),
            "CurrentTempRGB" : getHex(int(math.ceil(current.temperature))),
            "HighTempRGB" : getHex(int(math.ceil(daily.apparentTemperatureMax))),
            "LowTempRGB" : getHex(int(math.ceil(daily.apparentTemperatureMin)))
        }

        return search_results

@app.route('/')
def simpleweather():
    return render_template('weather.html')

@app.route('/search', methods=['POST','GET'])
def search(api = api_key):
    if request.method == 'POST':
        global searchId
        if searchId == 0:
            searchId = 1
        else:
            searchId += 1
        ##Get Zip from user
        zip = request.form['zip']

        ##Get Location Data
        location = getLocationData(zip)

        ##Get Weather Data
        weather = getWeatherData(api_key, location, searchId)

    return render_template('search.html', results=weather)

if __name__ == '__main__':
    app.debug = True
    app.run()