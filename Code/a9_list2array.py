# Autor: Yanpeng Mei
# Created at : 13.02.2022

'''
'a9_list2array'    -   convert the form of the control points from one-dimensional list into numpy.array
cp4opt   -   tcontrol points of the NURBS-surface, form: list
cp   -   control points of the NURBS-surface, form: numpy.array
'''

import numpy as np
import pickle

def a9_list2array(cp4opt):
    with open('a2_parameters.txt', 'rb') as open1:
        temp1 = pickle.load(open1)
    cp_orig = temp1['cp0']

    dim1 = np.shape(cp_orig)
    cp = np.zeros(dim1)
    temp1 =0

    for i in range((dim1[2])):
        for j in range((dim1[0])):
            cp[j, :, i] = cp4opt[dim1[1]*temp1: dim1[1]*(temp1+1)]
            temp1 = temp1+1

    return cp