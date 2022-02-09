# Autor: Yanpeng Mei
# Created at : 29.01.2022

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
    [mc, nc] = np.shape(c)
    nk = np.size(k)
    dc = np.zeros((mc, nc - 1))
    for i in range(nc - 1):
        temp = d / (k[i+d+1] - k[i+1])
        dc[:, i] = temp * (c[:, i+1] - c[:, i])
    dk = k[1: (nk - 1)]
    return dc, dk


'''
# test
d = 3
c = np.asarray([ [0, 10, 20, 30, 40, 50],
                          [0, 5, -5, 5, -5, 0] ])
k = np.asarray([0, 0, 0, 0, 1/3, 2/3, 1, 1, 1, 1])
dc, dk = bspderiv(d, c, k)
print('dc = ', dc)
print('dk = ', dk)
print('type of dk is ', type(dk))
# dc should be [[ 90.  45.  30.  45.  90.]
#                        [ 45. -45.  30. -45.  45.]]
# dk should be [0.       0.       0.       0.33333333 0.66666667    1.      1.      1.]
'''
