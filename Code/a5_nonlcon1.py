# Autor: Yanpeng Mei
# Created at : 10.02.2022

'''
'a5_nonlcon1' is the non-linear constraint for the optimization, when the tolerance band is exactly defined(my method)
cp   -   control points of the original surface
cpVar   -   optimization variable
path / pathVar   -   are similarly defined
'''

import pickle
from a3_path import a3_path


def a5_nonlcon1(cpVar):
    with open('a2_parameters.txt', 'rb') as open1:
        temp1 = pickle.load(open1)
    tb_r = temp1['tb_r']
    cp = temp1['cp']

    path = a3_path(cp)
    pathVar = a3_path(cpVar)

    temp2 = 0
    temp3 = path.shape[1]
    for i in range(temp3):
        temp4 = ((pathVar[0, i] - path[0, i])**2 + (pathVar[1, i] - path[1, i])**2 + (pathVar[2, i] - path[2, i])**2)**(1/2)
        if temp4 <= tb_r:
            temp2 = temp2 + 1

    nonLinearCond = temp2 - temp3

    return nonLinearCond
