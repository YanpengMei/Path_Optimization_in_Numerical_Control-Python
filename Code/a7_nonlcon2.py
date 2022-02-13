# Autor: Yanpeng Mei
# Created at : 11.02.2022

'''
'a7_nonlcon2'    -   the non-linear constraint for the optimization, when the tolerance band is linearly defined(traditional way)
cp4opt0   -   control points of the original surface in 'list' form
cp4opt   -   the optimization variable
'''

import pickle
from a3_path import a3_path


def a7_nonlcon2(cp4opt):
    with open('a2_parameters.txt', 'rb') as open1:
        temp0 = pickle.load(open1)
    cp4opt0 = temp0['cp4opt0']
    with open('a2_tb_r4Ltb.txt', 'rb') as open2:
        temp1 = pickle.load(open2)
    tb_r4Ltb = temp1['tb_r4Ltb']


    path = a3_path(cp4opt0)
    pathVar = a3_path(cp4opt)

    temp2 = 0
    temp3 = path.shape[1]
    for i in range(temp3):
        temp4 = ((pathVar[0, i] - path[0, i])**2 + (pathVar[1, i] - path[1, i])**2 + (pathVar[2, i] - path[2, i])**2)**(1/2)
        if temp4 <= tb_r4Ltb:
            temp2 = temp2 + 1

    nonLinearCond = temp3 -temp2

    return nonLinearCond
