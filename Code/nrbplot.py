# Autor: Yanpeng Mei
# Created at : 05.02.2022

'''
This function was written by me.
'numpy' and 'matplotlib' should be installed and imported !!!!!!
'''

'''
nrbplot:  Plot a surface or a iso-parametric curve(for non-iso--parametric curve, just use the existed function)

Meaning of the input:
nrb - Dictionary of NURBS curve, surface(see nrbmak)
subd - Number of evaluation points
for curve: type(subd) == 'int'
for surface: type(subd) == 'list', [npnts in u, npnts in v]
'''

import numpy as np
import matplotlib.pyplot as plt
from nrbeval import nrbeval


def nrbplot(nurbs, subd):
    order = nurbs['Order']
    if (order[0] < 2 and len(order) == 1) or (order[0] < 2 and len(order) == 1 and order[1]< 2):
        print('Warning! The plot with order smaller than 2 may not be correct')
    sorc = len(nurbs['Knots'])
    if sorc == 2:  # plot a NURBS surface
        tt = (list(np.linspace(0,1,subd[0])), list(np.linspace(0,1,subd[1])))
        p = nrbeval(nurbs, tt)
        ax3 = plt.axes(projection='3d')
        ax3.plot_surface(p[0, :, :], p[1, :, :], p[2, :, :],)
        ax3.set_xlabel('X')
        ax3.set_ylabel('Y')
        ax3.set_zlabel('Z')
        #plt.show()

    elif sorc==1: # plot a NURBS curve
        ut = (list(np.linspace(0, 1, subd)), )
        p = nrbeval(nurbs, ut)
        plt.plot(p[0, :], p[1, :])
        plt.xlabel('X')
        plt.ylabel('Y')
        #plt.show()

'''
# test 1
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
nrbplot(srf, [50, 25])
'''
'''
# test 2
cp_cur = np.asarray([[0.5, 1.5, 4.5, 3.0, 7.5, 6.0, 8.5],
                                  [3.0, 5.5, 5.5, 1.5, 1.5, 4.0, 4.5]])
knot = ([0, 0, 0, 1/4, 1/2, 3/4, 3/4, 1, 1, 1], )
crv = nrbmak(cp_cur, knot)
nrbplot(crv, 20)
'''
