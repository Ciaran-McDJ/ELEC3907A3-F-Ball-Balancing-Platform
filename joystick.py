

import RPi.GPIO as GPIO
import smbus
import time
from platformCode import PlatformController

address = 0x48
bus = smbus.SMBus(1)
cmd = 0x40

Z_pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(Z_pin, GPIO.IN, GPIO.PUD_UP)

def analogRead (chn):
    bus.write_byte(address, cmd+chn)
    value = bus.read_byte(address)
    return value
def analogWrite(value):
    bus.write_byte_data(address, cmd, value)
    
p = PlatformController()
    
while True:
    val_Z = GPIO.input(Z_pin)
    val_Y = analogRead(0)
    val_X = analogRead(1)
    print("Click: %d, Y: %d, X: %d" % (val_Z, val_Y, val_X))
    
    p.set_platform_angle(0,20*val_Y/130-20, 30)
    