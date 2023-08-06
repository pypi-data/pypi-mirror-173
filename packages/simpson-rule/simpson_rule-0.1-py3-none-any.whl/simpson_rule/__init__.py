def simpson_rule(f, a: float, b: float, 
                     n: int) -> float:
    """
    Returns a numerical approximation of the definite integral 
    of f between a and b by the Simpson rule.
   
    Parameters:
        f(function): function to be integrated
        a(float): low bound
        b(float): upper bound
        n(int): number of iterations of the numerical approximation
       
    Returns:
        result(float): the numerical approximation of the definite integral    
   

    """
    
    assert n % 2 == 0   # to verify that n is even
    
    # Definition of step and the result
    step = (b - a)/n
    result = f(a) + f(b)          # first and last
    
    # Moving Variable in X-axis
    xn = a + step 
    
    # Sum of y-pairs
    for i in range(n-1):
        if i % 2 == 0:
            result += 4 * f(xn)
        else:
            result += 2 * f(xn)
       
        
        xn += step
        

    return (step/3) * result