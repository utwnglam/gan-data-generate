from pyface.api import GUI
from mayavi import mlab
import numpy as np
from PIL import Image
import os
import glob
import argparse

import binvox_rw
# import moviepy.editor as mpy

space = 40
max_cutoff = 192


def binvox_viewer():
    # file_list = glob.glob('BINVOX/DATA/BINVOX_desk/*.binvox')
    file_list = glob.glob('voxel_result/*.binvox')

    for file in file_list:
        base = os.path.basename(file)
        print(base)
        base = os.path.splitext(base)[0]

        #
        #   VISUALIZE BINVOX FILE DIRECTLY
        #
        with open(file, 'rb') as f:
            model = binvox_rw.read_as_3d_array(f)
        # print(np.any(model.data[:, :, 63]))
        xx, yy, zz = np.where(model.data == 1)

        fig = mlab.figure(1, size=(700, 700))

        mlab.points3d(xx, yy, zz,
                      # scale_mode='none',
                      color=(0, 1, 0),
                      mode="cube",
                      scale_factor=1)
        mlab.view(azimuth=225, elevation=70, distance=140, focalpoint=(32, 32, 32))
        fig.scene.camera.parallel_projection = True
        fig.scene.camera.parallel_scale = 65
        mlab.axes(figure=fig, nb_labels=5, extent=(0, 64, 0, 64, 0, 64))
        mlab.outline(extent=(0, 64, 0, 64, 0, 64))

        # output = 'BINVOX/OUTPUT/' + base + '_3D.png'
        output = 'View/' + base + '_3D.png'
        GUI().process_events()
        imgmap_RGB = mlab.screenshot(figure=fig, mode='rgb', antialiased=True)
        img_RGB = np.uint8(imgmap_RGB)
        img_RGB = Image.fromarray(img_RGB)
        if not os.path.exists('View'):
            os.makedirs('View')
        img_RGB.save(output)

        # mlab.show()
        mlab.clf()


def png_viewer(args):
    # file_list = glob.glob('BINVOX/INPUT/*.png')
    file_list = glob.glob('voxel_result/*.png')

    for file in file_list:
        base = os.path.basename(file)
        print(base)
        base = os.path.splitext(base)[0]
        img = Image.open(file)
        data = np.array(img)
        data = data[::4, ::4, 0:]
        colors = np.resize(data, (space, space, space, 3))
        furniture = np.zeros((space, space, space))
        fig = mlab.figure(1, size=(650, 690), bgcolor=(0, 0, 0))

        for i in range(colors.shape[0]):
            for j in range(colors.shape[1]):
                for k in range(colors.shape[2]):
                    if np.all(colors[i][j][k] < args.cutoff):
                        furniture[i][j][k] = 1

        xx, yy, zz = np.where(furniture == 1)
        # Create and populate lookup table (the integer index in s corresponding
        #   to the point will be used as the row in the lookup table
        s = np.arange(len(xx))
        lut = np.zeros((len(xx), 4))
        for row in s:
            # temp = np.append((colors[xx[row]][yy[row]][zz[row]] + (256-max_cutoff)), 255)
            temp = np.append((185, 208, 208), 255)
            lut[row, :] = temp

        # Plot the points, update its lookup table
        currfig = mlab.points3d(xx, yy, zz, s,
                                scale_mode='none',
                                mode="cube",
                                scale_factor=1)
        currfig.module_manager.scalar_lut_manager.lut.number_of_colors = len(s)
        currfig.module_manager.scalar_lut_manager.lut.table = lut

        #
        #   MANIPULATING VIEWING RELATED SETTING
        #
        centre = space / 2
        if args.angle == 'x':
            mlab.view(azimuth=270, elevation=90, distance=140, focalpoint=(centre, centre, centre))
        elif args.angle == 'y':
            mlab.view(azimuth=0, elevation=90, distance=140, focalpoint=(centre, centre, centre))
        elif args.angle == 'iso':
            mlab.view(azimuth=315, elevation=65, distance=140, focalpoint=(centre, centre, centre))
        fig.scene.camera.parallel_projection = True
        fig.scene.camera.parallel_scale = 50    # smaller the number, greater zoom
        mlab.axes(figure=fig, nb_labels=5, extent=(0, space, 0, space, 0, space))
        mlab.outline(extent=(0, space, 0, space, 0, space))

        duration = 6  # duration of the animation in seconds (it will loop)

        def make_frame(t):
            """ Generates and returns the frame for time t. """
            mlab.view(azimuth=360 * t / duration)  # camera angle
            return mlab.screenshot(antialiased=True)  # return a RGB image

        output = 'ViewResult/' + base + '_out.gif'
        # animation = mpy.VideoClip(make_frame, duration=duration).resize(0.5)
        # animation.write_gif(output, fps=25)

        output = 'ViewResult/' + base + '_out.png'
        GUI().process_events()
        imgmap_RGB = mlab.screenshot(figure=fig, mode='rgb', antialiased=True)
        img_RGB = np.uint8(imgmap_RGB)
        img_RGB = Image.fromarray(img_RGB)
        # if not os.path.exists('BINVOX/OUTPUT'):
        #     os.makedirs('BINVOX/OUTPUT')
        img_RGB.save(output)

        mlab.clf()


def main():
    def cutoff_type(x):
        x = int(x)
        if x > max_cutoff:
            raise argparse.ArgumentTypeError('Maximum cutoff is ' + str(max_cutoff))
        return x

    parser = argparse.ArgumentParser(description='Finding the centre point of the 3D cube')
    parser.add_argument('file_type', type=str, choices=['binvox', 'png'], help='enter the target file type')
    parser.add_argument('-a', '--angle', type=str, default='iso', choices=['x', 'y'],
                        help='The viewing angle of 3D space')
    parser.add_argument('-c', '--cutoff', type=cutoff_type, default=192, help='The cut off value of the colour range')
    args = parser.parse_args()

    if args.file_type == 'binvox':
        binvox_viewer()
    elif args.file_type == 'png':
        png_viewer(args)


if __name__ == "__main__":
    main()
