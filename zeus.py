from datetime import datetime, timedelta; import numpy, ast, json, requests, urllib2, numpy, sys

class WeatherDataPoint:
    def __init__(self, time, temp):
        self.time=time
        self.temp=temp

class PjmDataPoint:
    def __init__(self, time, load, zone):
        self.time=time
        self.load=load
        self.zone=zone
    def __str__(self):
        return self.zone+' '+str(self.time)+' '+str(self.load)
    

def getWeatherData(zone, datetime):
    latlon = open('pjmzones.csv').read().replace('\n',' ')
    latlon=ast.literal_eval(latlon)

    baseUrl='https://api.darksky.net/forecast/'
    apikey='eaf6379ff9461d7506e187909ab14c05/'
    #make api key a constant at the top of the zeus file
    latitude=0
    longitude=0
    latitude,longitude = latlon[zone]
    datestring = datetime.strftime('%Y-%m-%dT%H:%M:%S')

    baseUrl = baseUrl + apikey + str(latitude)+','+str(longitude)+','+datestring
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
        print time, temp
    return timeTempList
        


def getPjmData(datetime):
    datestring = datetime.strftime('%Y%m%d%H%M%S')
    url='http://web.archive.org/web/'+datestring+'/http://oasis.pjm.com/doc/projload.txt'
    pjm_response = requests.get(url)
    pjm_text = pjm_response.text
    pjm_lines = pjm_text.split('\r\n')
    headerPositionList=[]
    timeLoadList=[]
    for idx, pjm_line in enumerate(pjm_lines):
        if 'HOUR ENDING' in pjm_line:
            headerPositionList.append(idx)
    for position in headerPositionList:
        #extract zone from header line
        headerLine = pjm_lines[position].strip()
        zone=headerLine[0:headerLine.find('HOUR')]
        #get data for this zone
        zoneDataList = getPjmDataForZone(zone, pjm_lines[position+4:position+18])
        timeLoadList.append(zoneDataList)
    return timeLoadList

def getPjmDataForZone(zone, timelines):
    zoneDataList=[]
    for idx in 0, 2, 4, 6, 8, 10, 12:
        datestring = timelines[idx][0:9].strip()
        amList = timelines[idx][12:].split()
        pmList = timelines[idx+1][12:].split()
        dailyList = amList+pmList

        for tidx, loadReading in enumerate(dailyList):
            if tidx<12:    
                timestring = str(tidx+1).zfill(2)
                mer='AM'
            else:
                timestring = str(tidx-11).zfill(2)
                mer='PM'
                
            tempDatetime = datetime.strptime(datestring+' '+timestring+mer, '%m/%d/%y %I%p')
            dataPoint = PjmDataPoint(tempDatetime, loadReading, zone)
            loadList.append(dataPoint)
            print dataPoint
    return zoneDataList

getWeatherData('PEPCO',datetime.now())
