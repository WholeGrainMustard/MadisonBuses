'''
File: combineFiles.py
Purpose: Script to combine JSON files into a running csv.
Created by: Alton Hipps
Last edited: 08/01/25
'''

import os
import metroClasses
import datetime as dt
import pandas as pd

def checkCount(fileList):
    if len(fileList)>1:
        return True
    else:
        return False

def getJSONs(stem):
    tempList=[]

    fileList=os.listdir(stem)
    #print(fileList)
    if checkCount(fileList)==False:
        #print(checkCount(fileList))
        return False
    for file in fileList:
        fullPath=stem+'\\'+file
        jsonFile=open(fullPath,'r')
        onlyLine=jsonFile.readline()
        onlyLine=onlyLine.replace('"','')
        onlyLine=onlyLine.replace("'","")
        jsonFileAsList=onlyLine.split('{')
        objList=[]
        for piece in jsonFileAsList:
            vechicleList=piece.split(',')
            vehicleDictBuild={}
            if len(vechicleList)==1:
                continue
            for item in vechicleList:
                propPair=item.split(':')
                for i in range(len(propPair)):
                    propPair[i]=propPair[i].strip()
                length=len(propPair)
                if length==4: # handle timestamps
                    propPair[1]=propPair[1]+' '+propPair[2]+' '+propPair[3]
                    propPair.pop(2)
                    propPair.pop(2)
                    length=len(propPair)
                if length==2:
                    #print(propPair)
                    vehicleDictBuild[propPair[0]]=propPair[1]
            #print(vehicleDictBuild)
            try: #Error handling for bad JSON files
                if vehicleDictBuild['lat'] == '0.0' and vehicleDictBuild['lon'] == '0.0':
                    #print(f'No Data found: {vehicleDictBuild}')
                    continue
            except Exception as e:
                print(f'Error with {file}: {e}')
                continue
            #print(vehicleDictBuild)
            newVehicle=metroClasses.Record(vehicleDictBuild)
            objList.append(newVehicle)
        if len(objList)>1:
            tempList.append(objList[:])
    return tempList

def buildRoutes(recList):
    outDict={}
    for recordFile in recList:
        for record in recordFile:
            recRoute=(record.route)
            if recRoute not in list(outDict.keys()):
                outDict[recRoute]=metroClasses.Route(metroClasses.Vehicle(record))
                #print(outDict[recRoute])
            else:
                routeObj=outDict[recRoute]
                vehicleSearch=(routeObj.findVehicle(record.vid))
                if vehicleSearch[0] == False: #route Exists but vehicle not added
                    routeObj.addVehicle(metroClasses.Vehicle(record))
                else: #route and vehicle exist
                    vehicleSearch[0].update(record)
    return outDict

def manageFolder(folderName,folderLoc):
    dirList=os.listdir(folderLoc)
    if folderName not in dirList:
        os.mkdir(folderLoc+'\\'+folderName)
        return folderLoc+'\\'+folderName
    return folderLoc+'\\'+folderName

def manageCSV(location):
    dirList=os.listdir(location)
    ts=dt.datetime.now().strftime('%y_%m_%d')
    csvName=ts+'.csv'
    if csvName not in dirList:
        csv=open(location+'\\'+csvName,'x')
        csv.close()
    return location+'\\'+csvName

def routeDictToFile(inDict,filePath):
    for routeKey in list(inDict.keys()):
        routeObj=inDict[routeKey]
        busList=routeObj.activeBuses
        #print(routeObj)
        routeFolder=manageFolder(routeObj.id,filePath)
        if len(routeObj.destinations)>0 and routeObj.destinations[0] != '':
            for destintation in routeObj.destinations:
                destFolder=manageFolder(destintation.replace('/','-').replace('.',''),routeFolder)
                for bus in busList:
                    bDest=bus.recentRec.destination.replace('/','-').replace('.','')
                    if bDest == destintation: # find correct file
                        csvName=manageCSV(destFolder)
                        csvF=open(csvName,'a')
                        lastLine=''
                        for record in bus.records:
                            currentLine=record.asString()+'\n'
                            if currentLine!=lastLine:
                                csvF.write(currentLine)
                                lastLine=currentLine[:]
                        csvF.close()
                        # open csv and drop duplicates
                        df=pd.read_csv(csvName,names=['Time', 'Lat', 'Long', 'Heading', 'Route', 'Destination', 'Delay', 'STST', 'Fullness', 'BusID'])
                        #print(df.columns)
                        df.drop_duplicates(inplace=True,ignore_index=True,subset=['Lat', 'Long', 'Heading', 'Route', 'Destination', 'Delay', 'STST', 'Fullness', 'BusID'])
                        df.to_csv(csvName,index=False)
                
def cleanUpJSONs(path):
    counter=0
    fileList=os.listdir(path)
    #print(fileList)
    if checkCount(fileList)==False:
        return False
    for file in fileList:
        if file[-4:]=='json':
            os.remove(path+'\\'+file)
            counter+=1
    return f'Removed {counter} files'

if __name__=="__main__":
    testLoc='C:\\Users\\ahipp\\Desktop\\Buses'

    locData=testLoc+'\\data'
    locOut=testLoc+'\\combined'

    jsons=getJSONs(testLoc+'\\data')
    d=buildRoutes(jsons)
    routeDictToFile(d,testLoc+'\\combined')
    cleanUpJSONs(testLoc+'\\data copy')
    print('Complete')