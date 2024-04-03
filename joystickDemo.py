# Demo to show off joystick control. Balance a ball using the joystick!
# joystick controls pitch and roll, pushing the joystick makes it jump

from time import time, sleep
import math
from platformCode import PlatformController
from joystick import Joystick

MAX_INPUT_RANGE = 250
MAX_ANGLE = 5

p = PlatformController()
j = Joystick()

print("Starting Test!")
p.set_platform_angle(pitch = 0, roll = 0, z = 0)
sleep(1)
startTime = time()

i=0



# TEMP - measuring some time stuff
joystickInputTime = 0
settingMotorTime = 0

tempJoystickTime = 0
tempMotorTime = 0



while time() < startTime+10:
    tempJoystickTime = time()
    val_Z = j.isZPushed()
    (xInput, yInput) = j.getJoystickPosition()
    joystickInputTime += time() - tempJoystickTime
    #print("Click: %d, Y: %d, X: %d" % (val_Z, xInput, yInput))
    
    roll = ((xInput / MAX_INPUT_RANGE)-0.5) *MAX_ANGLE*2
    pitch = -((yInput / MAX_INPUT_RANGE)-0.5) *MAX_ANGLE*2
    
    #print("pitch = ", pitch, "roll = ", roll)
    
    if val_Z:
        height = 0
    else:
        height = 25
    
    tempMotorTime = time()
    p.set_platform_angle(pitch = pitch, roll = roll, z = height)
    settingMotorTime += time() - tempJoystickTime
    #print(time() - startTime)
    i+=1
    print(i)
    

print(i)
print("num loops per second = ", i/10)
print("number of miliseconds per loop = ", 1/(i/10) * 1000)