import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import os
import sys
import glob

RESO = 40
RATIO = 4
TOTAL = RESO * RATIO


def method2_range100():
    img = Image.open('result/00035-sgan-custom-256voxel40x40-4gpu004705.png')
    data = np.array(img)
    colors = np.resize(data, (TOTAL, TOTAL, TOTAL, 3))
    #  -----------------------------------------
    #    UNCOMMENT IT IF YOU HAVE ENLARGED
    #  -----------------------------------------
    # data = data[::RATIO, ::RATIO, ::RATIO, 0:]
    cube = np.zeros((RESO, RESO, RESO), dtype=bool)

    for count in range(101):
        transparent = np.array([0.0 + count * 0.01, 0.0 + count * 0.01, 0.0 + count * 0.01])
        for i in range(colors.shape[0]):
            for j in range(colors.shape[1]):
                for k in range(colors.shape[2]):
                    if colors[i][j][k][0] < transparent[0] and colors[i][j][k][1] < transparent[1] and \
                            colors[i][j][k][2] < transparent[2]:
                        cube[i][j][k] = True

        #
        #  PLOTTING GRAPH TO SEE VOXEL
        #
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(cube, facecolors=colors, edgecolor='grey')
        plt.savefig('ViewResult/view_' + str(count) + '.png')
        # plt.show()

        cube = np.zeros((RESO, RESO, RESO), dtype=bool)     # resetting the whole cube array


def method2_range255():
    img = Image.open('result/00035-sgan-custom-256voxel40x40-4gpu004705.png')
    data = np.array(img)
    data = np.resize(data, (TOTAL, TOTAL, TOTAL, 3))
    #  -----------------------------------------
    #    UNCOMMENT IT IF YOU HAVE ENLARGED
    #  -----------------------------------------
    # data = data[::RATIO, ::RATIO, ::RATIO, 0:]
    cube = np.zeros((RESO, RESO, RESO), dtype=bool)

    #
    #  CHECKING FROM CERTAIN LEVEL
    #
    for CutOff in range(250, 253, 10):
        transparent = np.array([CutOff, CutOff, CutOff])
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                for k in range(data.shape[2]):
                    # it is TRUE when all value in the compare result array is TRUE
                    if np.all(data[i][j][k] <= transparent):
                        cube[i][j][k] = True

        # colors = np.divide(data, 255)

        #
        #  PLOTTING GRAPH TO SEE VOXEL
        #
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(cube, facecolors=data, edgecolor='grey')

        if not os.path.exists('ViewResult'):
            os.makedirs('ViewResult')
        plt.savefig('ViewResult/view_' + str(CutOff) + '.png')
        # plt.show()
        cube = np.zeros((RESO, RESO, RESO), dtype=bool)  # resetting the whole cube array


def main():
    file_list = []
    folder_name = ''

    if len(sys.argv) > 1:
        folder_name = sys.argv[1]
        file_list = glob.glob('voxel_result/*' + folder_name + '*.png')
        print(file_list)
    else:
        print('#\n#\n#   Please input the target folder as argv[1].\n#\n#')

    for file in file_list:
        #
        #  OPEN AND CONVERT 2D PNG TO 3D VOXEL ARRAY
        #
        img = Image.open(file)
        data = np.array(img)
        data = data[::RATIO, ::RATIO, 0:]
        data = np.resize(data, (RESO, RESO, RESO, 3))

        #
        #  CHECKING FROM 128 TO 192 LEVEL
        #
        cube = np.zeros((RESO, RESO, RESO), dtype=bool)
        #  ------------------------------------------------
        #    UNCOMMENT IF YOU HAVE TO LOOP FOR THE CUTOFF
        #  ------------------------------------------------
        # for CutOff in range(250, 253, 10):
        CutOff = 245
        transparent = np.array([CutOff, CutOff, CutOff])

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                for k in range(data.shape[2]):
                    # it is TRUE when all value in the compare result array is TRUE
                    if np.all(data[i][j][k] <= transparent):
                        cube[i][j][k] = True

        # colors = np.divide(data, 255)

        #
        #  PLOTTING GRAPH TO SEE VOXEL
        #
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(cube, facecolors=data, edgecolor='grey')

        if not os.path.exists('ViewResult'):
            os.makedirs('ViewResult')
        plt.savefig('ViewResult/view' + str(CutOff) + '_' + file[13:])
        # plt.show()
        # cube = np.zeros((RESO, RESO, RESO), dtype=bool)  # resetting the whole cube array


if __name__ == "__main__":
    main()
