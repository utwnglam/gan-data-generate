import numpy as np
from PIL import Image

import os
import sys
import glob
import argparse

# import moviepy.editor as mpy
from pyface.api import GUI
from mayavi import mlab

RESO = 64
CutOff = 128
mapping = np.array([
        [1, 2, 15, 16, 17, 20, 21, 22],
        [4, 3, 14, 13, 18, 19, 24, 23],
        [5, 8, 9, 12, 31, 30, 25, 26],
        [6, 7, 10, 11, 32, 29, 28, 27],
        [59, 58, 55, 54, 33, 36, 37, 38],
        [60, 57, 56, 53, 34, 35, 40, 39],
        [61, 62, 51, 52, 47, 46, 41, 42],
        [64, 63, 50, 49, 48, 45, 44, 43],
    ])


def flatten(data):
    furniture = np.zeros((RESO, RESO, RESO), dtype=bool)
    colors = np.zeros((RESO, RESO, RESO, 3))

    for i in range(8):
        for j in range(8):
            z_num = (7 - i) * 8 + (7 - j)
            for a in range(64):
                for b in range(64):
                    if np.all(data[i * 64 + a][j * 64 + b] < CutOff):
                        furniture[a][b][z_num] = True
                        colors[a][b][z_num] = data[i * 64 + a][j * 64 + b]

    return furniture, colors


def hilbert(data):
    furniture = np.zeros((RESO, RESO, RESO), dtype=bool)
    colors = np.zeros((RESO, RESO, RESO, 3))

    for i in range(8):
        for j in range(8):
            num = 64 - mapping[i][j]
            for a in range(64):
                for b in range(64):
                    if np.all(data[i * 64 + a][j * 64 + b] < CutOff):
                        furniture[a][b][num] = True
                        colors[a][b][num] = data[i * 64 + a][j * 64 + b]

    return furniture, colors


def professor(data):
    furniture = np.zeros((RESO, RESO, RESO), dtype=bool)
    colors = np.zeros((RESO, RESO, RESO, 3))

    for i in range(8):
        for j in range(8):
            z_num = (7 - i) * 8 + (7 - j)
            for a in range(64):
                for b in range(64):

                    if np.all(data[i * 64 + a][j * 64 + b] < CutOff):
                        furniture[a][b][num] = True
                        colors[a][b][num] = data[i * 64 + a][j * 64 + b]

    return furniture, colors


def hilbert_professor():
    pass


def make_frame(t):
    """ Generates and returns the frame for time t. """
    duration = 6  # duration of the animation in seconds
    mlab.view(azimuth=360 * t / duration)  # camera angle

    return mlab.screenshot(antialiased=True)  # return a RGB image


def visualize(args):
    file_list = glob.glob('voxel_result/*.png')

    for file in file_list:
        img = Image.open(file)
        basename = os.path.basename(file)
        basename = os.path.splitext(basename)[0]
        data = np.array(img)
        print(basename, data.shape)

        furniture, colors = method_dict[args.mode](data)

        xx, yy, zz = np.where(furniture == 1)
        s = np.arange(len(xx))
        lut = np.zeros((len(xx), 4))
        for row in s:
            temp = np.append((colors[xx[row]][yy[row]][zz[row]] + (256 - 208)), 255)
            lut[row, :] = temp

        # Plot the points, update its lookup table
        currfig = mlab.points3d(xx, yy, zz, s,
                                scale_mode='none',
                                mode="cube",
                                scale_factor=1)
        fig = mlab.figure(1, size=(512, 555))
        currfig.module_manager.scalar_lut_manager.lut.number_of_colors = len(s)
        currfig.module_manager.scalar_lut_manager.lut.table = lut

        mlab.view(azimuth=315, elevation=65, distance=140, focalpoint=(32, 32, 32))
        fig.scene.camera.parallel_projection = True
        fig.scene.camera.parallel_scale = 65  # smaller the number, greater zoom
        mlab.axes(figure=fig, nb_labels=5, extent=(0, RESO, 0, RESO, 0, RESO))
        mlab.outline(extent=(0, RESO, 0, RESO, 0, RESO))

        # output = 'ViewResult/' + basename + '_out.gif'
        # animation = mpy.VideoClip(make_frame, duration=duration).resize(0.5)
        # animation.write_gif(output, fps=25)

        output = 'ViewResult/' + basename + '_3D.png'
        GUI().process_events()
        imgmap_RGB = mlab.screenshot(figure=fig, mode='rgb', antialiased=True)
        img_RGB = np.uint8(imgmap_RGB)
        img_RGB = Image.fromarray(img_RGB)
        if not os.path.exists('ViewResult'):
            os.makedirs('ViewResult')
        img_RGB.save(output)

        mlab.clf()


method_dict = {
    "flatten": flatten,
    "hilbert": hilbert,
    "professor": professor,
    "hilbert_and_professor": hilbert_professor
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=str, choices=["flatten", "hilbert", "professor", "hilbert_and_professor"],
                        help='enter \'flatten\'/ \'hilbert\' \'professor\' \'hilbert_and_professor\'')
    args = parser.parse_args()
    visualize(args)


if __name__ == "__main__":
    main()
