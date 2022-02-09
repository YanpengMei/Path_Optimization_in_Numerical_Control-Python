# Autor: Yanpeng Mei
# Created at : 29.01.2022

'''
bspeval:  Evaluate B-Spline at parametric points

Meaning of the input:
d - Degree of the B-Spline.
c - Control Points, matrix of size (dim,nc).
k - Knot sequence, row vector of size nk.
u - Parametric evaluation points, row vector of size nu.

Meaning of the output:
p - Evaluated points, matrix of size (dim,nu)
'''

import numpy as np
from findspan import findspan
from basisfun import basisfun


def bspeval(d, c, k, u):
    nu = np.size(u)
    [mc, nc] = np.shape(c)
    s = findspan(nc - 1, d, u, k)
    b = basisfun(s, u, d, k)
    temp1 = s - d + 1
    p = np.zeros((mc, nu))
    for i in range(d+1):
        temp2 = np.tile(b[:, i].T, (mc, 1))
        p = p +  temp2* c[:,temp1 + i - 1]
    return p


'''
# test
d = 3
c = np.asarray([[0, 10, 20, 30, 40, 50],
                         [0, 5,  -5, 5,  -5, 0 ]])
k = np.asarray([0, 0, 0, 0, 1/3, 2/3, 1, 1, 1, 1])
u = np.linspace(0,1,10)
p = bspeval(d,c,k,u)
print(p)
# p should be
#    [[ 0.   8.48765432   14.56790123    19.16666667    23.11728395    26.88271605   30.83333333    35.43209877    41.51234568    50.        ]
#     [ 0.   2.19135802   0.86419753       -0.83333333     -0.58641975      0.58641975   0.83333333       -0.86419753    -2.19135802      0.        ]]
'''
