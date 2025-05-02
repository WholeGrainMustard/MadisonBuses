'''
File: config.py
Purpose: File to access config file
Created by: Alton Hipps
Last edited: 03/22/25
'''
import os

class Config:
    def __init__(self,path=os.getcwd()+'\\config.txt'):
        try:
            f=open(path,'r')
            content=f.read().split('\n')
            #print (content)
            for i in range(len(content)):
                #print(content[i])
                content[i]=content[i].split('=')
            #print(content)
            self.API=content[0][1]
            self.home=content[1][1]
        except Exception as e:
            print(f'Error with config init: {e}')
        