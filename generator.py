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


def version_one():
    RESO = 30
    RATIO = 3
    TOTAL = RESO * RATIO
    ADDITION = (1024 * 1024) - (TOTAL * TOTAL * TOTAL)
    LOOP = 0

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


#####################################
#   GENERATE 3D DATA SET version 2
#####################################

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
    method = ''
    color_or_not = False

    if len(sys.argv) > 3:
        loop = int(sys.argv[1])
        method = sys.argv[2]
        if sys.argv[3] == 'yes':
            color_or_not = True
        elif sys.argv[3] == 'no':
            color_or_not = False
    else:
        print('#\n#   USAGE: python generator.py [Number_of_png] [axis_type] [need_color_or_not]\n' +
              '#   * ALL ARGV IS COMPULSORY.\n#')

    for iteration in range(loop):
        #
        #  RANDOM GENERATE THE LENGTH OF CUBE
        #
        x, y, z = np.indices((Space, Space, Space))

        if method == 'len':
            length = random.randrange(10, 20 + 1)
            print(iteration, length)
            cube = (x >= 10) & (x < (length + 10)) \
                & (y >= 10) & (y < (length + 10)) \
                & (z >= 10) & (z < (length + 10))
        elif method == 'x':
            x_axis = random.randrange(0, 20)
            print(iteration, x_axis)
            cube = (x >= x_axis) & (x < (20 + x_axis)) \
                & (y >= 10) & (y < (20 + 10)) \
                & (z >= 10) & (z < (20 + 10))
        elif method == 'y':
            y_axis = random.randrange(0, 20)
            print(iteration, y_axis)
            cube = (x >= 10) & (x < (20 + 10)) \
                & (y >= y_axis) & (y < (20 + y_axis)) \
                & (z >= 10) & (z < (20 + 10))
        elif method == 'z':
            z_axis = random.randrange(0, 20)
            print(iteration, z_axis)
            cube = (x >= 10) & (x < (20 + 10)) \
                & (y >= 10) & (y < (20 + 10)) \
                & (z >= z_axis) & (z < (20 + z_axis))
        elif method == 'fix':
            cube = (x >= 10) & (x < (20 + 10)) \
                & (y >= 10) & (y < (20 + 10)) \
                & (z >= 10) & (z < (20 + 10))
        elif method == 'xyz':
            x_axis = random.randrange(0, 20)
            y_axis = random.randrange(0, 20)
            z_axis = random.randrange(0, 20)
            cube = (x >= x_axis) & (x < (20 + x_axis)) \
                & (y >= y_axis) & (y < (20 + y_axis)) \
                & (z >= z_axis) & (z < (20 + z_axis))

        colors = np.ones(cube.shape + (3,))  # set all the other empty voxel into transparent
        colors = np.multiply(colors, 255)

        #
        #   COLOUR SAMPLE
        #
        if color_or_not:
            sequence = [0, 32, 64, 96, 128]
            surface = (random.choice(sequence), random.choice(sequence), random.choice(sequence))
            print(iteration, surface)
            colors[cube, :] = surface
        else:
            colors[cube, :] = (0, 0, 0)

        #
        #   TRANSLATING 3D VOXEL TO 2D IMAGE
        #
        convert = colors.reshape((-1, 3))
        convert = np.vstack([convert, np.full(((imgLength * imgLength) - (Space * Space * Space), 3), 255)])
        output = convert.reshape((imgLength, imgLength, 3))

        output = output.repeat(Ratio, axis=0)  # enlarge the size of array by ratio
        output = output.repeat(Ratio, axis=1)
        output = np.uint8(output)  # change it back to integer format

        #
        #  OUTPUT
        #
        folder_name = 'space' + str(Space) + '_ratio' + str(Ratio) + '_method-' + method
        if color_or_not:
            folder_name = folder_name + '_withColor'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        new = Image.fromarray(output)
        new.save(folder_name + '/output_' + str(iteration) + ".png")


if __name__ == "__main__":
    main()
