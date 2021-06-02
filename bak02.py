#!/usr/bin/python
#--------------------------------------   
# This script reads data from a 
# MCP3008 ADC device using the SPI bus.
#
# Analogue joystick version!
#
# Author : Matt Hawkins
# Date   : 25/122017
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

import spidev
import time
import os
from random import Random



# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

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




while True:

  # Read the joystick position data
  vrx_pos = ReadChannel(vrx_channel)
  vry_pos = ReadChannel(vry_channel)

  # Read switch state
  swt_val = ReadChannel(swt_channel)

  # Print out results
  print "--------------------------------------------"  
  print("X : {}  Y : {}  Switch : {}".format(vrx_pos,vry_pos,swt_val))
  pos=TriggerPos(vrx_pos,vry_pos,swt_val)
  if pos != 'center':
    os.system("espeak -a 200 -v en+f20 "+pos+" --stdout | aplay")
  # Wait before repeating loop
  time.sleep(delay)