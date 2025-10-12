'''
File: config.py
Purpose: File to access config file
Created by: Alton Hipps
Last edited: 03/22/25
'''
import os
import datetime as dt

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
            self.routes=content[2][1].split(',')
            #print(self.routes)
        except Exception as e:
            print(f'Error with config init: {e}')

    def logChecker(self,max_size=10000000):
        path=self.home+'//data//log.txt'
        size=os.path.getsize(path)

        # For testing
        # size=max_size+1

        if max_size < size:
            try:
                dtStr=dt.datetime.now().strftime('%y_%m_%d')
                #print(dtStr)
                os.rename(path,self.home+'//data//log_'+dtStr+'.txt')
                with open(path,'w') as f:
                    f.write('')
                print('New Log File created')
            except:
                print('Log File Error')
