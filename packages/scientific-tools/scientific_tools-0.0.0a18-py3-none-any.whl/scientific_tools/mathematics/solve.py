"""This file contains functions to solve equations."""

def dichotomy(f, x_min, x_max, args_before_x=[], args_after_x=[], accuracy=-3):
    """Search the x value to obtain f(x)=0 with an accuracy of 10^(accuracy).
    
    This function is based on the dichotomous algorithm.

    function is a function with at least one argument x. f(x_min) and f(x_max) must have different signs (one positive and one negative).
    args_before_x is the list of positional arguments before the variable argument's position
    args_after_x is the list of positional arguments after the variable argument's position
    The value of the variable argument x varies from min_x to max_variable
    """
    a = x_min
    b = x_max
    while b-a > 10**accuracy :
        m = (b-a)/2
        y_a = f(*args_before_x, a, *args_after_x)
        y_m = f(*args_before_x, m, *args_after_x)
        if y_m == 0 :
            return m
        elif y_a*y_m > 0 :
            a = m
        else :
            b = m
    return (b-a)/2    
