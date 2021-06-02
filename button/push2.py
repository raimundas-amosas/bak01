import RPi.GPIO as GPIO
import time
import os
import subprocess
from subprocess import PIPE, Popen

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


def led_(c, led):
    if c=='on':
        print("LED on")
        GPIO.output(led,GPIO.HIGH)
    if c=='off':
        print("LED off")
        GPIO.output(led,GPIO.LOW)




def irasom(i, p):
    myCmd = 'arecord --format=S16_LE --duration=1 --rate=16000 --file-type=wav rec/out_'+i+'_'+p+'.wav'
    os.system(myCmd)



def konvertuojam():
    path, dirs, files = next(os.walk("cmd/"))
    file_count = len(files)

    myCmd='sox rec/out_*.wav cmd/command_'+str(file_count)+'.wav'
    os.system(myCmd)


    myCmd='php  ~/bak1/button/speech/convert.php /home/pi/gpio/button/cmd/'+'command_'+str(file_count)+'.wav'

    output = subprocess.check_output(myCmd, shell=True)
    return output.decode('UTF-8')

def isvalom():
    myCmd='rm rec/out_*.wav';
    os.system(myCmd)


def do_action(cmd):
    if cmd=="ijunk-melyna":
        print ("melyna on")
        led_('on', 14)
    if cmd=="isjunk-melyna":
        print ("melyna off")
        led_('off', 14)

    if cmd=="ijunk-raudona":
        print ("raudona on")
        led_('on', 15)
    if cmd=="isjunk-raudona":
        print ("raudona off")
        led_('off', 15)

    if cmd=="ijunk-balta":
        print ("balta on")
        led_('on', 23)
    if cmd=="isjunk-balta":
        print ("baltas off")
        led_('off', 23)

    if cmd=="ijunk-zalia":
        print ("zalia on")
        led_('on', 24)
    if cmd=="isjunk-zalia":
        print ("zalias off")
        led_('off', 24)

    if cmd=="ijunk-geltona":
        print ("geltonas on")
        led_('on', 25)
    if cmd=="isjunk-geltona":
        print ("geltonas off")
        led_('off', 25)




    if cmd=="ijunk-visus" or cmd=="ijunk-visas":
        print ("visi on")
        led_('on', 14)
        led_('on', 15)
        led_('on', 23)
        led_('on', 24)
        led_('on', 25)
    if cmd=="isjunk-visus" or cmd=="isjunk-visas":
        print ("visi off")
        led_('off', 14)
        led_('off', 15)
        led_('off', 23)
        led_('off', 24)
        led_('off', 25)



    if cmd=="ijunk-geltona":
        print ("geltonas on")
        led_('on', 25)
    if cmd=="isjunk-geltona":
        print ("geltonas off")
        led_('off', 25)




GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(14,GPIO.OUT) # melynas
GPIO.setup(15,GPIO.OUT) # raudonas
GPIO.setup(23,GPIO.OUT) # baltas
GPIO.setup(24,GPIO.OUT) #zalias
GPIO.setup(25,GPIO.OUT) #geltonas


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
            do_action(cmd)
            isvalom()
            i += 1



        if input_state ==True:
            p=0
            time.sleep(0.3)

except KeyboardInterrupt:
        GPIO.cleanup()

