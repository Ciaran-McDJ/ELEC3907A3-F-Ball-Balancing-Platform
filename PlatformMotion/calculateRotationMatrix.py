import numpy as np

from helperFuncs import *




def calculateRotationMatrix(pitch:float, roll:float):
    """
    Calculate the rotation matrix for a pitch + roll movement
    Rotation about y is pitch, and rotation about x is roll
    
    inputs:
    float pitch Angle of platform in degrees
    float roll Angle of platform in degrees

    output:
    TODO
    """

    R_pitch = [[cosd(pitch), 0, sind(pitch)], [0, 1, 0], [-sind(pitch), 0, cosd(pitch)]]
    R_roll = [[1, 0, 0], [0, cosd(roll), -sind(roll)], [0, sind(roll), cosd(roll)]]

    R = np.matmul(R_pitch, R_roll)

    return R

print(calculateRotationMatrix(45,45))