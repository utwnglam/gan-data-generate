import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import random
import os
import sys
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

RESO = 30
RATIO = 3
TOTAL = RESO * RATIO
ADDITION = (1024 * 1024) - (TOTAL * TOTAL * TOTAL)
direction = None
LOOP = 0

if len(sys.argv) > 1:
    direction = sys.argv[1]
    if len(sys.argv) > 2:
        LOOP = int(sys.argv[2])
else:
    print("argv[1] = \'-g3\' / \'-g2\' / \'-v\'")
    print('-g3: generate png which represent 3D voxel cube\n-g2: generate png which there is a 2D square')
    print('-v: visualizer - under construction')
    print('argv[2] for \'-g3\' and \'-g2\': NUMBER of png you would like to generate')

if direction is None:
    pass

elif direction == '-g3':   # g stands for generator
    for iteration in range(LOOP):
        #
        # RANDOM GENERATOR OF CUBE
        #
        x, y, z = np.indices((RESO, RESO, RESO))
        range_up = random.randint(5, 10)
        range_down = random.randint(20, 25)
        print(range_up, range_down, iteration)
        cube = (x >= range_up) & (x < range_down) & (y >= range_up) & (y < range_down) & (z >= range_up) & (
                    z < range_down)

        colors = np.ones(cube.shape + (3,))  # set all the other empty voxel into transparent
        colors[cube, :] = (0, 0, 0)

        #
        # TRANSLATING 3D VOXEL TO 2D IMAGE
        #
        convert = colors
        for i in range(convert.shape[0]):
            for j in range(convert.shape[1]):
                convert[i][j] = convert[i][j] * 255

        convert = convert.repeat(RATIO, axis=0)  # enlarge the size of array by ratio
        convert = convert.repeat(RATIO, axis=1)
        convert = convert.repeat(RATIO, axis=2)

        output = convert.reshape((-1, 3))
        output = np.vstack([output, np.full((ADDITION, 3), 255)])
        output = output.reshape((1024, 1024, 3))
        output = np.uint8(output)  # change it back to integer format

        #
        # OUTPUT
        #
        if not os.path.exists('result'):
            os.makedirs('result')
        new = Image.fromarray(output)
        new.save('result/output_' + str(iteration) + ".png")

elif direction == '-g2':   # g stands for generator
    for iteration in range(LOOP):
        #
        # RANDOM GENERATE A CENTRE POSITION
        #
        square = np.zeros((1024, 1024, 3))
        centre_x = random.randrange(1, 1022)
        centre_y = random.randrange(1, 1022)
        smallest = min(centre_x, centre_y, (1023-centre_x), (1023-centre_y))
        length = random.randrange(1, smallest)

        print(iteration, centre_x, centre_y, length)

        # set the desired pixel into red
        square[(centre_x-length):(centre_x+length+1), (centre_y-length):(centre_y+length+1), :] = [1, 0, 0]

        #
        # TRANSLATING THE ARRAY INTO PNG FORMAT
        #
        for i in range(1024):
            square[i] = square[i] * 255
        output = np.uint8(square)  # change it back to integer format

        #
        # OUTPUT
        #
        if not os.path.exists('result'):
            os.makedirs('result')
        new = Image.fromarray(output)
        new.save('result/output_' + str(iteration) + ".png")

#
# TRANSLATING 2D RESULT BACK TO 3D VOXEL FOR VISUALIZATION
#
elif direction == '-v':     # v stands for visualizer
    #
    # OPEN THE TARGET PNG
    #
    img = Image.open('result/output_0.png')
    data = np.array(img)

    #
    # CONVERT THE 2D PNG TO ARRAY THAT CAN BE REPRESENT BY VOXEL
    #
    data = np.resize(data, (TOTAL, TOTAL, TOTAL, 3))
    data = data[::3, ::3, ::3, 0:]
    colors = np.divide(data, 255)

    cube = np.zeros((RESO, RESO, RESO), dtype=bool)
    transparent = np.array([1, 1, 1])

    for i in range(colors.shape[0]):
        for j in range(colors.shape[1]):
            for k in range(colors.shape[2]):
                if not np.array_equal(colors[i][j][k], transparent):
                    cube[i][j][k] = True

    #
    # PLOTTING THE GRAPH TO MAKE SURE VOXEL IS NORMAL
    #
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.voxels(cube, facecolors=colors, edgecolor='grey')
    plt.savefig('foo.png')
    plt.show()
