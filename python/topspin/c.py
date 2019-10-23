from __future__ import division
from math import *
from sys import argv

def parse_code():

    if len(argv) > 2:
        raise ValueError("Input should not have any whitespace")

    try:
        code = argv[1]
    except:
        raise ValueError("Input not understood or is not given")

    return code

  
def evaluate_expression(): 
  
    # expression to be evaluated 
    expr = parse_code()
  
    # evaluating expression 
    out = eval(expr, {"__builtins__":None}, safe_dict) 
  
    # printing evaluated result 
    MSG("{}".format(out)) 

    return
  
if __name__ == "__main__": 
  
    # methods 
    safe_list = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 
                 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 
                 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 
                 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 
                 'tan', 'tanh'] 
  
    safe_dict = dict([(k, locals().get(k, None)) for k in safe_list]) 
  
    evaluate_expression() 
