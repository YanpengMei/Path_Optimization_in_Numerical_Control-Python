# Autor: Yanpeng Mei
# Created on : 03.02.2022

'''
nrbeval:  Evaluate a NURBS at parametric points

Meaning of the input:
nurbs - Dictionary of NURBS curve or Surface (see nrbmak)
tt - Parametric evaluation points along U and v direction
tt = ([ut], [vt]) for surface or tt = ([ut]) for curve

Meaning of the output:
p - Evaluated points on the NURBS curve, surface in Cartesian coordinates (x,y,z)
'''

import numpy as np
from bspeval import bspeval


def nrbeval(nurbs, tt):
    st1 = len(tt[0])
    p = np.zeros((3, st1))
    if len(tt) == 1: # NURBS structure represents a curve
        temp1 = nurbs['Order']
        temp2 = nurbs['Knots']
        val = bspeval((temp1[0] - 1), nurbs['CP'], np.asarray(temp2[0]), np.asarray(tt[0]))
        p = val[0:3, :]
    elif len(tt) == 2: # NURBS structure represents a surface
        temp3 = nurbs['NumCP']
        num1 = temp3[0]
        num2 = temp3[1]
        temp4 = nurbs['Order']
        degree1 = temp4[0] - 1
        degree2 = temp4[1] - 1
        nt1 = len(tt[0])
        nt2 = len(tt[1])

        #temp5 = np.zeros((4*num1, num2))   # Evaluate along the v direction
        temp5 = nurbs['CP']
        temp6 = temp5.reshape((4*num1, num2))
        temp7 = nurbs['Knots']
        temp8 = bspeval(degree2,temp6,np.asarray(temp7[1]),np.asarray(tt[1]))
        temp9 = temp8.reshape((4, num1, nt2))

        temp10 = temp9.transpose((0, 2, 1))    # Evaluate along the u direction
        temp11 = np.reshape(temp10,(4*nt2, num1))
        temp12 = nurbs['Knots']
        temp12 = bspeval(degree1, temp11, np.asarray(temp12[0]), np.asarray(tt[0]))
        temp13 = np.reshape(temp12, (4, nt2, nt1))
        val = np.transpose(temp13, (0, 2, 1))
        p = val[0:3, :, :]

    return p

'''
# test 1
cp_cur = np.asarray([[0.5, 1.5, 4.5, 3.0, 7.5, 6.0, 8.5],
                                  [3.0, 5.5, 5.5, 1.5, 1.5, 4.0, 4.5]])
knot = ([0, 0, 0, 1/4, 1/2, 3/4, 3/4, 1, 1, 1], )
crv = nrbmak(cp_cur, knot)
ut = (list(np.linspace(0,1,10)), )
p = nrbeval(crv, ut)
print(p)
# p sshould be
#[[0.5    1.48765432     2.67283951   3.75                 3.97222222     3.67592593     5.08333333     7.21604938     7.06790123     8.5],
# [3.      4.72839506     5.4691358     5.27777778     4.29012346     2.70987654     1.72222222     2.0308642       3.66049383     4.5],
# [0.       0.                    0.                   0.                     0.                     0.                      0.                    0.                     0.                     0.  ]]
'''
'''
# test 2
cp_sur = np.zeros((3,5,5))
cp_sur[:,:,0] = [ [0.0,  3.0,  5.0,  8.0, 10.0],
                         [0.0,  0.0,  0.0,  0.0, 0.0],
                         [2.0,  2.0,  7.0,  7.0,  8.0] ]
cp_sur[:,:,1] = [ [0.0,  3.0,  5.0,  8.0, 10.0],
                         [3.0,  3.0,  3.0,  3.0,  3.0],
                         [0.0,  0.0,  5.0,  5.0,  7.0] ]
cp_sur[:,:,2] = [ [0.0,  3.0,  5.0,  8.0, 10.0],
                         [5.0,  5.0,  5.0,  5.0,  5.0],
                         [0.0,  0.0,  5.0,  5.0,  7.0] ]
cp_sur[:,:,3] = [ [0.0,  3.0,  5.0,  8.0, 10.0],
                         [8.0,  8.0,  8.0,  8.0,  8.0],
                         [5.0,  5.0,  8.0,  8.0, 10.0] ]
cp_sur[:,:,4] = [ [0.0,  3.0,  5.0,  8.0, 10.0],
                         [10.0, 10.0, 10.0, 10.0, 10.0],
                         [5.0,  5.0,  8.0,  8.0, 10.0] ]
knots = ([0, 0, 0, 1/3, 2/3, 1, 1, 1], [0, 0, 0, 1/3, 2/3, 1, 1, 1])
srf = nrbmak(cp_sur, knots)
ut = list(np.linspace(0, 1, 5))
vt = list(np.linspace(0, 1, 5))
tt = (ut, vt)
p = nrbeval(srf, tt)
for i in range(5):
    print('p [:, :, ', i, '] = ', p[:, :, i])
print(np.shape(p))
'''
