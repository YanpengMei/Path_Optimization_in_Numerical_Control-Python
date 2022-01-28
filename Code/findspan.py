# Autor: Yanpeng Mei
# Created at : 28.01.2022

'''
This function was originally written in Matlab by Rafael Vazquez in 2010.
I re-write it in python.
To avoid mistakes, the input and output(Type, Size and Value) of each function will be exactly the same as in Matlab !!!!!!
'numpy' should be installed and imported !!!!!!
'''

'''
basicfun:  Basis function for B-Spline

Meaning of the input:
n - number of control points - 1
p - spline degree
u - parametric point
U - knot sequence

Meaning of the output:
s - knot span index

Modification of Algorithm A2.1 from 'The NURBS BOOK' pg68
'''


import numpy as np

def findspan(n,p,u,U):
    s = np.zeros(np.size(u), dtype=int)       # datatype in s should be int
    for j in range(np.size(u)):
        if u[j] == U[n+1]:
            s[j] = n
            continue
        temp1=np.arange(len(U))
        temp2 = max(temp1[U<=u[j]] )
        s[j] = temp2
    return s


'''
# test 1
import numpy as np
from findspan import findspan
n = 3
U = np.asarray([0, 0, 0, 1/2, 1, 1, 1])
p = 2
u = np.linspace(0, 1, 10)
s = findspan(n, p, u, U)
print(s)
print(type(s[0]))
# s should be [2   2   2   2   2   3   3   3   3   3]
'''

'''
# test 2
import numpy as np
from findspan import findspan
p = 2
m = 7
n = m - p - 1
U = np.asarray([0, 0, 0, 1/3, 2/3, 1, 1, 1])
u = np.asarray([ 0,   0.11880,   0.55118,   0.93141,   0.40068,   0.35492, 0.44392,   0.88360,   0.35414,   0.92186,   0.83085,   1])
s = findspan (n, p, u, U)
print(s)
print(type(s[0]))
# s should be [2   2   3   4   3   3   3   4   3   4   4   4]
'''