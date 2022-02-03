# Autor: Yanpeng Mei
# Created at : 03.02.2022

'''
This function was written by me.
'numpy' should be installed and imported !!!!!!
'''

'''
nrbmak:  Construct the NURBS dictionary given the control points and the knots

Meaning of the input:
cp : Control points
    		    For a curve the control points are represented by a matrix of size (dim,nu). 
    		    For a surface a multidimensional array of size (dim,nu,nv).
    		    Where 
    		    nu is number of points along the parametric U direction,
    		    nv the number of points along the V direction,
    		    dim is the dimension. 
    		    Valid options are
    		    2 .... (x,y)        2D Cartesian coordinates
    		    3 .... (x,y,z)      3D Cartesian coordinates

knots : Non-decreasing knot sequence spanning the interval [0, 1]

type(CP) -  numpy array
type(Number), type(Order) - list
type(Knots) - tuple(knot of u, knot of v), the element of the tuple is list

Meaning of the output:
nurbs : Dictionary for representing a NURBS entity

NURBS dictionary:
Both curves and surfaces are represented by a dictionary.
Form   .... Type name 'B-NURBS'
DimCP    .... Dimension of the control points
NumCP .... Number of Control points
CP  .... Control Points
Order  .... Order of the spline
Knots  .... Knot sequence
Note: the control points are always converted and stored within the NURBS structure as 4D homogeneous coordinates.
A curve is always stored along the U direction, and the vknots element is an empty matrix. 
For a surface the spline order is a vector [du,dv] containing the order along the U and V directions respectively.
'''


import numpy as np


def nrbmak(cp, knots):
    nurbs = dict(Form = 'B-NURBS', DimCP = 4, Knots = knots)
    ncp = np.shape(cp)
    dim = ncp[0]

    if len(knots) == 2:   # constructing a surface
        nurbs['NumCP'] = ncp[1:3]
    elif len(knots) == 1:  # constructing a curve
        nurbs['NumCP'] = ncp[1]

    if dim == 3:    # constructing a surface
        temp1 = np.zeros((4, ncp[1], ncp[2]))
        temp1[3, :, :] = 1
        temp1[0:3, :, :] = cp
        nurbs['CP'] = temp1
    elif dim ==2:     # constructing a curve
        temp2 = np.zeros((4, ncp[1]))
        temp2[3, :] = 1
        temp2[0:2, :] = cp
        nurbs['CP'] = temp2

    uorder = len(knots[0]) - ncp[1]
    if len(knots) == 2:  # constructing a surface
        vorder = len(knots[1]) - ncp[2]
        nurbs['Order'] = [uorder, vorder]
    elif len(knots) == 1:   # constructing a curve
        nurbs['Order'] = [uorder]

    return nurbs


'''
# test 1
cp_cur = np.asarray([[0.5, 1.5, 4.5, 3.0, 7.5, 6.0, 8.5],
                                  [3.0, 5.5, 5.5, 1.5, 1.5, 4.0, 4.5]])
knot = ([0, 0, 0, 1/4, 1/2, 3/4, 3/4, 1, 1, 1], )
crv = nrbmak(cp_cur, knot)
print(crv)
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
print(srf)
'''
