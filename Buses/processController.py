'''
File: processController.py
Purpose: Control the data aquisition process
Created by: Alton Hipps
Last edited: 08/01/25
'''
import datetime as dt
import time
import getData
import grabWeather
import downtimeCheck
from config import Config


def controlProcess(pauseS=10,downS=300):
    try:
        print('Process Control Running')
        
        con=Config()
        home=con.home
        rts=con.routes

        i=0
        x=5
        while True:
            i+=1
            x+=1

            if downtimeCheck.checkTime(i) == False:
                time.sleep(downS)
                continue

            result=getData.collectData(home,rts)
            if x>5:
                weatherResult=grabWeather.checkWeather(home)
                if weatherResult==True:
                    x=0
                con.logChecker()
            else:
                weatherResult='Not Checked'

            print(f'Run {i}\tBuses: {result}\tWeather: {weatherResult}')
            time.sleep(pauseS)

    except KeyboardInterrupt:
        print('Closing processController...')

if __name__=='__main__':
    controlProcess(pauseS=20)