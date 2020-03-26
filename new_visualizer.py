from pyface.api import GUI
from mayavi import mlab
import numpy as np
from PIL import Image

import glob
import argparse

import binvox_rw

space = 64


def binvox_viewer():
    file_list = glob.glob('BINVOX/INPUT/*.binvox')

    for file in file_list:
        print(file)
        #
        #   VISUALIZE BINVOX FILE DIRECTLY
        #
        with open(file, 'rb') as f:
            model = binvox_rw.read_as_3d_array(f)
        print('The input binvox shape is ' + str(model.data.shape))
        xx, yy, zz = np.where(model.data == 1)

        mlab.points3d(xx, yy, zz,
                      color=(0, 1, 0),
                      mode="cube",
                      scale_factor=1)
        mlab.show()


def png_viewer(args):
    file_list = glob.glob('BINVOX/INPUT/*.png')

    for file in file_list:
        print(file)
        img = Image.open(file)
        data = np.array(img)
        colors = np.resize(data, (space, space, space, 3))
        furniture = np.zeros((space, space, space))

        for i in range(colors.shape[0]):
            for j in range(colors.shape[1]):
                for k in range(colors.shape[2]):
                    if np.all(colors[i][j][k] < args.cutoff):
                        furniture[i][j][k] = 1

        xx, yy, zz = np.where(furniture == 1)
        fig = mlab.figure(1, size=(700, 700))
        currfig = mlab.points3d(xx, yy, zz,
                      color=(0, 1, 0),
                      mode="cube",
                      scale_factor=1)

        mlab.axes(nb_labels=4)
        # mlab.view(azimuth=45, elevation=70)
        currfig.scene.camera.zoom(0.7)

        output = 'BINVOX/OUTPUT/' + file[13:]
        GUI().process_events()
        imgmap_RGB = mlab.screenshot(figure=fig, mode='rgb', antialiased=True)
        img_RGB = np.uint8(imgmap_RGB)
        img_RGB = Image.fromarray(img_RGB)
        img_RGB.save(output)

        # mlab.show()


def main():
    parser = argparse.ArgumentParser(description='Finding the centre point of the 3D cube')
    parser.add_argument('file_type', type=str, help='enter the target file type: png/ binvox to view')
    parser.add_argument('--angle', type=str, help='The viewing angle of 3D space')
    parser.add_argument('-c', '--cutoff', type=int, default=192, help='The cut off value of the colour range')
    args = parser.parse_args()
    if args.file_type == 'binvox':
        binvox_viewer()
    elif args.file_type == 'png':
        png_viewer(args)


if __name__ == "__main__":
    main()

