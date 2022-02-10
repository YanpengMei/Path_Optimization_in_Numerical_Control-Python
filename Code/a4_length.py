# Autor: Yanpeng Mei
# Created at : 10.02.2022

'''
a4_length:  get the length of the tool path

Meaning of the input:
cp - control points of the test surface

Meaning of the output:
length - length of the tool path
'''

import numpy as np
from a3_path import a3_path


def a4_length(cp):
    path = a3_path(cp)
    length = np.sum(((path[0, 1:] - path[0, 0:-1])**2 + (path[1, 1:] - path[1, 0:-1])**2 + (path[2, 1:] - path[2, 0:-1])**2)**(1/2))
    return length