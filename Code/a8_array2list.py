# Autor: Yanpeng Mei
# Created at : 13.02.2022

'''
'a8_array2list'    -   convert the form of the control points from numpy.array into a one-dimensional list
cp   -   control points of the NURBS-surface, form: numpy.array
cp4opt   -   tcontrol points of the NURBS-surface, form: list
'''

import numpy as np

def a8_array2list(cp):
    dim1 = np.shape(cp)
    dim2 = dim1[0]*dim1[1]*dim1[2]
    cp4opt = list(np.zeros((1, dim2)))
    temp1 =0
    for i in range((dim1[2])):
        for j in range((dim1[0])):
            cp4opt[dim1[1]*temp1: dim1[1]*(temp1+1)] = cp[j, :, i]
            temp1 = temp1+1

    return cp4opt