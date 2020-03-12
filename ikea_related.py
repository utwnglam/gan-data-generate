import os
import glob
import argparse

import numpy as np
import scipy.ndimage
import binvox_rw


def to_vox(args):
    file_list = glob.glob('BINVOX/DATA/IKEA_' + args.folder + '/*')
    print(file_list)

    for file in file_list:
        os.system('./BINVOX/binvox -d 64 -dc ' + file)


def variation(args):
    file_list = glob.glob('BINVOX/DATA/BINVOX_' + args.folder + '/*.binvox')

    for file in file_list:
        print(file)
        with open(file, 'rb') as f:
            model = binvox_rw.read_as_3d_array(f)

        scipy.ndimage.binary_dilation(model.data.copy(), output=model.data)
        # scipy.ndimage.binary_erosion(model.data.copy(), structure=np.ones((1, 1, 1)), output=model.data)

        with open('BINVOX/chair_out.binvox', 'wb') as f:
            model.write(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=str, help='The target IKEA folder to convert')
    args = parser.parse_args()
    # to_vox(args)
    variation(args)


if __name__ == "__main__":
    main()
