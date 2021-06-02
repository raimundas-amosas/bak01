import RPi.GPIO as GPIO
import time


def led_(c, led):
    if c=='on':
        print("LED on")
        GPIO.output(led,GPIO.HIGH)
    if c=='off':
        print("LED off")
        GPIO.output(led,GPIO.LOW)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)



led_('on', 25)

time.sleep(1)

led_('off', 25)
