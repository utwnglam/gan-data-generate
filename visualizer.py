import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
import sys
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

RESO = 40
RATIO = 1
TOTAL = RESO * RATIO
target_trans = 0
#
#  OPEN AND CONVERT 2D PNG TO 3D VOXEL ARRAY
#
if len(sys.argv) == 2:
    target_trans = int(sys.argv[1])
if len(sys.argv) > 2:
    print("USAGE: python visualizer.py [target_transparency]")

img = Image.open('result/00035-sgan-custom-256voxel40x40-4gpu004645.png')
data = np.array(img)
data = np.resize(data, (TOTAL, TOTAL, TOTAL, 3))
#  -----------------------------------------
#    UNCOMMENT IT IF YOU HAVE ENLARGED
#  -----------------------------------------
# data = data[::RATIO, ::RATIO, ::RATIO, 0:]

#
#  SEE THE INSIDE OF THE OBJECT WHETHER IT IS SOLID OR NOT
#
if(len(sys.argv) == 2):
    cube = np.zeros((RESO, RESO, RESO), dtype=bool)
    colors = np.divide(data, 255)
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


#
#  CHECKING FROM 128 TO 192 LEVEL
#
if(len(sys.argv) == 1):
    cube = np.zeros((RESO, RESO, RESO), dtype=bool)
    for CutOff in range(240, 253, 5):
        transparent = np.array([CutOff, CutOff, CutOff])

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                for k in range(data.shape[2]):
                    # it is TRUE when all value in the compare result array is TRUE
                    if np.all(data[i][j][k] <= transparent):
                        cube[i][j][k] = True

        colors = np.divide(data, 255)

        #
        #  PLOTTING GRAPH TO SEE VOXEL
        #
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(cube, facecolors=colors, edgecolor='grey')

        if not os.path.exists('ViewResult'):
            os.makedirs('ViewResult')
        plt.savefig('ViewResult/view_' + str(CutOff) + '.png')
        cube = np.zeros((RESO, RESO, RESO), dtype=bool)     # resetting the whole cube array


# for count in range(101):
#     transparent = np.array([0.0 + count * 0.01, 0.0 + count * 0.01, 0.0 + count * 0.01])
#     for i in range(colors.shape[0]):
#         for j in range(colors.shape[1]):
#             for k in range(colors.shape[2]):
#                 if colors[i][j][k][0] < transparent[0] and colors[i][j][k][1] < transparent[1] and \
#                         colors[i][j][k][2] < transparent[2]:
#                     cube[i][j][k] = True
#
#     #
#     #  PLOTTING GRAPH TO SEE VOXEL
#     #
#     fig = plt.figure()
#     ax = fig.gca(projection='3d')
#     ax.voxels(cube, facecolors=colors, edgecolor='grey')
#     plt.savefig('ViewResult/view_' + str(count) + '.png')
#     # plt.show()
#
#     cube = np.zeros((RESO, RESO, RESO), dtype=bool)     # resetting the whole cube array
