# Autor: Yanpeng Mei
# Created at : 08.02.2022

'''
This is the main file of my thesis "Path optimization when interpolating in Numerical Controls"
This program was originally done in Matlab, but now I will rewrite part of it in Python out of interest.
This is just a short version. Please see my Matlab version for more information.
In Matlab version, i minimized the curvature of the tool path. This time i will try something new. I will minimize the length of the path.
And i will only consider the most common case, which means the iso-parametric path('u' or 'v' is constant)
There are also many other changes compared with the original Matlab version.

In my thesis, the whole tool path will be divided into many segments based on the Tuple
The tool path I am considering is a combination of many NURBS-curves(segments)
Optimization: minimizing the length of each NURBS-segment by adjusting the position of the control points of the original surface

List of functions:
'a3_path' get the tool path with given Tuple
'a4_length' get the length of the path
'a5_nonlcon1' is the non-linear constraint for the optimization, when the tolerance band is exactly defined(my method)
'a6_finerPath' get a finer tool path with given Tuple(more sampling points)
'a7_nonlcon2' is the non-linear constraint for the optimization, when the tolerance band is linearly defined(traditional way)
'''

import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.optimize import minimize
from nrbmak import nrbmak
from nrbplot import nrbplot
from a3_path import a3_path
from a4_length import a4_length
from a5_nonlcon1 import a5_nonlcon1
from a7_nonlcon2 import a7_nonlcon2
from a8_array2list import a8_array2list
from a10_tb_r4LTB import a10_tb_r4LTB


# 1. Create a NURBS-surface as the test surface
# In the following, "test surface/path" will be also called as "original surface/path" or "real surface/path"
# 1.1 define control points
# allocate multi-dimensional array of control points for NURBS-surface
# cp0   -   control points of the test surface
cp0 = np.zeros((3,6,3))
cp0[:, :, 0] = [ [ 0, 50,150,  250,  350,  400],
                     [ 0,   0,    0,      0,      0,      0],
                     [-5, 10, -20,    20,   -10,      5] ]

cp0[:, :, 1] = [ [ 0,   50,   150,  250,  350,  400],
                    [50,  50,     50,    50,    50,   50],
                   [-50, 100, -200,  200, -100,  50] ]

cp0[:, :, 2] = [ [ 0,   50,   150,  250,  350, 400],
                 [100, 100,   100,  100,  100, 100],
                    [-5,   10,    -20,    20,   -10,  5] ]

# In order to facilitate the subsequent optimization process, we need to convert the control points into a one-dimensional list
cp4opt0 = a8_array2list(cp0)


# 1.2 define knots
knots = ([0, 0, 0, 1/4, 2/4, 3/4, 1, 1, 1], [0, 0, 0, 1, 1, 1])


# 1.3 generate and plot the test NURBS-surface
# surf   -   test NURBS-surface
fig1 = plt.figure()
surf = nrbmak(cp0, knots)
nrbplot(surf, [100,50])



# 2. Input tuple(u,v), set parameters and get the test path
# 2.1 input tuple 'tpl'
# tpl   -   tuple is a n*2 matrix [u_i  v_i], n is the number of points in tuple
# input tpl with right order
# test
'''
tpl = np.array([[0.1,            0.1],
                        [0.9,            0.1],
                        [0.9,            0.9]])
'''
'''
tpl = np.array([[0.5,            0.1],
                        [0.5,            0.9]])
'''

# demo with a simple 2D case, to get a better plot
#'''
tpl = np.array([[0,     0.5],
                         [1,     0.5]])
#'''


# 2.2 define the radius of the rolerance band and step size when generating the path
# tb_r   -   radius of the rolerance band
# step_xy   -   step size in 3D-coordinate system when generating the path
tb_r = 4
step_xy = 2


# 2.3 get the number of sampling points and number of segments
# numP   -   number of sampling points
# numS   -   number of segments
# get the "range" of the surface by measuring the control points
# max_delta_cpX        maximum difference of x-coordinate of each row of control points
# max_delta_cpY        maximum difference of y-coordinate of each column of control points
max_delta_cpX = (cp0[0, -1, :] - cp0[0, 0, :]).max()
max_delta_cpY = (cp0[1, :, -1] - cp0[1, :, 0]).max()

delta_u = np.array(tpl[1:, 0] - tpl[0:-1, 0])
delta_v = np.array(tpl[1:, 1] - tpl[0:-1, 1])

numP = (np.round(((max_delta_cpX * delta_u / step_xy)**2 + (max_delta_cpY * delta_v / step_xy)**2)**(1/2))).astype(int)

numS = tpl.shape[0] - 1

# we will devide the segments in 2 types:
# type 1: iso-parametric segments with constant v
# type 2: iso-parametric segments with constant u
segType = (np.zeros((numS, 2))).astype(int)
for i in range(numS):
    if (delta_u[i] != 0 and delta_v[i] == 0):
        segType[i, 1]=1
    elif (delta_u[i] == 0 and delta_v[i] != 0):
        segType[i, 1]=2


# 2.4 save the parameters to a file
dict1 = {'cp0' : cp0, 'cp4opt0' : cp4opt0, 'knots' : knots, 'tpl' : tpl, 'tb_r' : tb_r, 'step_xy' : step_xy, 'numP' : numP, 'numS' : numS, 'segType' : segType}
fileHandle1 = open('a2_parameters.txt', 'wb')
pickle.dump(dict1, fileHandle1)
fileHandle1.close()

# how to read
# with open('a2_parameters.txt', 'rb') as open1:
#     temp1 = pickle.load(open1)
# cp0 = temp1['cp0']


# 2.5 generate and plot the original path
path = a3_path(cp4opt0)
plt.plot(path[0, :], path[1, :], path[2, :], c='r', linewidth = 5)
plt.title('test surface and test path')
plt.show()



# 3. Optimize the path and compare the results
# 3.1 opt1
constr1 = {'type' : 'eq', 'fun' : a5_nonlcon1}
lengthOpt1 = minimize(a4_length, cp4opt0, method = 'trust-constr', constraints=constr1, options={'xtol': 1e-03, 'gtol': 1e-03, 'barrier_tol': 1e-03, 'maxiter': 9000})
# print(lengthOpt1)
cp4opt1 = lengthOpt1.x
pathOpt1 = a3_path(cp4opt1)


# 3.2 opt2
tb_r4Ltb = a10_tb_r4LTB()
dict2 = {'tb_r4Ltb' : tb_r4Ltb}
fileHandle2 = open('a2_tb_r4Ltb.txt', 'wb')
pickle.dump(dict2, fileHandle2)
fileHandle2.close()

constr2 = {'type' : 'eq', 'fun' : a7_nonlcon2}
lengthOpt2 = minimize(a4_length, cp4opt0, method = 'trust-constr', constraints=constr2, options={'xtol': 1e-03, 'gtol': 1e-03, 'barrier_tol': 1e-03, 'maxiter': 9000})
# print(lengthOpt2)
cp4opt2 = lengthOpt2.x
pathOpt2 = a3_path(cp4opt2)


# 3.3 print the lengths
# length - length of the original path
# length1 - length of the optimized path, when the tolerance band is exactly defined
# length2 - length of the optimized path, when the tolerance band is linearly defined(traditional way)
length = a4_length(cp4opt0)
print('length = ', length)
length1 = a4_length(cp4opt1)
print('length with optimization method 1 = ', length1)
length2 = a4_length(cp4opt2)
print('length with optimization method 2 = ', length2)



# 4. Demonstration
# If the 'tpl' is not the third situation as in section 2.1, then this chapter should be changed
fig2 = plt.figure()
plt.plot(path[0, :], path[2, :], c='b', linewidth = 1, label='original')
plt.plot(pathOpt1[0, :], pathOpt1[2, :], c='r', linewidth = 1, label='opt1')
plt.plot(pathOpt2[0, :], pathOpt2[2, :], c='y', linewidth = 1, label='opt2')
plt.legend()
plt.axis('equal')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Original and optimized paths')
plt.show()
