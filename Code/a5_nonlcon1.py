# Autor: Yanpeng Mei
# Created at : 10.02.2022

'''
'a5_nonlcon1'    -   the non-linear constraint for the optimization, when the tolerance band is exactly defined(my method)
cp4opt0   -   control points of the original surface in 'list' form
cp4opt   -   the optimization variable
'''

import pickle
from a3_path import a3_path


def a5_nonlcon1(cp4opt):
    with open('a2_parameters.txt', 'rb') as open1:
        temp1 = pickle.load(open1)
    tb_r = temp1['tb_r']
    cp4opt0 = temp1['cp4opt0']

    path = a3_path(cp4opt0)
    pathVar = a3_path(cp4opt)

    temp2 = 0
    temp3 = path.shape[1]
    for i in range(temp3):
        temp4 = ((pathVar[0, i] - path[0, i])**2 + (pathVar[1, i] - path[1, i])**2 + (pathVar[2, i] - path[2, i])**2)**(1/2)
        if temp4 <= tb_r:
            temp2 = temp2 + 1

    nonLinearCond = temp3 -temp2

    return nonLinearCond
