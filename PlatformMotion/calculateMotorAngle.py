import numpy as np
from helperFuncs import *
from calculateRotationMatrix import calculateRotationMatrix


B = 100 # Base size constant (mm)
P = 150 # Platform size constant (mm)

a = 1 # Controlled arm length (mm)
b = 1 # Uncotrolled arm (mm)

h_0 = 100 # Default platform height


def calculateMotorAngle(pitch:float, roll:float, z:float)
    """TODO"""

    
    calculateRotationMatrix(pitch,roll)

    p1 = P * [cosd(0) sind(0) 0]
    p2 = P * [cosd(120) sind(120) 0]
    p3 = P * [cosd(240) sind(240) 0]

    B1 = (B * [cosd(0) sind(0) 0])
    B2 = (B * [cosd(120) sind(120) 0])
    B3 = (B * [cosd(240) sind(240) 0])
