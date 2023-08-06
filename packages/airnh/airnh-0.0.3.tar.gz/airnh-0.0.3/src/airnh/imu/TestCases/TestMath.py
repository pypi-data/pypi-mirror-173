import numpy as np

def compNum(v1, v2):
    if v1 is None or v2 is None:
        return False
    else:
        return np.abs(v1 - v2) < 10**-3
    
def compNPArray(a1, a2):
    if a1 is None or a2 is None:
        return False
    else:
        return np.array_equal(a1, a2)

def checker(cond, msg):
    if cond:
        print('\033[1m' + '\033[92m  \u2714 ' + msg  +  '\033[0m')
    else:
        print('\033[91m \u274c ' + msg + '\033[0m')
        

def test_trig(fList):
    checker(compNum(np.sin(30*np.pi/180), fList[0](30)), "Sine")
    checker(compNum(np.cos(30*np.pi/180), fList[1](30)), "Cosine")
    checker(compNum(np.tan(30*np.pi/180), fList[2](30)), "Tangent")
    checker(compNum(np.arcsin(0.5)*180/np.pi, fList[3](0.5)), "Arcsine")
    checker(compNum(np.arccos(0.2)*180/np.pi, fList[4](0.2)), "Arccosine")
    checker(compNum(np.arctan(0.1)*180/np.pi, fList[5](0.1)), "Arctangent")

def test_atan2(foo):
    checker(compNum(np.arctan2(1, 1)*180/np.pi, foo(1, 1)), "Arctangent [1, 1] (y, x) =  45 deg")
    checker(compNum(np.arctan2(-1, 1)*180/np.pi, foo(-1, 1)), "Arctangent [-1, 1] (y, x) = -45 deg")
    checker(compNum(np.arctan2(-1, -1)*180/np.pi, foo(-1, -1)), "Arctangent [-1, -1] (y, x) = -135 deg")
    checker(compNum(np.arctan2(1, -1)*180/np.pi, foo(1, -1)), "Arctangent [1, -1] (y, x) = 135 deg")
    
    
    
def test_norm(foo):
    x = np.array([4.076, 3.31, 2.55])
    checker(compNum(np.linalg.norm(x), foo(x)), "Vector Norm")
    
    
def test_normalize(foo):
    x = np.random.rand(3,1)
    checker(compNPArray(x/np.linalg.norm(x), foo(x)), "Vector Normalization")


def test_dot(foo):
    a = np.random.rand(1,3)
    b = np.random.rand(1,3).T
    checker(compNum(np.dot(a,b), foo(a,b)), "Vector Dot Product")


def test_calcDotAngle(foo):
    a = np.array([0, 1])
    rad = np.random.rand()
    R = np.array([[np.cos(rad), -np.sin(rad)],[np.sin(rad), np.cos(rad)]])
    b = np.matmul(R, a)
    checker(compNum(rad*180/np.pi, foo(a, b)), "Find angle by dot product")

def test_cross(foo):
    a = np.random.rand(1,3)
    b = np.random.rand(1,3)
    checker(compNPArray(np.cross(a,b), foo(a,b)), "Vector Cross Product")
    
def test_calcCrossAngle(foo):
    a = np.array([0, 1])
    rad = -np.random.rand()
    R = np.array([[np.cos(rad), -np.sin(rad)],[np.sin(rad), np.cos(rad)]])
    b = np.matmul(R, a)
    checker(compNum(rad*180/np.pi, -foo(a, b)), "Find angle by cross product")
    
def test_vec_shape1x3(vec):
    checker(vec.shape == (1,3), "Vector Shape 1x3")
    
def test_vec_t(vec, transpose):
    checker(compNPArray(vec.T, transpose), "Vector Transpose")
    
def test_mat_t(mat, mT):
    checker(compNPArray(mat.T, mT), "Matrix Transpose")

def test_matmul_correct(ans):
    checker([])
    
def test_matmul(m, a, fList):
    cond = True
    for func in fList:
        res = func(m,a)
        cond = cond and compNPArray(res, np.matmul(m, a))
    checker(cond, "Matrix multiplication")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    