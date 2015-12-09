import urllib2, urllib, json
baseurl = "http://api.openweathermap.org/data/2.5/weather?zip=33323&units=imperial&APPID=45dd9de404ef246619a921a6bc566818"
result = urllib2.urlopen(baseurl).read()
data = json.loads(result)
jsonPrint = json.dumps(data, sort_keys=True, indent=4)

search_results = {
                "City Name": data['name'],
                "Weather" : str(data['weather'][0]['description']).title(),
                "Low" : data['main']['temp_min'],
                "High" : data['main']['temp_max'],
                "Current Temp" : data['main']['temp']
                }
print (jsonPrint)