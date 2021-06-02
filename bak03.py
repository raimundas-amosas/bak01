#!/usr/bin/python
#--------------------------------------   
import spidev
import time
import os
from random import Random
import subprocess
import RPi.GPIO as GPIO
import json

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LED = 24
GPIO.setup(LED,GPIO.OUT)

GPIO.output(LED,GPIO.LOW)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000




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





# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data


def TriggerPos(vrx_pos, vry_pos, swt_val):
    ret="";
    if vry_pos<400:
        ret="right"
    if vry_pos>600:
        ret="left"

    if vrx_pos<400:
        ret+="top"
    if vrx_pos>600:
        ret+="bottom"

    if(swt_val<100):
        ret="click"

    if len(ret)==0:
        ret="center"
    return ret

# Define sensor channels
# (channels 3 to 7 unused)
swt_channel = 0
vrx_channel = 1
vry_channel = 2

# Define delay between readings (s)
delay = 0.2




i=0
p=0

while True:

    # Read the joystick position data
    vrx_pos = ReadChannel(vrx_channel)
    vry_pos = ReadChannel(vry_channel)

    # Read switch state
    swt_val = ReadChannel(swt_channel)

    # Print out results
    print ("--------------------------------------------"  )
    print("X : {}  Y : {}  Switch : {}".format(vrx_pos,vry_pos,swt_val))
    pos=TriggerPos(vrx_pos,vry_pos,swt_val)
    if pos != 'center' and pos != 'click':
    #    os.system("espeak -a 200 -v en+f20 "+pos+" --stdout | aplay")
        print(pos)
    else:
        if pos == 'click':
             if p == 0:
                filename="rec/recording_"+str(i)+"_"+str(p)+".wav"
                GPIO.output(LED,GPIO.HIGH)
                irasome(filename)
             p += 1
        else:
            if p > 0:
                stabdome()
                print("Pradedame konvertavima....")
                ret=konvertuojam(filename)
                GPIO.output(LED,GPIO.LOW)
                res = json.loads(ret)
                cmd='python3 convert_02.py Ona "'+res["transcript"]+'"'
                os.system(cmd)
                print(res["transcript"])
                print("Konvertavimas baigtas")

            #    isvalom()
                i += 1
            p = 0

    time.sleep(delay)

        







'''
i=0
p=0
try:
    while True:
        input_state = GPIO.input(18)
        if input_state == False:
            print('Button Pressed')
            irasom(str(i), str(p))
        #    time.sleep(1)
            p += 1

        if p>0 and input_state == True:
            print("Pradedame konvertavima....")
            cmd=konvertuojam()
            print(cmd)
            print("Konvertavimas baigtas")
            isvalom()
            i += 1



        if input_state ==True:
            p=0
            time.sleep(0.3)
'''





