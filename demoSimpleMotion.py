# This is a demo script to run on the pi to move the platform around and demo how nicely it moves

from time import time, sleep
import math
from PlatformController import PlatformController

print("Starting Test!")
p = PlatformController()

p.set_platform_angle(pitch = 0, roll = 0, z = 0)
sleep(3)
startTime = time()

maxInputRange = 250
maxAngle = 20

while time() < startTime+50:
    
    (xInput, yInput) = getControllerInput()

    roll = (xInput / maxInputRange) *maxAngle
    pitch = (yInput / maxInputRange) *maxAngle

    p.set_platform_angle(pitch = pitch, roll = roll, z = 0)



p.cleanup()