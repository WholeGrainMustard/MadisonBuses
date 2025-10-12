'''
File: combineController.py
Purpose: Script to control the combination of files
Created by: Alton Hipps
Last edited: 03/22/25
'''
import datetime as dt
import time
import combineFiles
from config import Config

def controlCombination(freqM=20):
    try:
        print('Combo Control Running')

        con=Config()
        loc=con.home

        locData=loc+'data'
        locOut=loc+'combined'

        while True:
            ts=dt.datetime.now().strftime('%H:%M:%S')
            print(ts)
            jsons=combineFiles.getJSONs(locData)
            if isinstance(jsons,bool):
                print(f'{ts}\tSkipped')
                time.sleep(60*freqM)
                continue
            d=combineFiles.buildRoutes(jsons)
            combineFiles.routeDictToFile(d,locOut)
            combineFiles.cleanUpJSONs(locData)

            print(f'{ts}\tComplete')
            time.sleep(60*freqM)

    except KeyboardInterrupt:
        print('Closing combineController...')

if __name__=='__main__':
    controlCombination(freqM=30)