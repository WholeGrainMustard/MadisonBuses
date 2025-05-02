'''
File: grabWeather.py
Purpose: Grab weather details for the Madison Area from weather.gov
Created by: Alton Hipps
Last edited: 03/22/25
'''

# add logging

import requests
import os
import datetime as dt

def getLogFile(root):
    startPath=root+'weather'
    fileList=os.listdir(startPath)
    #print(fileList)
    logName=startPath+'\\log.txt'


    if 'log.txt' not in fileList: # check if log file exists
        logFile=open(logName,'x')
        logFile.close()

    return logName

def logWrite(logFileName,result):
    file=open(logFileName,'a')
    
    file.write(result+'\n')

    file.close()


def requestWeather():
    h={'Cache-Control': 'no-cache',
       "Pragma": "no-cache",
       "Expires": "0"
       }

    response = requests.get(url='https://forecast.weather.gov/MapClick.php?lat=43.0816&lon=-89.3768&lg=english&&FcstType=json', headers=h)

    #print(f'{response}\t{response.url}')

    responseDict=response.json()['currentobservation']

    if response.status_code!=200:
        return f'{response}\t{response.url}'

    try:
        return responseDict
    except Exception as e:
        return f'ERROR: {e}'
    
def checkForCSV(root):
    startPath=root+'weather\\'
    fileList=os.listdir(startPath)
    #print(fileList)

    currentTime=dt.datetime.now()
    nameString=currentTime.strftime("%y_%m_%d")+'.csv'
    #print(nameString)

    if nameString not in fileList:
        retTup=(False,startPath+nameString)
    else:
        retTup=(True,startPath+nameString)

    #print(retTup)
    return retTup

def checkWeather(stem):
    logfile=getLogFile(stem)
    try:
        weatherResponse=requestWeather()
        check=checkForCSV(stem)
        if check[0]==True:
            csv=open(check[1],'a')
        else:
            csv=open(check[1],'x')
            headers='Date,Temperature,RelativeHumidity,Weather,WindChill\n'
            csv.write(headers)

        prepString=','.join([weatherResponse['Date'],
                            weatherResponse['Temp'],
                            weatherResponse['Relh'],
                            weatherResponse['Weather'],
                            weatherResponse['WindChill']])+'\n'

        #print(prepString)
        csv.write(prepString)
        csv.close()
        message=f'{dt.datetime.now().strftime("%m/%d/%y %H:%M:%S")}\tCompleted successfully'
        outcome=True
    except Exception as e:
        message=f'ERROR: {e}'
        outcome=False

    logWrite(logfile,message)

    return outcome


if __name__=="__main__":
    path='...\\Buses\\'
    checkWeather(path)
    print('Complete')