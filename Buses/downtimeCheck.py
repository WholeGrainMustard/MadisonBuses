'''
File: downtimeCheck.py
Purpose: Check if it downtime should occur
Created by: Alton Hipps
Last edited: 
'''
import time
import datetime as dt

def checkTime(runNum):
 # account for downtime
    now=dt.datetime.now()
    if 0<now.hour<4:
        time.sleep(3600)
        print(f'Run {runNum}\tBetween 1 and 3\tWaiting 1 hour')
        return False
    elif now.hour==0 and now.minute>30:
        time.sleep(600)
        print(f'Run {runNum}\tBetween 12 and 12:30\tWaiting 10min')
        return False
    elif now.hour==4 and now.minute<30:
        time.sleep(600)
        print(f'Run {runNum}\tBetween 4 and 4:30\tWaiting 10min')
        return False
    else:
        return True