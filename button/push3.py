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





def irasom(i, p):
    myCmd = 'arecord --format=S16_LE --duration=1 --rate=16000 --file-type=wav rec/out_'+i+'_'+p+'.wav'
    os.system(myCmd)



def konvertuojam():
    path, dirs, files = next(os.walk("cmd/"))
    file_count = len(files)

    myCmd='sox rec/out_*.wav cmd/command_'+str(file_count)+'.wav'
    os.system(myCmd)


    myCmd='php  ~/bak1/button/speech/convert.php /home/pi/bak1/button/cmd/'+'command_'+str(file_count)+'.wav'

    output = subprocess.check_output(myCmd, shell=True)
    return output.decode('UTF-8')

def isvalom():
    myCmd='rm rec/out_*.wav';
    os.system(myCmd)



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

except KeyboardInterrupt:
        GPIO.cleanup()

