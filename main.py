# This is the main control loop that should be run on the pi to balance the ball

# Import Things
# TODO import camera function and platform motion function
from time import time
from PlatformController import PlatformController



# DEFINE CONSTANTS
desiredPosX = 100 #Units? TODO what should be for center?
desiredPosY = 100
# PID Control Loop Parameters
kPX = 1
kPY = 1
kDX = 0
kDY = 0
kIX = 0
kIY = 0

# DEFINE VARIABLES
running = True # Program stops when turned to False
lastLoopTime = time()
currentLoopTime = time()
timeSinceLastLoop = 0
newXPos = None # Position for current run of loop
newYPos = None
lastXPos = None # Position from last run of loop
lastYPos = None
propXErr = 0 # Proportional Error only based on current position
propYErr = 0
lastPropXErr = 0 # Proportional Error from last run of loop for calculating derivative term
lastPropYErr = 0
derXErr = 0 # Derivative Error based on how fast error is changing
derYErr = 0
intXErr = 0 # Integral Error based on cumulative total of error # TODO - am I implementing this correctly?
intYErr = 0
correctionX = 0
correctionY = 0

if __name__ == "main":
    p = PlatformController()
    print("Starting Main Loop")
    while running == True: 
        # This is the loop that runs every 'frame'

        # SET UP FOR NEW RUN OF LOOP
        lastLoopTime = currentLoopTime
        currentLoopTime = time()
        timeSinceLastLoop = currentLoopTime - lastLoopTime
        lastXPos = newXPos
        lastYPos = newYPos
        lastPropXErr = propXErr
        lastPropYErr = propYErr


        
        # GET CAMERA DATA
        newXPos, newYPos = getCameraData()
        if newXPos == None:
            # This means the camera did not manage to identify the ball position this frame
            # Assume ball moving at constant velocity from last frame
            # TODO - deal with case where it returns None (didn't detect ball), also if ball goess off maybe if doesn't detect for some amount of time just stop
            newXPos = lastXPos
            newYPos = lastYPos



        # COMPUTE ERROR AND HOW PLATFORM MUST MOVE
        propXErr = newXPos - desiredPosX # Positive means newXPos is too positive
        propYErr = newYPos - desiredPosY

        derXErr = (propXErr - lastPropXErr)/timeSinceLastLoop # Positive means propXErr increasing
        derYErr = (propYErr - lastPropYErr)/timeSinceLastLoop

        intXErr += propXErr * timeSinceLastLoop # Positive means propXErr is staying too positive
        intYErr += propYErr * timeSinceLastLoop

        correctionX = (propXErr * kPX) + (derXErr * kDX) + (intXErr * kIX)
        correctionY = (propYErr * kPY) + (derYErr * kDY) + (intYErr * kIY)
        


        # MOVE MOTORS
        # Note - right now pitch and roll proportional to correction, from small angle approximation angle should be roughly proportional to force which should be proportional to correction
        p.set_platform_angle(pitch = correctionX, roll = correctionY, z = 0)



