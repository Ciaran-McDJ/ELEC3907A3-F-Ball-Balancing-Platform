import numpy as np
from helperFuncs import *
from calculateRotationMatrix import calculateRotationMatrix

# NOTE: for numpy np.matmul(A,B) is matrix multiplication A*B
# NOTE: for numpy A.dot(b) where A is 3x3 and b is 3x1, does matrix-vector multiplication A*b

B = 100 # Base size constant (mm)
P = 150 # Platform size constant (mm)

a = 1 # Controlled arm length (mm)
b = 1 # Uncotrolled arm (mm)

h_0 = 100 # Default platform height


# Calculations that only need to be done once

# Platform Vectors (platform basis)
p1 = P * np.array([cosd(0), sind(0), 0])
p2 = P * np.array([cosd(120), sind(120), 0])
p3 = P * np.array([cosd(240), sind(240), 0])

# Base Vectors (base basis)
B1 = (B * np.array([cosd(0), sind(0), 0]))
B2 = (B * np.array([cosd(120), sind(120), 0]))
B3 = (B * np.array([cosd(240), sind(240), 0]))

def calculateMotorAngle(pitch:float, roll:float, z:float) -> tuple[float,float,float]:
    """TODO add comment"""

    T = np.array([0, 0, h_0]) + np.array([0, 0, z])

    # Rotation matrix calculation to determine platform vectors
    R = calculateRotationMatrix(pitch,roll)
    P1 = (T + R.dot(p1))
    P2 = (T + R.dot(p2))
    P3 = (T + R.dot(p3))

    # Calculating l vectors (vector from bottom of motor arm to platform)
    l1 = (T + R.dot(p1) - B1)
    l2 = (T + R.dot(p2) - B2)
    l3 = (T + R.dot(p3) - B3)

    

    #TODO - do rest of calcs
    rho1 = 60
    rho2 = 60
    rho3 = 60

    return (rho1, rho2, rho3)


    
