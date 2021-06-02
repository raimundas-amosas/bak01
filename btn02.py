import RPi.GPIO as GPIO
import time
from datetime import datetime

import os
from random import Random
import subprocess
import RPi.GPIO as GPIO
import json
import subprocess



LED1 = 24
LED2 = 18
LED3 = 25
BTN = 23
DELAY = 0.2



def stop_sound():
    myCmd = "./aplay.sh"
    os.system(myCmd)


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
            stop_sound()
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

                cmd="php proc.php '"+res["transcript"]+"' "+res["alias"]+" '"+f1+"'";

                ret2 = subprocess.check_output(cmd, shell=True);
                proc_output=[]
                proc_output=json.loads(ret2.decode('utf-8'))
               
                print(proc_output)
                if proc_output["cnt"] > 0:
           
                    cmd="php history.php '"+res["transcript"]+"' "+res["alias"]+" '"+proc_output["row"]["alias"]+"'";
                    os.system(cmd)
                else:
                    cmd="php history.php '"+res["transcript"]+"' "+res["alias"]+" ''";
                    os.system(cmd)


                GPIO.output(LED3,GPIO.HIGH)

                if not proc_output["unknown"]:
                    print(proc_output["row"]["text"])
                    if proc_output["cmd"] == "convert":
                        print("KONVERTUOJU")
                        cmd='python3 convert_02.py Ona "'+proc_output["row"]["text"]+'" '+proc_output["rec_file"]
                        os.system(cmd)

                        cmd="aplay "+'tts/komanda-' + proc_output["rec_file"] + '.wav &'
                        os.system(cmd)

                        cmd="php update.php '"+proc_output["rec_file"]+"' "+proc_output["row"]["id"]+" "+proc_output["act"];
                        os.system(cmd)
                    else:
                        print("SKAITOME")
                        cmd="aplay "+'tts/komanda-' + proc_output["rec_file"] + '.wav &'
                        os.system(cmd)
                else:
                    cmd="aplay "+'tts/komanda-cmd_4.wav &'
                    os.system(cmd)
                

                



                

                GPIO.output(LED3,GPIO.LOW)
            except ValueError as e:
                GPIO.output(LED2,GPIO.LOW)
                print (e)
    
    

            
            #    isvalom()
            i += 1
        p = 0
    time.sleep(DELAY)

        
        
GPIO.cleanup() # Clean up
