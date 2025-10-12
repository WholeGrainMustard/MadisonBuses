'''
File: mapCreate.py
Purpose: File to hold functions and classes used to create maps.
Created by: Alton Hipps
Last edited: 07/31/25
'''
import geopandas as gpd
import pandas as pd
import os
from datetime import datetime,timedelta
import keplergl
import bs4
import re

from config import Config
import keplerConfig

# Function to make sure each line is readable
def nextReadableLine(fileObj):
    try:
        csvList=fileObj.readline()
        return csvList
    except:
        return (nextReadableLine(fileObj))

# function to create list of full file
def fileToListOfLists(csvPath):
    fileList=[]
    f=open(csvPath)
    while True:
        line=nextReadableLine(f)
        if not line:
            break
        else:
            lineList=line.split(',')
            fileList.append(lineList)
    f.close()
    return fileList

# create class to contain data for each bus destination
class BusRoute:
    count=1
    def __init__(self):
        self.id=BusRoute.count
        #self.df=[]
        BusRoute.count+=1

    # Method to read a csv to a dataframe
    def fromCSV(self,csvPath,headDictionary,mode='new'):
        eCount=1
        longList=fileToListOfLists(csvPath)
        # Package as dataframe
        skip=True
        for listItem in longList:
            skip=False
            if len(listItem)!=10:
                skip=True
                continue
            try:
                headDict=dict(headDictionary)
                headDict['TimeStamp'].append(datetime(
                    int(listItem[0][:4]), # year
                    int(listItem[0][4:6]), # month
                    int(listItem[0][6:8]), # day
                    int(listItem[0].split(' ')[1]), # hour
                    int(listItem[0].split(' ')[2]), # minute
                    int(listItem[0].split(' ')[3]) # second
                ))
                headDict['Lat'].append(listItem[1])
                headDict['Long'].append(listItem[2])
                headDict['Heading'].append(listItem[3])
                headDict['RTDesignation'].append(listItem[4])
                headDict['Destination'].append(listItem[5])
                headDict['DelayStatus'].append(listItem[6])
                headDict['Speed'].append(listItem[7])
                headDict['Fullness'].append(listItem[8])
                headDict['BusID'].append(listItem[9][:-1])
            except Exception as e:
                if(len(listItem[0]))>20:listItem='Too long'
                #print(f'{eCount}\t{listItem}')
                #print(f'\t{e}')
                eCount+=1
                continue
        if skip==True:
            #print('No data ingested')
            return False
        if len(headDict)<1:
            #print('No data ingested')
            return False
        outDf=pd.DataFrame(headDict)
        if mode=='new':
            #print('New!!')
            self.df=pd.DataFrame(headDict)
            return True
        elif mode=='add':
            oldDf=self.df
            oldDf.append(outDf)
            self.df=oldDf
            #print('Add!!')
            return True
        else:
            #print('DF Only')
            return outDf
        
# Class to contain all busRoute objects
class routeContainer:
    count=1
    def __init__(self,inRoutes): # somethign is going on here but filter step solves problem
        self.id=routeContainer.count

        self.rts=[]
        for rt in list(inRoutes.keys()):
            self.rts.append(rt)
        
        self.routeObjs=inRoutes
        routeContainer.count+=1

        self.rtDfDict={}
        tempList=self.rts
        tempList.reverse()
        for rt in tempList:
            workingDict=inRoutes[rt]
            tempDF=pd.DataFrame()
            for dest in list(inRoutes[rt].keys()):
                df=workingDict[dest]
                df=df.loc[df['RTDesignation'] == rt]
                #print(df['RTDesignation'].unique()) #.loc[workingDict[rt]['RTDesignation'] == rt]
                tempDF = pd.concat([tempDF, df], axis=0)
            self.rtDfDict[rt]=tempDF.copy(deep=True)
            self.rtDfDict[rt]=self.rtDfDict[rt].loc[self.rtDfDict[rt]['RTDesignation'] == rt] # filter step
            self.rtDfDict[rt].reset_index(drop=True, inplace=True)
            tempDF = None
            workingDict = None

    def toCSVs(self,destinationFolder=os.getcwd()+r"\csvs"):
        for rt in list(self.rtDfDict.keys()):
            df=self.rtDfDict[rt]
            minValue=df['TimeStamp'].min()
            maxValue=df['TimeStamp'].max()
            minMonth=str(minValue.month)
            minDay=str(minValue.day)
            maxMonth=str(maxValue.month)
            maxDay=str(maxValue.day)
            if len(minMonth)<2:
                minMonth='0'+minMonth
            if len(minDay)<2:
                minDay='0'+minDay
            if len(maxMonth)<2:
                maxMonth='0'+maxMonth
            if len(maxDay)<2:
                maxDay='0'+maxDay
            filePath=f'{destinationFolder}\\{rt}_{str(minValue.year)[2:4]}{minMonth}{minDay}_to_{str(maxValue.year)[2:4]}{maxMonth}{maxDay}.csv'
            df.to_csv(path_or_buf=filePath,index=False,index_label=None)
        print(f'{len(list(self.rtDfDict.keys()))} csvs written')

    def createMaps(self,outputLocation=os.getcwd()+"\\routes"):
        try:
            for rt in list(self.rtDfDict.keys()):
                df=self.rtDfDict[rt]
                dtRange=keplerConfig.createDateRange(df)
                gdf = gpd.GeoDataFrame(df,  # convert the dataframe to geodataframe
                            geometry=gpd.points_from_xy(x=df.Long,
                                                        y=df.Lat))
                gdf=gdf.drop(['Lat','Long','Speed','BusID'],axis=1)
                gdf=gdf.drop_duplicates()
                gdf['TimeStamp']=gdf['TimeStamp'].astype('str')

                map = keplergl.KeplerGl(config=keplerConfig.createConfig(rt,dtRange), show_docs=False)
                map.add_data(data=gdf, name=f'Rt{rt}')
                map.save_to_html(file_name=f'{outputLocation}\\{rt}.html',read_only=True)

                # retitle the webpages
                with open(f'{outputLocation}\\{rt}.html') as inf:
                    txt = inf.read()
                    soup = bs4.BeautifulSoup(txt,features="lxml")
                    soup.head.title.string = re.sub(r'Kepler.gl', f'Route {rt}', soup.head.title.string)

                # save the file again
                with open(f'{outputLocation}\\{rt}.html', "w") as outf:
                    outf.write(str(soup))
            return True

        except Exception as e:
            print(f'Error:{e}')
            return False
    

# Function to search through full folder structure
def folderSearch(dataFolder=os.getcwd()+r"\combined"):
    folderStructure=[]
    # Identity Route Name folders
    bigList=os.listdir(dataFolder)
    #print(bigList)

    for item in bigList:
        routeList=os.listdir(dataFolder+'\\'+item)
        for route in routeList:
            destinationList=os.listdir(dataFolder+'\\'+item+'\\'+route)
            if len(destinationList)!=0:
                for dest in destinationList:
                    folderStructure.append(dataFolder+'\\'+item+'\\'+route+'\\'+dest)
    return (folderStructure,bigList)

# function to gate the time range allowed for access
def timegateFiles(folderStructure,numOfDays=14):
    #create list of acceptable file names
    today=datetime.today()
    month=today.month
    if month<10:
        month='0'+str(month)
    todayFile=f'{str(today.year)[2:4]}_{month}_{today.day}.csv'
    fileList=[todayFile]
    # loop through and create file paths for each day until days reached by substractions
    count=1
    while count < numOfDays:
        newDate=today-timedelta(days=1*count)
        month=newDate.month
        if month<10:
            month='0'+str(month)
        newStr=f'{str(newDate.year)[2:4]}_{month}_{newDate.day}.csv'
        fileList.append(newStr)
        count+=1
    # Compare actual file names to list of acceptable
    cleanedListOfPaths=[]
    for path in folderStructure:
        pathCut=path.split('\\')
        pathCut.reverse()
        pathTail=pathCut[0]
        if pathTail in fileList:
            cleanedListOfPaths.append(path)
        else:
            continue
    return cleanedListOfPaths # must return cleaned list of paths

# function to create BusRoute objs for each route
def createBusRoutes(dataFolder,headers):
    busRoutes={}
    allPaths,routeNames=folderSearch(dataFolder)
    #print(routeNames)

    cleanedPaths=timegateFiles(allPaths) # to Impliment yet

    counter=0
    for path in cleanedPaths:
        spliter=path.split('\\')
        for piece in spliter:
            if piece in routeNames:
                i=spliter.index(piece)
                routeName=spliter[i]
                destination=spliter[i+1]
                fileName=spliter[i+2]
        #print(routeName,destination,fileName)

        # add each bus route
        if routeName not in busRoutes.keys():
            busRoutes[routeName]={}

        busObj=BusRoute()
        message=busObj.fromCSV(path,headers)
        if message==True:
            busRoutes[routeName][destination]=busObj.df

        counter+=1
        ''' for testing
        #print(counter)

        if counter>150:
            break
        '''
    print(f'{counter} files read into memory')
    return busRoutes

if __name__=="__main__":
    print('Creating Maps...')
    headers={
    'TimeStamp':[],
    'Lat':[],
    'Long':[],
    'Heading':[],
    'RTDesignation':[],
    'Destination':[],
    'DelayStatus':[],
    'Speed':[], 
    'Fullness':[],
    'BusID':[]
    }

    con=Config()
    home=con.home
    combinedFolder=f"{home}\\combined"

    allRoutes=routeContainer(createBusRoutes(combinedFolder,headers))
    allRoutes.toCSVs()
    allRoutes.createMaps()
    print('Complete!')