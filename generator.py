import numpy as np
from PIL import Image
import random
import os
import sys

Space = 40
Ratio = 4
TOTAL = Space * Ratio
imgLength = 256
ADDITION = (imgLength * imgLength) - (TOTAL * TOTAL * TOTAL)


##############################
#   GENERATE 3D DATA SET
##############################

# for iteration in range(LOOP):
#     #
#     #  RANDOM GENERATOR OF CUBE
#     #
#     x, y, z = np.indices((Space, Space, Space))
#     centre_x = random.randrange(0, (Space - 1))   # locate from [1-38] so no png contains no cube
#     centre_y = random.randrange(0, (Space - 1))
#     centre_z = random.randrange(0, (Space - 1))
#
#     smallest = min((Space - 1 - centre_x), (Space - 1 - centre_y), (Space - 1 - centre_z))
#     length = random.randrange(1, (smallest+1))
#     print(centre_x, centre_y, centre_z, length)
#
#     cube = (x >= centre_x) & (x < (centre_x+length)) \
#         & (y >= centre_y) & (y < (centre_y+length)) \
#         & (z >= centre_z) & (z < (centre_z+length))
#
#     colors = np.ones(cube.shape + (3,))  # set all the other empty voxel into transparent
#     colors[cube, :] = (0, 0, 0)
#
#     #
#     #  TRANSLATING 3D VOXEL TO 2D IMAGE
#     #
#     convert = np.multiply(colors, 255)
#     #  -----------------------------------------
#     #    UNCOMMENT IT IF YOU NEED TO ENLARGE
#     #  -----------------------------------------
#     # convert = convert.repeat(RATIO, axis=0)   # enlarge the size of array by ratio
#     # convert = convert.repeat(RATIO, axis=1)
#     # convert = convert.repeat(RATIO, axis=2)
#
#     output = convert.reshape((-1, 3))
#     output = np.vstack([output, np.full((ADDITION, 3), 255)])
#     output = output.reshape((imgLength, imgLength, 3))
#     output = np.uint8(output)   # change it back to integer format
#
#     #
#     #  OUTPUT
#     #
#     if not os.path.exists('dataSet'):
#         os.makedirs('dataSet')
#     new = Image.fromarray(output)
#     new.save('dataSet/output' + str(imgLength) + '_' + str(iteration) + ".png")

##############################
#   GENERATE 2D DATA SET
##############################

# for iteration in range(LOOP):
#     #
#     #  RANDOM GENERATE A CENTRE POSITION
#     #
#     square = np.zeros((1024, 1024, 3))
#     centre_x = random.randrange(1, 1022)
#     centre_y = random.randrange(1, 1022)
#     smallest = min(centre_x, centre_y, (1023-centre_x), (1023-centre_y))
#     length = random.randrange(1, smallest)
#     print(iteration, centre_x, centre_y, length)
#
#     # set the desired pixel into red
#     square[(centre_x-length):(centre_x+length+1), (centre_y-length):(centre_y+length+1), :] = [1, 0, 0]
#
#     #
#     #  TRANSLATING THE ARRAY INTO PNG FORMAT
#     #
#     square = np.multiply(square, 255)
#     output = np.uint8(square)
#
#     #
#     #  OUTPUT
#     #
#     if not os.path.exists('dataSet'):
#         os.makedirs('dataSet')
#     new = Image.fromarray(output)
#     new.save('dataSet/output_' + str(iteration) + ".png")


def main():
    loop = 0
    method = 'x-axis'

    if len(sys.argv) > 1:
        loop = int(sys.argv[1])
    else:
        print('#\n#\n# Please input a NUMBER as argv[1],\n' +
              '#   which is the NUMBER of png you would like to generate.\n#\n#')

    for iteration in range(loop):
        #
        #  RANDOM GENERATE THE LENGTH OF CUBE
        #
        x, y, z = np.indices((Space, Space, Space))

        if method is 'length':
            length = random.randrange(10, 20 + 1)
            print(iteration, length)
            cube = (x >= 10) & (x < (10 + length)) \
                & (y >= 10) & (y < (10 + length)) \
                & (z >= 10) & (z < (10 + length))
        elif method is 'x-axis':
            x_axis = random.randrange(0, 24 + 1)
            print(iteration, x_axis)
            cube = (x >= x_axis) & (x < (15 + x_axis)) \
                & (y >= 10) & (y < (15 + 10)) \
                & (z >= 10) & (z < (15 + 10))

        colors = np.ones(cube.shape + (3,))  # set all the other empty voxel into transparent
        colors[cube, :] = (0, 0, 0)

        #
        #  TRANSLATING 3D VOXEL TO 2D IMAGE
        #
        convert = np.multiply(colors, 255)
        convert = convert.reshape((-1, 3))
        convert = np.vstack([convert, np.full(((imgLength * imgLength) - (Space * Space * Space), 3), 255)])
        output = convert.reshape((imgLength, imgLength, 3))

        output = output.repeat(Ratio, axis=0)  # enlarge the size of array by ratio
        output = output.repeat(Ratio, axis=1)
        output = np.uint8(output)  # change it back to integer format

        #
        #  OUTPUT
        #
        folder_name = 'out1024_space' + str(Space) + '_ratio' + str(Ratio) + '_method-X-axis'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        new = Image.fromarray(output)
        new.save(folder_name + '/output_' + str(iteration) + ".png")


if __name__ == "__main__":
    main()
