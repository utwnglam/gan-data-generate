import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import os
import sys
import glob
import argparse

import moviepy.editor as mpy
from pyface.api import GUI
from mayavi import mlab

RESO = 64
RATIO = 2
TOTAL = RESO * RATIO
CutOff = 128

def visualize():
    file_list = glob.glob('voxel_result/*.png')

    for file in file_list:
        img = Image.open(file)
        basename = os.path.basename(file)
        data = np.array(img)
        print(data.shape)
        furniture = np.zeros((RESO, RESO, RESO), dtype=bool)
        reshape_png = []
        colors = np.resize(data, (RESO, RESO, RESO, 3))
        for i in range(8):
            for j in range(8):
                for a in range(64):
                    for b in range(64):
                        if np.all(data[i * 64 + a][j * 64 + b] < CutOff):
                            furniture[a][b][ (7 - i) * 8 + ( 7 - j)] = True
                            colors[a][b][ (7 - i) * 8 + ( 7 - j)] = [0,0,0]
                        else:
                            colors[a][b][ (7 - i) * 8 + ( 7 - j)] = [0,0,0]
                        
        # print(reshape_png)
        # colors = np.rot90(colors, 2, (0,1))
        # for i in range(colors.shape[0]):
        #     for j in range(colors.shape[1]):
        #         for k in range(colors.shape[2]):
        #             if np.all(colors[i][j][k] < CutOff):
        #                 furniture[i][j][k] = True

        xx, yy, zz = np.where(furniture == 1)
        s = np.arange(len(xx))
        lut = np.zeros((len(xx), 4))
        for row in s:
            temp = np.append((colors[xx[row]][yy[row]][zz[row]] + (256-208)), 255)
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
        fig.scene.camera.parallel_scale = 65    # smaller the number, greater zoom
        mlab.axes(figure=fig, nb_labels=5, extent=(0, 64, 0, 64, 0, 64))
        mlab.outline(extent=(0, 64, 0, 64, 0, 64))

        duration = 6  # duration of the animation in seconds (it will loop)

        def make_frame(t):
            """ Generates and returns the frame for time t. """
            mlab.view(azimuth=360 * t / duration)  # camera angle
            return mlab.screenshot(antialiased=True)  # return a RGB image

        output = 'ViewResult/' + basename + '_out.gif'
        animation = mpy.VideoClip(make_frame, duration=duration).resize(0.5)
        animation.write_gif(output, fps=25)

        mlab.clf()

def main():
    visualize()

if __name__ == "__main__":
    main()