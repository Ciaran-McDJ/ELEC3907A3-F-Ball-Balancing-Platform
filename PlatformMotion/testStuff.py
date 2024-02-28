import numpy as np

from helperFuncs import *

A = np.array([[0,0,0],[2,0,0],[0,0,0]])
B = np.array([[1,0,0],[0,0,0],[0,0,0]])

R = np.matmul(A, B)

print(R)