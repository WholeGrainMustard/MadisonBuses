'''
File: mainController.py
Purpose: Control the controller processes
Created by: Alton Hipps
Last edited: 07/16/25
'''
import sys
import threading
import time
import signal
import processController as pc
import combineController as cc

def signal_handler(signal, frame):
    print('\nYou pressed Ctrl+C, keyboardInterrupt detected!')
    sys.exit(0)

try:
    # Create threads
    t1=threading.Thread(target=pc.controlProcess, name='pcThread')
    t2=threading.Thread(target=cc.controlCombination, name='ccThread')

    t1.start()
    t2.start()

except KeyboardInterrupt: # not working right now
    t1.join()
    t2.join()
    print('Closing Process...')
    time.sleep(2)
    #sys.exit()
