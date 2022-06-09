######################
# FILE:calculate_mathematical_expression.py
# WRITER:Raz_Bareli  unixraz 203488747
# EXERCISE:intro2cs1 ex2 2021
# DESCRIPTION: math expression calculations
######################

def calculate_mathematical_expression(num1, num2, operation):
    """calculates 2 numbers with an operation within them"""
    if operation == "+":
        return num1 + num2
    if operation == ":" and num2 != 0:
        return num1 / num2
    if operation == ":" and num2 == 0:
        return None
    if operation == "-":
        return num1 - num2
    if operation == "*":
        return num1 * num2
    else:
        return None

def calculate_from_string(string):
    """calculates the math expression directly from the string"""
    x = string.split()
    num1 = float(x[0])
    num2 = float(x[2])
    operation = x[1]
    y = calculate_mathematical_expression(num1, num2, operation)
    return y








