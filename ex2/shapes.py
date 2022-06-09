######################
# FILE:shapes.py
# WRITER:Raz_Bareli  unixraz 203488747
# EXERCISE:intro2cs1 ex2 2021
# DESCRIPTION: function that calculates the area of a shape
######################

import math

def shape_area():
    """calculates areas of 3 different shapes"""
    num = float(input("Choose shape (1=circle, 2=rectangle, 3=triangle): "))
    if num != 1 and num != 2 and num != 3:
        return None
    if num == 1:
        r = float(input())
        return math.pi * r**2
    if num == 2:
        a = float(input())
        b = float(input())
        return a * b
    if num == 3:
        t = float(input())
        return math.sqrt(3)/4 * t**2
