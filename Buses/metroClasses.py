'''
File: metroClasses.py
Purpose: File to denote classes for metro buses, routes, and records.
Created by: Alton Hipps
Last edited: 03/22/25
'''

import os

class Record:
    def __init__(self,vehicleDict):
        self.vid=vehicleDict['vid']
        self.timestamp=vehicleDict['tmstmp']
        self.lat=vehicleDict['lat']
        self.lon=vehicleDict['lon']
        self.heading=vehicleDict['hdg']
        self.route=vehicleDict['rt']
        self.destination=vehicleDict['des']
        self.delay=vehicleDict['dly']
        self.speed=vehicleDict['spd']
        self.load=vehicleDict['psgld']
        self.startTime=vehicleDict['stst']

    def __str__(self):
        return f'{self.timestamp}\t{self.lat}\t{self.lon}\t{self.route}'

    def asString(self):
        return f'{self.timestamp},{self.lat},{self.lon},{self.heading},{self.route},{self.destination},{self.delay},{self.speed},{self.load},{self.startTime}'


class Vehicle:
    vehicle_count=0
    def __init__(self,vehicleDict): # can provide Record or dictionary
        if isinstance(vehicleDict, dict):
            self.id=vehicleDict['vid']
            self.records=[Record(vehicleDict)]
            self.recentRec=self.records[0]
            self.activityCounter=3
            self.recCount=1
        else:
            self.id=vehicleDict.vid
            self.records=[vehicleDict]
            self.recentRec=self.records[0]
            self.activityCounter=3
            self.recCount=1
        
        Vehicle.vehicle_count+=1

    def __str__(self):
        return f'ID: {self.id}\tRecords: {self.recCount}'

    def update(self,vehicleDict):
        listToAdd=self.records
        new_i=len(listToAdd)
        if isinstance(vehicleDict,dict):
            listToAdd.append(Record(vehicleDict))
        else:
            listToAdd.append(vehicleDict)
        self.records=listToAdd
        self.recCount=len(self.records)
        self.recentRec=self.records[new_i]


class Route:
    allRoutes={}
    def __init__(self,vehicleObj):
        self.destinations=[vehicleObj.recentRec.destination]
        self.activeBuses=[vehicleObj]
        self.busesToDump=[]
        self.id=vehicleObj.recentRec.route
        Route.allRoutes[self.id]=self

    def __str__(self):
        return f'Route: {self.id}\tDest: {self.destinations}\tActive: {len(self.activeBuses)}'

    def addVehicle(self,Vehicle):
        busList=self.activeBuses
        busList.append(Vehicle)
        self.activeBuses=busList
        destList=self.destinations
        if Vehicle.recentRec.destination not in destList:
            destList.append(Vehicle.recentRec.destination)

    def getAllRoutes(self):
        return Route.allRoutes
    
    def addVehicleToRoute(self,vehicle):
        routeName=vehicle.recentRec.route
        if routeName in list(Route.allRoutes.keys()):
            retrieved=Route.allRoutes[routeName]
            retrieved.addVehicle(vehicle)
    
    def findVehicle(self,vid):
        index=0
        outVehicle=False
        for vehicle in self.activeBuses:
            if vehicle.id == vid:
                outVehicle=vehicle
                break
            else:
                index+=1
        return (outVehicle,index)

    def dumpInactives(self,fileLoc):
        inactives=self.busesToDump
        for bus in inactives:
            fileList=os.listdir(fileLoc)
            print(fileList)
            routeName=bus.recentRec.route
            print(routeName)
            folder=fileLoc+routeName
            print(folder)
            if routeName not in fileList:
                os.makedirs(folder)
            
if __name__=='__main__':
    exBus={'vid': '2317', 'tmstmp': '20250319 12:57', 'lat': '43.12012065780519', 'lon': '-89.32788530648503', 'hdg': '242', 'pid': 387, 'rt': 'A', 'des': 'JUNCTION', 'pdist': 26787, 'dly': False, 'spd': 26, 'tatripid': '1215058', 'origtatripno': '1215058', 'tablockid': '112A', 'zone': '', 'mode': 1, 'psgld': 'EMPTY', 'srvtmstmp': '20250319 12:57', 'oid': '5822', 'or': False, 'rid': '1651', 'lwid1': 'N/A', 'lwid2': '001651', 'blk': 2402, 'tripid': 759020, 'tripdyn': 0, 'stst': 45780, 'stsd': '2025-03-19', 'hidden': False}

    route=Route(Vehicle(exBus))
    route.dumpInactives('...\\Buses')
    print(route.activeBuses[0].recentRec.asString())
    print(route)