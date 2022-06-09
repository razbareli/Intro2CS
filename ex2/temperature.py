######################
# FILE:temperature.py
# WRITER:Raz_Bareli  unixraz 203488747
# EXERCISE:intro2cs1 ex2 2021
# DESCRIPTION: function that predicts summer
######################

def is_it_summer_yet(min, a, b, c):
    """trying to predict if summer has arrived"""
    if a > min:
        if b > min:
            return True
        return c > min
    return b > min and c > min
