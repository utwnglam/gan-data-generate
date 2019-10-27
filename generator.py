import numpy as np
from PIL import Image
import random
import os
import sys

RESO = 30
RATIO = 3
TOTAL = RESO * RATIO
ADDITION = (1024 * 1024) - (TOTAL * TOTAL * TOTAL)
LOOP = 0

if len(sys.argv) > 1:
    LOOP = int(sys.argv[1])
else:
    print('#\n#\n# Please input a NUMBER as argv[1],\n#   which is the NUMBER of png you would like to generate.\n#\n#')

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
    if not os.path.exists('dataSet'):
        os.makedirs('dataSet')
    new = Image.fromarray(output)
    new.save('dataSet/output_' + str(iteration) + ".png")

#
#   GENERATE 2D DATA SET
#

# for iteration in range(LOOP):
#     #
#     # RANDOM GENERATE A CENTRE POSITION
#     #
#     square = np.zeros((1024, 1024, 3))
#     centre_x = random.randrange(1, 1022)
#     centre_y = random.randrange(1, 1022)
#     smallest = min(centre_x, centre_y, (1023-centre_x), (1023-centre_y))
#     length = random.randrange(1, smallest)
#
#     print(iteration, centre_x, centre_y, length)
#
#     # set the desired pixel into red
#     square[(centre_x-length):(centre_x+length+1), (centre_y-length):(centre_y+length+1), :] = [1, 0, 0]
#
#     #
#     # TRANSLATING THE ARRAY INTO PNG FORMAT
#     #
#     for i in range(1024):
#         square[i] = square[i] * 255
#     output = np.uint8(square)  # change it back to integer format
#
#     #
#     # OUTPUT
#     #
#     if not os.path.exists('dataSet'):
#         os.makedirs('dataSet')
#     new = Image.fromarray(output)
#     new.save('dataSet/output_' + str(iteration) + ".png")
