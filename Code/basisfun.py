# Autor: Yanpeng Mei
# Created at : 28.01.2022

'''
basicfun:  Basis function for B-Spline

Meaning of the input:
iv - knot span (from FindSpan() )
uv - parametric points
p - spline degree
U - knot sequence 

Meaning of the output:
b - Basis functions vector

Adapted from Algorithm A2.2 from 'The NURBS BOOK' pg70.
'''

import numpy as np


def basisfun(iv, uv, p, U):
    b = np.zeros((np.size(uv), p + 1))
    for jj in range(1, np.size(uv)+1):
        i = iv[jj - 1] + 1
        u = uv[jj - 1]
        left = np.zeros((p + 1, 1))
        right = np.zeros((p + 1, 1))
        n = np.zeros(p+1)
        n[0] = 1
        for j in range(1, p+1):
            left[j] = u - U[i - j]
            right[j] = U[i + j - 1] - u
            saved = 0
            for r in range(j):
                temp = n[r] / (right[r + 1] + left[j - r])
                n[r] = saved + right[r + 1] * temp
                saved = left[j - r] * temp
            n[j] = saved
        b[jj - 1, :] = n
    return b


''' 
# test
n = 3
U = [0 0 0 1/2 1 1 1]
p = 2
u = np.linspace (0, 1, 10);  
s = findspan (n, p, u, U);  
b = basisfun (s, u, p, U)
# b should be [ [1.                   0.                   0.        ]
#                         [0.60493827   0.37037037   0.02469136]
#                         [0.30864198   0.59259259   0.09876543]
#                         [0.11111111   0.66666667   0.22222222]
#                         [0.01234568   0.59259259   0.39506173]
#                         [0.39506173   0.59259259   0.01234568]
#                         [0.22222222   0.66666667   0.11111111]
#                         [0.09876543   0.59259259   0.30864198]
#                         [0.02469136   0.37037037   0.60493827]
#                         [0.                   0.                   1.                ] ]
'''
