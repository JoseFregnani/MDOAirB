"""" 
Function  : area_triangle_3d.py
Title     : Triangle area 3D
Written by: Alejandro Rios
Date      : November/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module calculate the area triangle for applications in 3D surfaces area calculation

Future implementations:
    - 

Inputs:
    - Triangle coordinates x, y, z
Outputs:
    - area 
"""
########################################################################################
"""Importing Modules"""
########################################################################################
########################################################################################
"""Function definition"""
########################################################################################




import numpy as np
def area_triangle_3d(x, y, z):

    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    #
    y1 = y[0]
    y2 = y[1]
    y3 = y[2]
    #
    z1 = z[0]
    z2 = z[1]
    z3 = z[2]
    # A=sqrt(s*(s-a)*(s-b)*(s-c))
    # Method  2
    # https://math.stackexchange.com/questions/128991/how-to-calculate-area-of-3d-triangle
    T1 = (x2*y1 - x3*y1 - x1*y2 + x3*y2 + x1*y3 - x2*y3)**2
    T2 = (x2*z1 - x3*z1 - x1*z2 + x3*z2 + x1*z3 - x2*z3)**2
    T3 = (y2*z1 - y3*z1 - y1*z2 + y3*z2 + y1*z3 - y2*z3)**2
    area = (np.sqrt(T1+T2+T3)/2)
    return(area)
