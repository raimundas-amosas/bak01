import RPi.GPIO as GPIO
import time
from datetime import datetime

import os
from random import Random
import subprocess
import RPi.GPIO as GPIO
import json



LED1 = 24
LED2 = 18
LED3 = 25
BTN = 23
DELAY = 0.2






def irasome(filename):
    myCmd = "./arec.sh "+filename
    os.system(myCmd)


def stabdome():
    myCmd = "./arec.sh"
    os.system(myCmd)



def konvertuojam(filename):
    myCmd='php speech/convert.php '+filename
    output = subprocess.check_output(myCmd, shell=True)
    return output.decode('UTF-8')

def isvalom():
    myCmd='rm rec/out_*.wav';
    os.system(myCmd)

def current_time():
    return datetime.now().strftime('%Y-%m-%d_%H:%M:%S')




GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(LED1,GPIO.OUT)
GPIO.output(LED1,GPIO.LOW)



GPIO.setup(LED2,GPIO.OUT)
GPIO.output(LED2,GPIO.LOW)

GPIO.setup(LED3,GPIO.OUT)
GPIO.output(LED3,GPIO.LOW)



i=0
p=0
while True: # Run forever
    if GPIO.input(BTN) == GPIO.HIGH:
        if p == 0:
            filename="rec/recording_"+str(i)+"_"+str(p)+".wav"
            GPIO.output(LED1,GPIO.HIGH)
            irasome(filename)
        p += 1
        
    else:
        if p > 0:
            stabdome()
            GPIO.output(LED1,GPIO.LOW)
            GPIO.output(LED2,GPIO.HIGH)
            print("Pradedame konvertavima....")
            ret=konvertuojam(filename)
            
            print(ret)
            
            
            
            
            try:
           
                res = json.loads(ret)
    
                f1=current_time()
                cmd='python3 convert_02.py Ona "'+res["transcript"]+'" "'+f1+'"'
                os.system(cmd)
                print(res["transcript"])
                print("Konvertavimas baigtas")
                
                
                GPIO.output(LED2,GPIO.LOW)
         

                #os.system("");
                GPIO.output(LED3,GPIO.HIGH)
                os.system("aplay "+'tts/komanda-' + f1 + '.wav')
                GPIO.output(LED3,GPIO.LOW)
            except ValueError as e:
                GPIO.output(LED2,GPIO.LOW)
                print (e)
    
    

            
            #    isvalom()
            i += 1
        p = 0
    time.sleep(DELAY)

        
        
GPIO.cleanup() # Clean up
