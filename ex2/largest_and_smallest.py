######################
# FILE:largest_and_smallest.py
# WRITER:Raz_Bareli  unixraz 203488747
# EXERCISE:intro2cs1 ex2 2021
# DESCRIPTION: function that determines largest and smallest number
# I chose the 2 cases in the checking function, to cover for all extreme cases. The 2 missing cases
# where that all 3 numbers are equal, and that only the right number is the largest and two other are identical
######################

def largest_and_smallest(x, y, z):
    """return largest and smallest number"""
    if x >= y >= z:
        return x, z
    if z >= y >= x:
        return z, x
    if x >= z >= y:
        return x, y
    if y >= z >= x:
        return y, x
    if y >= x >= z:
        return y, z
    if z >= x >= y:
        return z, y

def check_largest_and_smallest():
    """checks the function largest_and_smallest"""
    a = (17, 1) == largest_and_smallest(17, 1, 6)
    b = (17, 1) ==largest_and_smallest(1, 17, 6)
    c = (2, 1) == largest_and_smallest(1, 1, 2)
    d = (17, 1) == largest_and_smallest(1, 1, 17)
    e = (1, 1) == largest_and_smallest(1, 1, 1)
    return a == b == c == d == e