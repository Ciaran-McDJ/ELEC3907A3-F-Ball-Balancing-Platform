import numpy as np
from helperFuncs import *
from calculateRotationMatrix import calculateRotationMatrix

# NOTE: for numpy np.matmul(A,B) is matrix multiplication A*B
# NOTE: for numpy A.dot(b) where A is 3x3 and b is 3x1, does matrix-vector multiplication A*b

B = 115.47 # Base size constant (mm)
P = 115.47 # Platform size constant (mm)

a = 100 # Controlled arm length (mm)
b = 150 # Uncotrolled arm (mm)

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
    """ Calculates the 3 servo motor angles to achieve the desired platform position
    
    inputs:
    float pitch (Degrees) Rotation about the y-axis (right hand rule thumb pointing towards neg y :(  )
    float roll (Degrees) Rotation about the x-axis (right hand rule thumb pointing towards pos x)
    float z (mm) Delta height from h0

    returns:
    (psi1, psi2, psi3) (Degrees) The three motor angles {relative to the z-axis}

    NOTE: Does approximations, should be very good up to about 20 degrees with values chosen
    TODO: make it so if position is impossible it throws an exception instead of crashing
    """

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

    magl1sqrd = l1[0]**2 + l1[1]**2 + l1[2]**2
    magl2sqrd = l2[0]**2 + l2[1]**2 + l2[2]**2
    magl3sqrd = l3[0]**2 + l3[1]**2 + l3[2]**2

    magl1 = math.sqrt(magl1sqrd)
    magl2 = math.sqrt(magl2sqrd)
    magl3 = math.sqrt(magl3sqrd)

    # Calculating motor angle
    # beta represents the angle between controlled arm and l vector
    beta1 = math.degrees(math.acos( (-b**2+a**2+magl1sqrd) / (2*a*magl1) ))
    beta2 = math.degrees(math.acos( (-b**2+a**2+magl2sqrd) / (2*a*magl2) ))
    beta3 = math.degrees(math.acos( (-b**2+a**2+magl3sqrd) / (2*a*magl3) ))

    # % alpha represents the angle between the z-axis and the l vector
    # % TODO - can probably make this one more efficient
    alpha1 = math.degrees(math.atan( math.sqrt(l1[0]**2+l1[1]**2) / l1[2] ))
    alpha2 = math.degrees(math.atan( math.sqrt(l2[0]+l2[1]) / l2[2] ))
    alpha3 = math.degrees(math.atan( math.sqrt(l3[0]+l3[1]) / l3[2] ))

    # % psi represents the motor angle, angle between controlled arm and z-axis
    psi1 = alpha1 + beta1
    psi2 = alpha2 + beta2
    psi3 = alpha3 + beta3

    return (psi1, psi2, psi3)


calculateMotorAngle(10, 5, 20)    
