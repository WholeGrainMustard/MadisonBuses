'''
File: processController.py
Purpose: Control the data aquisition process
Created by: Alton Hipps
Last edited: 03/22/25
'''
import datetime as dt
import time
import getData
import grabWeather
import downtimeCheck
from config import Config

con=Config()
home=con.home

i=0
x=5
while True:
    i+=1
    x+=1

    if downtimeCheck.checkTime(i) == False:
        time.sleep(300)
        continue

    result=getData.collectData(home)

    if x>5:
        weatherResult=grabWeather.checkWeather(home)
        if weatherResult==True:
            x=0
    else:
        weatherResult='Not Checked'

    print(f'Run {i}\tBuses: {result}\tWeather: {weatherResult}')
    time.sleep(10)
