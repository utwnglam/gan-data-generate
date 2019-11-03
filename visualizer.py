import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
import sys
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

RESO = 30
RATIO = 3
TOTAL = RESO * RATIO
iteration = 0
target_trans = 0
if len(sys.argv) == 2:
    target_trans = int(sys.argv[1])
if len(sys.argv) > 2:
    print("USAGE: python visualizer.py [target_transparency]")
#
# OPEN THE TARGET PNG
#
img = Image.open('result/00008-sgan-voxel-30-black-4gpu009645.png')
data = np.array(img)
#
# CONVERT THE 2D PNG TO ARRAY THAT CAN BE REPRESENT BY VOXEL
#
if(len(data) == 256):
    data = data.repeat(4, axis=0)  # enlarge the size of array by ratio
    data = data.repeat(4, axis=1)

data = np.resize(data, (TOTAL, TOTAL, TOTAL, 3))
data = data[::3, ::3, ::3, 0:]
colors = np.divide(data, 255)
cube = np.zeros((RESO, RESO, RESO), dtype=bool)
if(len(sys.argv) == 2):
    transparent = np.array([target_trans * 0.01,target_trans * 0.01,target_trans * 0.01])
    for i in range(colors.shape[0]):
        for j in range(colors.shape[1]):
            for k in range(colors.shape[2]):
                if (colors[i][j][k][0] < transparent[0] and colors[i][j][k][1] < transparent[1] and colors[i][j][k][2] < transparent[2]):
                    cube[i][j][k] = True
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.voxels(cube, facecolors=colors, edgecolor='grey')
    plt.savefig('view_result/view' + '_test' +'original'+'.png')                
    for count in range(29):
        cube[29-count][:][:] = False
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(cube, facecolors=colors, edgecolor='grey')
        plt.savefig('view_result/view' + '_test' +str(count)+'.png')
if(len(sys.argv) == 1):
    for count in range(101):
        transparent = np.array([0.0 + count * 0.01, 0.0 + count * 0.01, 0.0 + count * 0.01])
        for i in range(colors.shape[0]):
            for j in range(colors.shape[1]):
                for k in range(colors.shape[2]):
                    if (colors[i][j][k][0] < transparent[0] and colors[i][j][k][1] < transparent[1] and colors[i][j][k][2] < transparent[2]):
                        cube[i][j][k] = True
        #
        # PLOTTING THE GRAPH TO MAKE SURE VOXEL IS NORMAL
        #
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(cube, facecolors=colors, edgecolor='grey')
        plt.savefig('view_result/view' + str(count) +'.png')
        #plt.show()
