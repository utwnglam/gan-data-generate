import binvox_rw
import numpy as np
import argparse
import PIL.Image

from pyface.api import GUI
from mayavi import mlab

import gpu_accelerator

def boolean_grid2D_to_rgb_grid2D(boolean_grid2D):
    RGB_2d_grid = []
    insert_row = []
    for row_index in range(boolean_grid2D.shape[0]):
        for col_index in range(boolean_grid2D.shape[1]):
            if boolean_grid2D[row_index][col_index]:
                insert_row.append([0, 0, 0])
            else:
                insert_row.append([255, 255, 255])
        RGB_2d_grid.append(insert_row)
        insert_row = []
    return np.array(RGB_2d_grid)


def binvox_to_rgb_3Darray(binvox):
    boolean_table = binvox_to_boolean_table(binvox)
    x, y, z = boolean_table.shape
    rgb_3Darray = np.zeros((x, y, z, 3))
    for i in range(x):
        for j in range(y):
            for k in range(z):
                if(boolean_table[i][j][k] == False):
                    rgb_3Darray[i][j][k] = [255, 255, 255]
    return rgb_3Darray

def boolean_table_to_rgb_2Darray(boolean_table, mode = 'flatten', space = 64, grid_length = 8):
    if(mode == 'flatten'):
        rgb_2Darray = np.zeros((space * grid_length, space * grid_length, 3))
        x_length, y_length, z_length = boolean_table.shape
        count = 0
        for z_level in reversed(range(z_length)):
            rgb_grid2D = boolean_grid2D_to_rgb_grid2D(boolean_table[:,:,z_level])
            row_index = count // grid_length
            col_index = count - row_index * grid_length
            rgb_2Darray[row_index * space : space * (row_index + 1), col_index * space : space * (col_index + 1)] = rgb_grid2D
            count += 1

    elif(mode == 'Hilbert'):
        rgb_2Darray = np.zeros((space * grid_length, space * grid_length, 3))
        mapping = np.array([
        [1 ,2 ,15,16,17,20,21,22],
        [4 ,3 ,14,13,18,19,24,23],
        [5 ,8 ,9 ,12,31,30,25,26],
        [6 ,7 ,10,11,32,29,28,27],
        [59,58,55,54,33,36,37,38],
        [60,57,56,53,34,35,40,39],
        [61,62,51,52,47,46,41,42],
        [64,63,50,49,48,45,44,43],
    ])
        x_length, y_length, z_length = boolean_table.shape
        count = 1
        for z_level in reversed(range(z_length)):
            rgb_grid2D = boolean_grid2D_to_rgb_grid2D(boolean_table[:,:,z_level])
            row_index, col_index = np.where(mapping == count)
            row_index = row_index[0]
            col_index = col_index[0]
            rgb_2Darray[row_index * space : space * (row_index + 1), col_index * space : space * (col_index + 1)] = rgb_grid2D
            count += 1
    elif(mode == 'professor'):
        rgb_2Darray = np.full((space * grid_length * 2, space * grid_length * 2, 3), 255)
        x_length, y_length, z_length = boolean_table.shape
        count = 0
        for level in reversed(range(z_length)):
            row_index = count // grid_length
            col_index = count - row_index * grid_length
            current_2D_gird_x_axis = boolean_grid2D_to_rgb_grid2D(boolean_table[level,:,:])
            current_2D_gird_y_axis = boolean_grid2D_to_rgb_grid2D(boolean_table[:,level,:])
            current_2D_gird_z_axis = boolean_grid2D_to_rgb_grid2D(boolean_table[:,:,level])
            rgb_2Darray[row_index * space : (row_index + 1) * space, col_index * space : (col_index + 1) * space] = current_2D_gird_x_axis
            rgb_2Darray[row_index * space : (row_index + 1) * space, col_index * space + grid_length * space : (col_index + 1) * space + grid_length * space] = current_2D_gird_y_axis
            rgb_2Darray[row_index * space + grid_length * space : (row_index + 1) * space + grid_length * space, col_index * space : (col_index + 1) * space] = current_2D_gird_z_axis
            count += 1
    elif(mode == 'Hilbert_and_professor'):
        mapping = np.array([
        [1 ,2 ,15,16,17,20,21,22],
        [4 ,3 ,14,13,18,19,24,23],
        [5 ,8 ,9 ,12,31,30,25,26],
        [6 ,7 ,10,11,32,29,28,27],
        [59,58,55,54,33,36,37,38],
        [60,57,56,53,34,35,40,39],
        [61,62,51,52,47,46,41,42],
        [64,63,50,49,48,45,44,43],
    ])
        rgb_2Darray = np.full((space * grid_length * 2, space * grid_length * 2, 3), 255)
        x_length, y_length, z_length = boolean_table.shape
        count = 1
        for level in reversed(range(z_length)):
            row_index, col_index = np.where(mapping == count)
            row_index = row_index[0]
            col_index = col_index[0]
            current_2D_gird_x_axis = boolean_grid2D_to_rgb_grid2D(boolean_table[level,:,:])
            current_2D_gird_y_axis = boolean_grid2D_to_rgb_grid2D(boolean_table[:,level,:])
            current_2D_gird_z_axis = boolean_grid2D_to_rgb_grid2D(boolean_table[:,:,level])
            rgb_2Darray[row_index * space : (row_index + 1) * space, col_index * space : (col_index + 1) * space] = current_2D_gird_x_axis
            rgb_2Darray[row_index * space : (row_index + 1) * space, col_index * space + grid_length * space : (col_index + 1) * space + grid_length * space] = current_2D_gird_y_axis
            rgb_2Darray[row_index * space + grid_length * space : (row_index + 1) * space + grid_length * space, col_index * space : (col_index + 1) * space] = current_2D_gird_z_axis
            count += 1
    return rgb_2Darray

def binvox_to_rgb_2Darray(binvox, mode = 'flatten'):
    boolean_table = binvox_to_boolean_table(binvox)
    rgb_2Darray = boolean_table_to_rgb_2Darray(boolean_table, mode)
    return rgb_2Darray


def binvox_to_boolean_table(binvox):
    with open(binvox, 'rb') as f:
        model = binvox_rw.read_as_3d_array(f)
    return model.data

def rgb_2Darray_to_rgb_3Darray_and_boolean_table(rgb_2Darray, mode = 'flatten', grid_property = (64, 64, 8, 8), space = 64, cutoff = 128):
    row_grid_size, col_grid_size, num_of_row_grid, num_of_col_grid = grid_property
    mapping = np.array([
        [1 ,2 ,15,16,17,20,21,22],
        [4 ,3 ,14,13,18,19,24,23],
        [5 ,8 ,9 ,12,31,30,25,26],
        [6 ,7 ,10,11,32,29,28,27],
        [59,58,55,54,33,36,37,38],
        [60,57,56,53,34,35,40,39],
        [61,62,51,52,47,46,41,42],
        [64,63,50,49,48,45,44,43],
    ])
    if(mode == 'flatten'):
        rgb_3Darray, boolean_table = gpu_accelerator.boolean_table_to_rgb_2Darray_flatten(rgb_2Darray, cutoff)
    elif(mode == 'Hilbert'):
        rgb_3Darray, boolean_table = gpu_accelerator.boolean_table_to_rgb_2Darray_Hilbert(rgb_2Darray, cutoff, mapping)
    elif(mode == 'professor'):
        rgb_3Darray, boolean_table = gpu_accelerator.boolean_table_to_rgb_2Darray_professor(rgb_2Darray, cutoff)
    elif(mode == 'Hilbert_and_professor'):
        rgb_3Darray, boolean_table = gpu_accelerator.boolean_table_to_rgb_2Darray_Hilbert_and_professor(rgb_2Darray, cutoff, mapping)
    return rgb_3Darray, boolean_table


def rgb_2Darray_to_rgb_2Darray():
    pass


def rgb_3Darray_to_boolean_table(rgb_3Darray, cutoff):
    x, y, z = rgb_3Darray.shape
    boolean_table = np.zeros((x, y, z, 3))
    for i in range(x):
        for j in range(y):
            for k in range(z):
                if(np.all(rgb_3Darray[i][j][k] < cutoff)):
                    boolean_table[i][j][k] = True
    return boolean_table


def rgb_3Darray_and_boolean_table_to_3Dpng(rgb_3Darray, boolean_table, space=64):
    fig = mlab.figure(1, size=(512, 555))
    xx, yy, zz = np.where(boolean_table == 1)
    s = np.arange(len(xx))
    lut = np.zeros((len(xx), 4))
    for row in s:
        temp = np.append((rgb_3Darray[xx[row]][yy[row]][zz[row]] + (256 - 208)), 255)
        lut[row, :] = temp
    currfig = mlab.points3d(xx, yy, zz, s,
                            scale_mode='none',
                            mode="cube",
                            scale_factor=1)
    currfig.module_manager.scalar_lut_manager.lut.number_of_colors = len(s)
    currfig.module_manager.scalar_lut_manager.lut.table = lut

    mlab.view(azimuth=225, elevation=70, distance=140, focalpoint=(32, 32, 32))
    fig.scene.camera.parallel_projection = True
    fig.scene.camera.parallel_scale = 65  # smaller the number, greater zoom
    mlab.axes(figure=fig, nb_labels=5, extent=(0, space, 0, space, 0, space))
    mlab.outline(extent=(0, space, 0, space, 0, space))

    GUI().process_events()
    imgmap_RGB = mlab.screenshot(figure=fig, mode='rgb', antialiased=True)
    img_RGB = np.uint8(imgmap_RGB)
    # img_RGB = PIL.Image.fromarray(img_RGB)
    mlab.clf()
    return img_RGB

def generated_img_to_png_array(generated_img, mode = 'flatten'):
    generated_img_array = np.array(generated_img)
    rgb_3Darray, boolean_table = rgb_2Darray_to_rgb_3Darray_and_boolean_table(generated_img_array, mode)
    png_array = rgb_3Darray_and_boolean_table_to_3Dpng(rgb_3Darray, boolean_table)
    return png_array

def professor_judgement(xyz_result, choice=0):
    if(choice == 0):
        return np.any(xyz_result)
    elif(choice == 1):
        if(np.count_nonzero(xyz_result) >= 2):
            return True
        else:
            return False
    elif(choice == 2):
        return np.all(xyz_result)


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('binvox', type=str, help='path of binvox')
    # parser.add_argument('mode', type=str, help='enter \'flatten\'/ \'Hilbert\' \'professor\' \'Hilbert_and_professor\'')
    # args = parser.parse_args()
    # returned_thing = binvox_to_boolean_table(args.binvox)
    # returned_thing = boolean_table_to_rgb_2Darray(returned_thing, args.mode)
    # returned_thing = np.uint8(returned_thing)
    # returned_thing = PIL.Image.fromarray(returned_thing, 'RGB')
    # returned_thing.save("OUTPUT/testing.png")
    img = PIL.Image.open("INPUT/2d_seed0000.png")
    data = generated_img_to_png_array(img, 'Hilbert_and_professor')
    data = PIL.Image.fromarray(data)
    data.save('OUTPUT/test3.png')


if __name__ == "__main__":
    main()
