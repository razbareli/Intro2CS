######################
# FILE:quadratic_equation.py
# WRITER:Raz_Bareli  unixraz 203488747
# EXERCISE:intro2cs1 ex2 2021
# DESCRIPTION: function that solves quadratic equation
######################

import math

def quadratic_equation(a, b, c):
    """solves quadratic equation"""
    if (b**2 - 4*a*c) > 0:
        x1 = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)
        x2 = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)
        return x1, x2
    if (b**2-4*a*c) == 0:
        x1 = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)
        x2 = None
        return x1, x2
    else:
        x1 = None
        x2 = None
        return x1, x2

def quadratic_equation_user_input():
    """solves quadratic equation with user input"""
    user = input("Insert coefficients a, b, and c: ")
    u = user.split()
    a = float(u[0])
    b = float(u[1])
    c = float(u[2])
    if a == 0:
        print("The parameter 'a' may not equal 0")
    else:
        x1, x2 = quadratic_equation(a, b, c)
        if x1 == x2 == None:
            print("The equation has no solutions")
        elif x1 == None or x2 == None:
            if x1 == None:
                print("The equation has 1 solution:", end=" ")
                print(x2)
            else:
                print("The equation has 1 solution:", end=" ")
                print(x1)
        else:
            print("The equation has 2 solutions:", end=" ")
            print(x1, "and", x2)

