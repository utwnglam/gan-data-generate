from numba import jit
import numpy as np

@jit(nopython=True)
def professor_judgement(xyz_result, choice):
    if(choice == 0):
        return np.any(xyz_result)
    elif(choice == 1):
        if(np.count_nonzero(xyz_result) >= 2):
            return True
        else:
            return False
    elif(choice == 2):
        return np.all(xyz_result)

@jit(nopython=True)
def boolean_table_to_rgb_2Darray_flatten(rgb_2Darray,cutoff):
    boolean_table = np.zeros((64, 64, 64))
    rgb_3Darray = np.zeros((64, 64, 64, 3))
    for i in range(8):
        for j in range(8):
            z_num = (7 - i) * 8 + (7 - j)
            for a in range(64):
                for b in range(64):
                    if np.all(rgb_2Darray[i * 64 + a][j * 64 + b] < cutoff):
                        boolean_table[a][b][z_num] = True
                        rgb_3Darray[a][b][z_num] = rgb_2Darray[i * 64 + a][j * 64 + b]
    
    return rgb_3Darray, boolean_table

@jit(nopython=True)
def boolean_table_to_rgb_2Darray_Hilbert(rgb_2Darray, cutoff, mapping):
    boolean_table = np.zeros((64, 64, 64))
    rgb_3Darray = np.zeros((64, 64, 64, 3))
    for i in range(8):
        for j in range(8):
            num = 64 - mapping[i][j]
            for a in range(64):
                for b in range(64):
                    if np.all(rgb_2Darray[i * 64 + a][j * 64 + b] < cutoff):
                        boolean_table[a][b][num] = True
                        rgb_3Darray[a][b][num] = rgb_2Darray[i * 64 + a][j * 64 + b]
    return rgb_3Darray, boolean_table

@jit(nopython=True)
def boolean_table_to_rgb_2Darray_professor(rgb_2Darray, cutoff, choice=0):
    boolean_table = np.zeros((64, 64, 64))
    rgb_3Darray = np.zeros((64, 64, 64, 3))
    for i in range(8):
        for j in range(8):
            for a in range(64):
                for b in range(64):
                    x_pos = 63 - a
                    y_pos = 63 - b
                    z_pos = (7 - i) * 8 + (7 - j)
                    x_pixel = rgb_2Darray[(x_pos // 8) * 64 + b][(x_pos - 8 * (x_pos // 8)) * 64 + z_pos]
                    y_pixel = rgb_2Darray[511 + (y_pos // 8) * 64 + a][(y_pos - 8 * (y_pos // 8)) * 64 + z_pos]
                    z_pixel = rgb_2Darray[i * 64 + a][(j + 8) * 64 + b]
                    result = np.array([np.all(x_pixel < cutoff), np.all(y_pixel < cutoff), np.all(z_pixel < cutoff)])
                    if professor_judgement(result, choice):
                        boolean_table[a][b][z_pos] = True
                        rgb_3Darray[a][b][z_pos] = (x_pixel + y_pixel + z_pixel) / 255
    return rgb_3Darray, boolean_table

@jit(nopython=True)
def boolean_table_to_rgb_2Darray_Hilbert_and_professor(rgb_2Darray, cutoff, mapping, choice=0):
    boolean_table = np.zeros((64, 64, 64))
    rgb_3Darray = np.zeros((64, 64, 64, 3))
    for i in range(8):
        for j in range(8):
            for a in range(64):
                for b in range(64):
                    x_pos = 64 - a
                    xofx, yofx = np.where(mapping == x_pos)
                    y_pos = 64 - b
                    xofy, yofy = np.where(mapping == y_pos)
                    z_pos = 64 - mapping[i][j]
                    x_pixel = rgb_2Darray[xofx[0] * 64 + b][yofx[0] * 64 + z_pos]
                    y_pixel = rgb_2Darray[511 + (xofy[0] * 64) + a][(yofy[0] * 64) + z_pos]
                    z_pixel = rgb_2Darray[i * 64 + a][(j + 8) * 64 + b]
                    result = np.array([np.all(x_pixel < cutoff), np.all(y_pixel < cutoff), np.all(z_pixel < cutoff)])
                    if professor_judgement(result, choice):
                        boolean_table[a][b][z_pos] = True
                        rgb_3Darray[a][b][z_pos] = (x_pixel + y_pixel + z_pixel) / 255
    return rgb_3Darray, boolean_table