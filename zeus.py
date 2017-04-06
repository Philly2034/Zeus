from datetime import datetime; import numpy, ast, json, requests

class WeatherDataPoint:
    def __init__(self, time, temp):
        self.time=time
        self.temp=temp
    
def getLatLongForZone(zone):
    latlon = open('pjmzones.csv').read().replace('\n',' ')
    latlon=ast.literal_eval(latlon)
    return latlon[zone]

def getDarkSkyUrl(zone,datetime):
    baseUrl='https://api.darksky.net/forecast/'
    apikey='eaf6379ff9461d7506e187909ab14c05/'
    #make api key a constant at the top of the zeus file
    latitude=0
    longitude=0
    latitude,longitude = getLatLongForZone(zone)
    datestring = datetime.strftime('%Y-%m-%dT%H:%M:%S')
    # Just use datetime as parameter
    return baseUrl + apikey + str(latitude)+','+str(longitude)+','+datestring

def getWeatherData(baseUrl):
    '''Returns a list of time temperature tuples'''
    weatherDataRequest = requests.get(baseUrl)
    weatherJson = weatherDataRequest.json()
    hourlyDataList = weatherJson["hourly"]["data"]
    timeTempList = []
    for hourlyData in hourlyDataList:
        time = hourlyData["time"]
        temp = hourlyData["temperature"]
        wdp = WeatherDataPoint(time, temp)
        timeTempList.append(wdp)
    return timeTempList
        

def getPjmUrl(datetime):
    datestring = datetime.strftime('%Y%m%d%H%M%S')
    url='http://web.archive.org/web/'+datestring+'/http://oasis.pjm.com/doc/projload.txt'
    return url


datalist=getWeatherData(getDarkSkyUrl('PECO', datetime.now()))
for l in datalist:
    print(str(l.time) +' ' + str(l.temp))
