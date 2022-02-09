# Autor: Yanpeng Mei
# Created at : 29.01.2022

import numpy as np
import pickle
from matplotlib import pyplot as plt
from a3_path import a3_path


with open('a2_parameters.txt', 'rb') as open1:
    temp1 = pickle.load(open1)
knots = temp1['knots']
tpl = temp1['tpl']
cp = temp1['cp']
step_xy = temp1['step_xy']

max_delta_cpX = (cp[0, -1, :] - cp[0, 0, :]).max()
max_delta_cpY = (cp[1, :, -1] - cp[1, :, 0]).max()
print('max_delta_cpX, max_delta_cpY', max_delta_cpX, max_delta_cpY)

delta_u = np.array(tpl[1:, 0] - tpl[0:-1, 0])
delta_v = np.array(tpl[1:, 1] - tpl[0:-1, 1])
print('delta_u, delta_v', delta_u, delta_v)

numP = (np.round(((max_delta_cpX * delta_u / step_xy)**2 + (max_delta_cpY * delta_v / step_xy)**2)**(1/2))).astype(int)
print('numP', numP, type(numP), type(numP[0]))

numS = tpl.shape[0] - 1
print('numS', numS, type(numS))

segType = (np.zeros((numS, 2))).astype(int)
for i in range(numS):
    if (delta_u[i] != 0 and delta_v[i] == 0):
        segType[i, 1]=1
    elif (delta_u[i] == 0 and delta_v[i] != 0):
        segType[i, 1]=2
print('segType', segType)

path = np.zeros((3, (np.sum(numP) - numS +1)))
print('path.shape', path.shape)

ut_path = list(np.linspace(tpl[0, 0], tpl[0 + 1, 0], numP[0]))
vt_path = list(np.linspace(0, 0, numP[0])+0.5)
print('ut_path, vt_path', ut_path, vt_path,type(ut_path),type(vt_path),len(ut_path),len(vt_path))

p_a3 = a3_path(cp)
print('p_a3.shape', p_a3.shape)
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(p_a3[0, :], p_a3[1, :], p_a3[2, :])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()