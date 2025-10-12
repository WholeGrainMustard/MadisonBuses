'''
File: getData.py
Purpose: Request and record data from Madison Metro's bus API
Created by: Alton Hipps
Last edited: 03/22/25
'''

import datetime as dt
import requests
from config import Config
import math

def repeaterCheck(APIkey,routeList): # working to handle multiple requests
    #print(APIkey,len(routeList))

    if len(routeList)>10:  
        repeats=math.ceil(len(routeList)/10)
        #print(f'Repeats:{repeats}')

        outList=[]
        start=0
        end=9
        while repeats>0:
            shortList=routeList[start:end]
            #print(shortList)
            response=requestBuses(APIkey,shortList)
            #print(response)
            outList.extend(response)
            #print(len(outList))
            repeats=repeats-1
            start+=9
            end+=9
            #print(repeats,start,end)
    else:
        outList=requestBuses(APIkey,routeList)
    return outList


def requestBuses(APIkey,routeList):
    
    rtStr=''

    for rt in routeList:
        rtStr+=rt+','
    rtStr=rtStr[:-1]

    param={
        'rt':rtStr,
        'key':APIkey,
        'format':'json'
    }
    response = requests.get(url='https://metromap.cityofmadison.com/bustime/api/v3/getvehicles', params=param)

    #print(f'{response}\t{response.url}')

    if response.status_code!=200:
        return f'{response}\t{response.url}'
        
    twoDigits=dt.datetime.now().strftime('%S')

    try:
        respDictList=response.json()['bustime-response']['vehicle']
        for d in respDictList:
            d['tmstmp']=d['tmstmp']+':'+twoDigits
        return respDictList
    except Exception as e:
        return f'ERROR: {e}'

def writeToFile(jsonDict,fileName):
    f = open(fileName,'x')
    f.write(str(jsonDict))
    f.close()
    return True

def createFileName(stem):
    time=dt.datetime.now()
    file=stem+time.strftime("%y%m%d%H%M%S")+'.json'
    return file

def collectData(path,rtList):
    stem=path+'data\\'
    logFile=stem+'log.txt'

    logf = open(logFile,'a')

    try:
        key=Config().API
        fileName=createFileName(stem)
        #print(key,rtList)
        request=repeaterCheck(key,rtList)
        #print(len(request))
        if type(request)==str:
            print('Request Error')
            logf.write(request+'\n')
        writeToFile(request,fileName)
        logf.write(f'{dt.datetime.now().strftime("%m/%d/%y %H:%M:%S")}\tCompleted successfully\n')
        logf.close()
        return True
    except Exception as e:
        logf.write(f'ERROR Occured: {e}\n')
        logf.close()
        return False
    
if __name__=='__main__':
    collectData()
    print('Complete')