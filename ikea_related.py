import os
import glob
import argparse

import numpy as np
import scipy.ndimage
import binvox_rw


def to_vox():
    file_list = glob.glob('ShapeNetCore.v2/Collection/table/*.obj')

    for file in file_list:
        basename = os.path.basename(file)
        print(basename)
        os.system('./binvox -d 128 -down -dc -cb -rotx' + file)


def variation(args):
    file_list = glob.glob('BINVOX/DATA/BINVOX_' + args.folder + '/*.binvox')

    for file in file_list:
        base = os.path.basename(file)
        base = os.path.splitext(base)[0]

        with open(file, 'rb') as f:
            model = binvox_rw.read_as_3d_array(f)

        # scipy.ndimage.binary_dilation(model.data.copy(), output=model.data)

        edge = 64
        zoom_tuple = np.array([args.x, args.y, args.z])

        # Zooming out
        if np.any(zoom_tuple < 1):
            # Bounding box of the zoomed-out image within the output array
            zx = int(np.round(edge * args.x))
            zy = int(np.round(edge * args.y))
            zz = int(np.round(edge * args.z))

            x_axis = (edge - zx) // 2
            y_axis = (edge - zy) // 2
            z_axis = (edge - zz) // 2

            # Zero-padding
            out = np.zeros_like(model.data)
            out[x_axis:x_axis + zx, y_axis:y_axis + zy, z_axis:z_axis + zz] = \
                scipy.ndimage.zoom(model.data, zoom_tuple, order=0)

            # Moving the model up
            stop = 0
            while stop <= 32:
                if out[31][31][63 - stop]:
                    print(base, 63 - stop)
                    break
                elif out[30][31][63 - stop] or out[32][31][63 - stop]:
                    print('hi')
                    break
                stop += 1
            out = np.zeros_like(model.data)
            out[:, :, stop:64] = model.data[:, :, 0:64 - stop]
            model.data = out

        out_name = 'BINVOX/OUTPUT/' + base + '_x' + str(args.x) + 'y' + str(args.y) + 'z' + str(args.z) + '.binvox'

        with open(out_name, 'wb') as f:
            model.write(f)


def binvox_downsample():
    # file_list = glob.glob('ShapeNetCore.v2/Collection/table/*.binvox')
    file_list = glob.glob('*.binvox')

    for file in file_list:
        base = os.path.splitext(file)[0]
        print(base)
        with open(file, 'rb') as f:
            model = binvox_rw.read_as_3d_array(f)

        zoom_tuple = np.array([0.5, 0.5, 0.5])
        inter = scipy.ndimage.zoom(model.data, zoom_tuple, order=0)
        inter = np.rot90(inter, k=1, axes=(1, 2))

        x1 = y1 = z1 = x2 = y2 = z2 = 0
        for i in range(inter.shape[0]):
            x1 = i
            if np.any(inter[i]):
                break
        for i2 in reversed(range(inter.shape[0])):
            x2 = i2
            if np.any(inter[i2]):
                break
        for j in range(inter.shape[1]):
            y1 = j
            if np.any(inter[:, j]):
                break
        for j2 in reversed(range(inter.shape[1])):
            y2 = j2
            if np.any(inter[:, j2]):
                break
        for k in range(inter.shape[2]):
            z1 = k
            if np.any(inter[:, :, k]):
                break
        for k2 in reversed(range(inter.shape[2])):
            z2 = k2
            if np.any(inter[:, :, k2]):
                break

        print(x1, x2, y1, y2, z1, z2)
        bx = (x1 + (inter.shape[0]-1 - x2)) // 2
        by = (y1 + (inter.shape[1]-1 - y2)) // 2
        bz = (z1 + (inter.shape[2]-1 - z2)) // 2
        print(bx, by, bz)

        out = np.zeros_like(inter)
        out[bx: bx+(x2-x1), by: by+(y2-y1), bz: bz+(z2-z1)] = inter[x1:x2, y1:y2, z1:z2]
        model.data = out
        model.dims = [inter.shape[0], inter.shape[1], inter.shape[2]]
        out_name = base + '_64.binvox'

        with open(out_name, 'wb') as f:
            model.write(f)


def z_axis_pos():
    file_list = glob.glob('BINVOX/INPUT/*.binvox')

    for file in file_list:
        base = os.path.basename(file)

        with open(file, 'rb') as f:
            model = binvox_rw.read_as_3d_array(f)

        stop = 0
        while stop <= 32:
            if model.data[31][31][63 - stop]:
                print(base, 63 - stop)
                break
            elif model.data[30][31][63 - stop] or model.data[32][31][63 - stop]:
                print('hi')
                break
            stop += 1

        out = np.zeros_like(model.data)
        out[:, :, stop:64] = model.data[:, :, 0:64 - stop]
        model.data = out
        out_name = 'BINVOX/OUTPUT/' + base

        with open(out_name, 'wb') as f:
            model.write(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('function', type=str, help='enter \'scale\'/ \'convert\'')
    parser.add_argument('folder', type=str, help='enter the target folder to scale/ convert to binvox')
    parser.add_argument('-x', type=float, default=1.0, help='x-axis zoom factor (0.1 - 1.0)')
    parser.add_argument('-y', type=float, default=1.0, help='y-axis zoom factor (0.1 - 1.0)')
    parser.add_argument('-z', type=float, default=1.0, help='z-axis zoom factor (0.1 - 1.0)')
    args = parser.parse_args()

    if args.function == 'convert':
        to_vox()
    elif args.function == 'scale':
        # variation(args)
        pass


if __name__ == "__main__":
    binvox_downsample()
