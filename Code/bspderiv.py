# Autor: Yanpeng Mei
# Created at : 29.01.2022

'''
This function was originally written in Matlab by Mark Spink in 2000 and modified by Daniel Claxton in 2007.
I re-write it in python.
To avoid mistakes, the input and output(Type, Size and Value) of each function will be exactly the same as in Matlab !!!!!!
'numpy' should be installed and imported !!!!!!
'''

'''
bspderiv:  B-Spline derivative

Meaning of the input:
d - degree of the B-Spline
c - control points            double  matrix(mc,nc)
k - knot sequence           double  vector(nk)

Meaning of the output:
dc - control points of the derivative       double  matrix(mc,nc)
dk - knot sequence of the derivative      double  vector(nk)

Modification of Algorithm A3.3 from 'The NURBS BOOK' pg98
'''

import numpy as np


def bspderiv(d, c, k):
    [mc,nc] = np.shape(c)
    nk = np.size(k)
    dc = np.zeros((mc, nc - 1))
    for i in range(nc - 1):
        temp = d / (k[i+d+1] - k[i+1])
        dc[0:(mc-1), i] = temp * (c[0:(mc-1), i+1] - c[1:mc, i])
    dk = k[1: (nk - 1)]
    return dc, dk


'''
# test
d = 3
c = np.asarray([ [0, 10, 20, 30, 40, 50],
                          [0, 5, -5, 5, -5, 0] ])
k = np.asarray([0, 0, 0, 1/4, 2/4, 3/4, 1, 1, 1])
dc, dk = bspderiv(d, c, k)
print('dc = ', dc)
print('dk = ', dk)
# dc should be [ [ 60.  60. 140. 210. 660.]
#                        [  0.   0.   0.   0.   0.] ]
# dk should be [[0.   0.   0.25 0.5  0.75 1.   1.  ]]
'''
