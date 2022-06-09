######################
# FILE:math_print.py
# WRITER:Raz Bareli 203488747
# EXERSISE:intro2cs1 ex1 2021
# DESCRIPTION: using math module and print function
######################

import math

def golden_ratio():
    """prints the golden ratio"""
    print(2*math.cos(math.pi/5))
def six_squared():
    """calculated 6 squared"""
    print(6**2)
def hypotenuse():
    """calculates hypotenuse of rectangle"""
    print(math.sqrt(5**2+12**2))
def pi():
    """prints number Pi"""
    print(math.pi)
def e():
    """prints number e"""
    print(math.e)
def squares_area():
    """prints area of multipule squares"""
    print(1**2, 2**2, 3**2, 4**2, 5**2, 6**2, 7**2, 8**2, 9**2, 10**2)

if __name__ == "__main__":
    golden_ratio()
    six_squared()
    hypotenuse()
    pi()
    e()
    squares_area()

