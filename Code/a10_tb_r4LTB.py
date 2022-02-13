# Autor: Yanpeng Mei
# Created at : 13.02.2022

'''
'a10_tb_r4LTB'    -   find the new tolerance band radius, when the tolerance band is linearly defined(traditional way)
cp4opt0   -   control points of the original surface in 'list' form
finerPath   -   original path with more sampling points
'''

import pickle
import numpy as np
from a3_path import a3_path
from a6_finerPath import a6_finerPath

def a10_tb_r4LTB():
    with open('a2_parameters.txt', 'rb') as open1:
        temp1 = pickle.load(open1)
    tb_r = temp1['tb_r']
    cp4opt0 = temp1['cp4opt0']
    cp0 = temp1['cp0']
    numP = temp1['numP']
    numS = temp1['numS']

    path = a3_path(cp4opt0)
    finerPath = a6_finerPath(cp0)
    numpp = path.shape[1]  # number of points in path

    # construct (numpp - 1) lines
    k = np.zeros((1, numpp - 1))  # k - slope of these lines
    b = np.zeros((1, numpp - 1))  # b - intercept of these lines
    maxdisPL = np.zeros((1, numpp - 1))  # maximum distance between lines and the points in finer path
    finerPath2D = np.zeros((2, finerPath.shape[1]))
    consfac = 10  # the 'consfac' should be the same as in function a6_finerPath line 27

    for i in range(numS):
        p_start = 0
        p_end = numP[i] - 1
        if (path[0, p_start + 1] - path[0, p_start]) != 0 and (
                path[1, p_start + 1] - path[1, p_start]) <= 0.0001:  # u-segment
            finerPath2D[0, p_start:((p_end + 1) * consfac + 1)] = finerPath[0, p_start:((p_end + 1) * consfac + 1)]
            finerPath2D[1, p_start:((p_end + 1) * consfac + 1)] = finerPath[2, p_start:((p_end + 1) * consfac + 1)]
            k[0, p_start:p_end] = (path[2, (p_start + 1):(p_end + 1)] - path[2, p_start:p_end]) / (
                        path[0, (p_start + 1):(p_end + 1)] - path[0, p_start:p_end])
            b[0, p_start:p_end] = path[2, (p_start):(p_end)] - k[0, p_start:p_end] * path[0, (p_start):(p_end)]
        elif (path[0, p_start + 1] - path[0, p_start]) <= 0.0001 and (
                path[1, p_start + 1] - path[1, p_start]) != 0:  # v-segment
            finerPath2D[0, p_start:((p_end + 1) * consfac)] = finerPath[1, p_start:((p_end + 1) * consfac)]
            finerPath2D[1, p_start:((p_end + 1) * consfac)] = finerPath[2, p_start:((p_end + 1) * consfac)]
            k[0, p_start:p_end] = (path[2, (p_start + 1):(p_end + 1)] - path[2, p_start:p_end]) / (
                        path[1, (p_start + 1):(p_end + 1)] - path[1, p_start:p_end])
            b[0, p_start:p_end] = path[2, (p_start):(p_end)] - k[0, p_start:p_end] * path[1, (p_start):(p_end)]
        # if we rewrite y=k*x+b in the form of A*x+B*y+C=0 then we get:
        A = k
        B = np.zeros((1, k.shape[1])) - 1
        C = b

        temp2 = np.zeros((1, consfac))
        for j in range(p_start, p_end):
            for kk in range(consfac):
                temp2[0, kk] = np.absolute(
                    A[0, j] * finerPath2D[0, consfac * j + kk] + B[0, j] * finerPath2D[1, consfac * j + kk] + C[0, j]) / (
                                           (A[0, j] ** 2 + B[0, j] ** 2) ** (1 / 2))
            maxdisPL[0, j] = np.max(temp2)

        if i + 1 < numS:
            p_start = p_end
            p_end = p_end + numP[i + 1] - 1

    safety_factor = 10
    tb_r4LTB = tb_r - np.max(maxdisPL) * safety_factor

    return tb_r4LTB