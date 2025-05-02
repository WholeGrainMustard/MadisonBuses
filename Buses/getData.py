'''
File: getData.py
Purpose: Request and record data from Madison Metro's bus API
Created by: Alton Hipps
Last edited: 03/22/25
'''

import datetime as dt
import requests
from config import Config


def requestBuses(APIkey):
    param={
        'rt':'A,B,C,D,F,R,28,38,80,84',
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



def collectData(path):
    stem=path+'data\\'
    logFile=stem+'log.txt'

    logf = open(logFile,'a')
    try:
        key=Config().API
        fileName=createFileName(stem)
        request=requestBuses(key)
        if type(request)==str:
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