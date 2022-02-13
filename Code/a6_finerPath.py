# Autor: Yanpeng Mei
# Created at : 10.02.2022


'''
a6_finerPath:  get a finer tool path with given Tuple(with more sampling points, see line 27-28)
This finer path will be used in function 'a7__nonlcon2' to get a nonlinear condition of linear defined tolerance band

Meaning of the input:
cp0 - control points of the test surface

Meaning of the output:
finerPath - tool path in 3D-coordinate
'''

import numpy as np
import pickle
from nrbmak import nrbmak
from nrbeval import nrbeval


def a6_finerPath(cp0):
    with open('a2_parameters.txt', 'rb') as open1:
        temp1 = pickle.load(open1)
    knots = temp1['knots']
    tpl = temp1['tpl']
    consfac = 10
    numP = temp1['numP']*consfac
    numS = temp1['numS']
    segType = temp1['segType']

    surface = nrbmak(cp0, knots)
    finerPath = np.zeros((3, (np.sum(numP) - numS +1)))
    temp2 = 0

    for i in range(numS):
        if segType[i, 1]==1:       # u-segment with constant v
            ut_path = list(np.linspace(tpl[i, 0], tpl[i + 1, 0], numP[i]))
            vt_path = list(np.linspace(0, 0, numP[i]) + tpl[i, 1])
            tt = (ut_path, vt_path)
            temp3 = nrbeval(surface, tt)
            if i == 0:
                temp2 = temp2 + numP[i]
                finerPath[:, 0:numP[i]] = temp3[:, :, 0]
            else:
                temp2 = temp2 + numP[i] - 1
                finerPath[:, (temp2 - numP[i]):temp2] = temp3[:, :, 1]
        elif segType[i, 1]==2:       # v-segment with constant u
            ut_path = list(np.linspace(0, 0, numP[i]) + tpl[i, 0])
            vt_path = list(np.linspace(tpl[i, 1], tpl[i+1, 1], numP[i]))
            tt = (ut_path, vt_path)
            temp4 = nrbeval(surface, tt)
            temp5 = temp4.transpose(0, 2, 1)
            if i==0:
                temp2 = temp2 + numP[i]
                finerPath[:, 0:numP[i]] = temp5[:, :, 1]
            else:
                temp2 = temp2 + numP[i] - 1
                finerPath[:, (temp2 - numP[i]):temp2] = temp5[:, :, 1]

    return finerPath