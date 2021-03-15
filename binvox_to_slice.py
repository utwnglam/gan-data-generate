import glob
import binvox_rw
import os
import random

from PIL import Image
import numpy as np
import argparse

SPACE = 64
ROW_GRID = 8
COL_GRID = 8


def make_2D_grid_from_binvox(binvox_2D_grid, num):
    RGB_2d_grid = []
    insert_row = []

    img = Image.open('fine-tuned/' + str(num) + '.jpg')
    img_data = np.array(img)

    for row_index in range(binvox_2D_grid.shape[0]):
        for col_index in range(binvox_2D_grid.shape[1]):
            if binvox_2D_grid[row_index][col_index]:
                temp = img_data[row_index][col_index] // 2
                if num:
                    insert_row.append(temp)
                else:
                    insert_row.append([0, 0, 0])
            else:
                insert_row.append([255, 255, 255])
        RGB_2d_grid.append(insert_row)
        insert_row = []
    return np.array(RGB_2d_grid)


def make_2D_grid_flatten(args):
    file_list = glob.glob('voxel_result/*.binvox')

    for file in file_list:
        base = os.path.basename(file)
        print(base)
        base = os.path.splitext(base)[0]
        temp = random.randint(1, 50)

        if os.path.exists('ViewResult/new/' + base + '.png'):
            continue

        with open(file, 'rb') as f:
            model = binvox_rw.read_as_3d_array(f)
        canvas = Image.new('RGB', ((SPACE * ROW_GRID), (SPACE * COL_GRID)), 'white')
        # if not os.path.exists('OUTPUT'):
        #     os.makedirs('OUTPUT')

        count = 0
        for z_level in reversed(range(model.data.shape[2])):
            row_index = count//ROW_GRID
            col_index = count - row_index * ROW_GRID
            current_2D_gird = make_2D_grid_from_binvox(model.data[:, :, z_level], temp)
            current_2D_gird = np.uint8(current_2D_gird)
            canvas.paste(Image.fromarray(current_2D_gird, 'RGB'), (col_index * SPACE, row_index * SPACE))
            count += 1
        canvas.save('ViewResult/new/' + base + '.png')


def make_2D_grid_Hilbert(args):
    mapping = [
        [1 ,2 ,15,16,17,20,21,22],
        [4 ,3 ,14,13,18,19,24,23],
        [5 ,8 ,9 ,12,31,30,25,26],
        [6 ,7 ,10,11,32,29,28,27],
        [59,58,55,54,33,36,37,38],
        [60,57,56,53,34,35,40,39],
        [61,62,51,52,47,46,41,42],
        [64,63,50,49,48,45,44,43],
    ]
    mapping = np.array(mapping)
    file_list = glob.glob('../process_data/ShapeNetCore.v2/Collection/table_FirstSet_OnlyBinvox/*.binvox')
    # file_list = glob.glob(args.folder + '/*.binvox')

    for file in file_list:
        base = os.path.basename(file)
        print(base)
        base = os.path.splitext(base)[0]
        temp = random.randint(1, 50)

        with open(file, 'rb') as f:
            model = binvox_rw.read_as_3d_array(f)
        canvas = Image.new('RGB', ((SPACE * ROW_GRID), (SPACE * COL_GRID)), 'white')
        # if not os.path.exists('OUTPUT'):
        #     os.makedirs('OUTPUT')

        count = 1
        for z_level in reversed(range(model.data.shape[2])):
            row_index, col_index = np.where(mapping == count)
            current_2D_gird = make_2D_grid_from_binvox(model.data[:, :, z_level], temp)
            current_2D_gird = np.uint8(current_2D_gird)
            canvas.paste(Image.fromarray(current_2D_gird, 'RGB'), (col_index * SPACE, row_index * SPACE))
            count += 1
        canvas.save('ViewResult/new/' + base + '.png')


def make_2D_grid_professor(args):
    file_list = glob.glob(args.folder + '/*.binvox')
    for file in file_list:
        base = os.path.basename(file)
        print(base)
        base = os.path.splitext(base)[0]
        with open(file, 'rb') as f:
            model = binvox_rw.read_as_3d_array(f)
        canvas = Image.new('RGB', ((SPACE * ROW_GRID * 2), (SPACE * COL_GRID * 2)), 'white')
        if not os.path.exists('OUTPUT'):
            os.makedirs('OUTPUT')
        count = 0
        for level in reversed(range(model.data.shape[2])):
            row_index = count//ROW_GRID
            col_index = count - row_index * ROW_GRID
            current_2D_gird_x_axis = make_2D_grid_from_binvox(model.data[level, :, :], 0)
            current_2D_gird_y_axis = make_2D_grid_from_binvox(model.data[:, level, :], 0)
            current_2D_gird_z_axis = make_2D_grid_from_binvox(model.data[:, :, level], 0)
            current_2D_gird_x_axis = np.uint8(current_2D_gird_x_axis)
            current_2D_gird_y_axis = np.uint8(current_2D_gird_y_axis)
            current_2D_gird_z_axis = np.uint8(current_2D_gird_z_axis)
            canvas.paste(Image.fromarray(current_2D_gird_x_axis, 'RGB'), (col_index * SPACE,row_index * SPACE))
            canvas.paste(Image.fromarray(current_2D_gird_y_axis, 'RGB'), (col_index * SPACE,row_index * SPACE + ROW_GRID * SPACE))
            canvas.paste(Image.fromarray(current_2D_gird_z_axis, 'RGB'), (col_index * SPACE + SPACE * COL_GRID,row_index * SPACE))
            count += 1
        canvas.save('OUTPUT/' + base + '.png')


def make_2D_grid_Hilbert_and_professor(args):
    mapping = [
        [1 ,2 ,15,16,17,20,21,22],
        [4 ,3 ,14,13,18,19,24,23],
        [5 ,8 ,9 ,12,31,30,25,26],
        [6 ,7 ,10,11,32,29,28,27],
        [59,58,55,54,33,36,37,38],
        [60,57,56,53,34,35,40,39],
        [61,62,51,52,47,46,41,42],
        [64,63,50,49,48,45,44,43],
    ]
    mapping = np.array(mapping)
    file_list = glob.glob(args.folder + '/*.binvox')
    for file in file_list:
        base = os.path.basename(file)
        print(base)
        base = os.path.splitext(base)[0]
        with open(file, 'rb') as f:
            model = binvox_rw.read_as_3d_array(f)
        canvas = Image.new('RGB', ((SPACE * ROW_GRID * 2), (SPACE * COL_GRID * 2)), 'white')
        if not os.path.exists('OUTPUT'):
            os.makedirs('OUTPUT')
        count = 1
        for level in reversed(range(model.data.shape[2])):
            row_index, col_index = np.where(mapping == count)
            current_2D_gird_x_axis = make_2D_grid_from_binvox(model.data[level, :, :], 0)
            current_2D_gird_y_axis = make_2D_grid_from_binvox(model.data[:, level, :], 0)
            current_2D_gird_z_axis = make_2D_grid_from_binvox(model.data[:, :, level], 0)
            current_2D_gird_x_axis = np.uint8(current_2D_gird_x_axis)
            current_2D_gird_y_axis = np.uint8(current_2D_gird_y_axis)
            current_2D_gird_z_axis = np.uint8(current_2D_gird_z_axis)
            canvas.paste(Image.fromarray(current_2D_gird_x_axis, 'RGB'), (col_index * SPACE,row_index * SPACE))
            canvas.paste(Image.fromarray(current_2D_gird_y_axis, 'RGB'), (col_index * SPACE,row_index * SPACE + ROW_GRID * SPACE))
            canvas.paste(Image.fromarray(current_2D_gird_z_axis, 'RGB'), (col_index * SPACE + SPACE * COL_GRID,row_index * SPACE))
            count += 1
        canvas.save('OUTPUT/' + base + '.png')


method_dict = {
    "slice": make_2D_grid_flatten,
    "hilbert": make_2D_grid_Hilbert,
    "professor": make_2D_grid_professor,
    "hilbert_professor": make_2D_grid_Hilbert_and_professor
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=str, help='enter \'slice\'/ \'hilbert\' \'professor\' \'hilbert_professor\'')
    # parser.add_argument('folder', type=str, help='enter the target folder to scale/ convert to slice')
    args = parser.parse_args()
    method_dict[args.mode](args)


if __name__ == "__main__":
    main()
