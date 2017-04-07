from datetime import datetime, timedelta; import numpy, ast, json, requests, urllib2, numpy, sys

class WeatherDataPoint:
    def __init__(self, time, temp, zone):
        self.time=time
        self.temp=temp
        self.zone=zone

class PjmDataPoint:
    def __init__(self, time, load, zone):
        self.time=time
        self.load=load
        self.zone=zone
    def __str__(self):
        return self.zone+' '+str(self.time)+' '+str(self.load)

def getLatLonDict():
    latlon = open('pjmzones.csv').read().replace('\n',' ')
    latlon=ast.literal_eval(latlon)
    return latlon

def getWeatherDataForZone(zone, datetime):
    latlon = getLatLonDict()

    baseUrl='https://api.darksky.net/forecast/'
    apikey='eaf6379ff9461d7506e187909ab14c05/'
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
        wdp = WeatherDataPoint(time, temp, zone)
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
        headerLine = pjm_lines[position].strip()
        zone=headerLine[0:headerLine.find('HOUR')]
        zoneDataList = getPjmDataForZone(zone, pjm_lines[position+4:position+18])
        timeLoadList.extend(zoneDataList)
        #appending datapoints not list
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
            zoneDataList.append(dataPoint)
    return zoneDataList


def getFinalList(timeTempList, timeLoadList):
    matchesfound=0
    latlon = getLatLonDict()
    for loadDataPoint in timeLoadList:
        for tempDataPoint in timeTempList:
            if tempDataPoint.zone is not loadDataPoint.zone:
                continue
            elif (tempDataPoint.time - loadDataPoint.time) < 3600:
                print tempDataPoint.zone, tempDataPoint.time, tempDataPoint.temp, loadDataPoint.load
                matchesfound+=1
    if matchesfound!=len(timeLoadList):
        print 'We didnt match everything'
        #find the darksky data point that matches this one zone and time regions

#timeTempList = getWeatherDataForZone('PEPCO',datetime.now())
timeLoadList = getPjmData(datetime.now())
for t in timeLoadList:
    print t.zone
#getFinalList(timeTempList, timeLoadList)
