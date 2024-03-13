# This is a demo script to run on the pi to move the platform around and demo how nicely it moves

from time import time, sleep
import math
from PlatformController import PlatformController

# DEFINE VARIABLES
running = True # Program stops when turned to False
programStartTime = time()
behaviourStartTime = time()
behaviourRunTime = 0
lastLoopTime = time()
currentLoopTime = time()
timeSinceLastLoop = 0

setPitch = 0
setRoll = 0
setZ = 0

behaviour = 0


# BEHAVIOUR SETTINGS
# Behaviour 0
behaviour0WaitTime = 5

def goToNextBehaviour():
    # Move to next behaviour and reset some variables
    behaviour += 1
    behaviourStartTime = time()
    behaviourRunTime = 0
    currentLoopTime = behaviourStartTime
    lastLoopTime = behaviourStartTime



if __name__ == "main":
    print("Starting Main Loop")
    p = PlatformController()
    while running == True: 
        # This is the loop that runs every 'frame'

        # SET UP FOR NEW RUN OF LOOP (not each behaviour uses all of these)
        lastLoopTime = currentLoopTime
        currentLoopTime = time()
        timeSinceLastLoop = currentLoopTime - lastLoopTime
        behaviourRunTime += timeSinceLastLoop
        
        # DECIDE HOW IT SHOULD MOVE, GOES THROUGH BEHAVIOURS
        if behaviour == 0:
            # does at z = 0 then higher z position. At each height go flat, then tilt each direction
            print("Starting behaviour 0, test basic angles at 2 different heights")
            setZ = 0
            for i in range(2):
                setPitch = 0
                setR = 0
                p.set_platform_angle(pitch = setPitch, roll = setRoll, z = setZ)
                sleep(behaviour0WaitTime)

                setRoll = 10
                p.set_platform_angle(pitch = setPitch, roll = setRoll, z = setZ)
                sleep(behaviour0WaitTime)
                
                setRoll = 0
                setPitch = 10
                p.set_platform_angle(pitch = setPitch, roll = setRoll, z = setZ)
                sleep(behaviour0WaitTime)
                
                setRoll = -10
                setPitch = 0
                p.set_platform_angle(pitch = setPitch, roll = setRoll, z = setZ)
                sleep(behaviour0WaitTime)
                
                setRoll = 0
                setPitch = -10
                p.set_platform_angle(pitch = setPitch, roll = setRoll, z = setZ)
                sleep(behaviour0WaitTime)
                
                if i == 0:
                    setZ = 50
            
            setRoll = 0
            setPitch = 0
            setZ = 0
            p.set_platform_angle(pitch = setPitch, roll = setRoll, z = setZ)
            sleep(10)
            goToNextBehaviour()
        elif behaviour == 1:
            # Do smooth angle movement at 10 degrees in circle at z = 0, current period is 2pi seconds (about 6seconds pe cycle)
            print("Starting behaviour 1, smooth circle movement")
            setRoll = 10*math.sin(behaviourRunTime)
            setPitch = 10*math.cos(behaviourRunTime)
            setZ = 0

            if behaviourRunTime > 20:
                sleep(5)
                goToNextBehaviour()
        elif behaviour == 2:
            # Do smooth vertical movement at constant flat angle
            print("Starting behaviour 2, smooth vertical movement")
            setRoll = 0
            setPitch = 0
            setZ = 50*math.sin(behaviourRunTime)
            if (currentLoopTime - behaviourStartTime) > 10:
                sleep(5)
                goToNextBehaviour()
        elif behaviour == 3:
            setRoll = 10*math.sin(behaviourRunTime*2*math.pi/3) # period of 3s
            setPitch = 10*math.cos(behaviourRunTime*2*math.pi/3) # period of 3s
            setZ = 50*math.sin(behaviourRunTime*2*math.pi/10) # period of 10s 
            if (currentLoopTime - behaviourStartTime) > 30:
                sleep(5)
                goToNextBehaviour()
        elif behaviour == 4:
            p.cleanup()
            running = False


        # MOVE MOTORS
        p.set_platform_angle(pitch = setPitch, roll = setRoll, z = setZ)

