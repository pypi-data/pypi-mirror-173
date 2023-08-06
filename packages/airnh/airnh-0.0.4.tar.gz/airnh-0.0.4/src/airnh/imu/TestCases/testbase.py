import numpy as np
import pandas as pd

def compNum(v1, v2):
    try:
        if v1 is None or v2 is None:
            return False
        else:
            return np.abs(v1 - v2) < 10**-3
    except Exception as e:
        print(e)
        return False
    
def compNPArray(a1, a2):
    try:
        if a1 is None or a2 is None:
            return False
        elif a1.shape != a2.shape:
            return False        
        else:
            return np.array_equal(a1, a2)
    except Exception as e:
        print(e)
        return False

def compArraySim(a, b, tolerance = 10**-1):
    try:
        if a is None or b is None:
            return False
        elif a.shape != b.shape:
            # print('\033[91m ' + "different array size:" + '\033[0m')
            # print(f"a:{a.shape}")
            # print(f"b:{b.shape}")
            return False        
        else:
            diff = a-b
            err = np.linalg.norm(diff)
            if err < tolerance:
                return True
            else:
                return False
    except Exception as e:
        print(e)
        return False

def checker(cond, msg):
    if cond:
        print('\033[1m' + '\033[92m  \u2714 ' + msg  +  '\033[0m')
    else:
        print('\033[91m \u274c ' + msg + '\033[0m')
