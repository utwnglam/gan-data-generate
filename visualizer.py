import matplotlib.pyplot as plt
from pyface.api import GUI
from mayavi import mlab
import numpy as np
from PIL import Image
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import os
import sys
import glob
import argparse

import binvox_rw
import moviepy.editor as mpy

RESO = 40
RATIO = 4
TOTAL = RESO * RATIO
CutOff = 192


def method2_range100():
    img = Image.open('result/00035-sgan-custom-256voxel40x40-4gpu004705.png')
    data = np.array(img)
    colors = np.resize(data, (TOTAL, TOTAL, TOTAL, 3))
    #  -----------------------------------------
    #    UNCOMMENT IT IF YOU HAVE ENLARGED
    #  -----------------------------------------
    # data = data[::RATIO, ::RATIO, ::RATIO, 0:]
    cube = np.zeros((RESO, RESO, RESO), dtype=bool)

    for count in range(101):
        transparent = np.array([0.0 + count * 0.01, 0.0 + count * 0.01, 0.0 + count * 0.01])
        for i in range(colors.shape[0]):
            for j in range(colors.shape[1]):
                for k in range(colors.shape[2]):
                    if colors[i][j][k][0] < transparent[0] and colors[i][j][k][1] < transparent[1] and \
                            colors[i][j][k][2] < transparent[2]:
                        cube[i][j][k] = True

        #
        #  PLOTTING GRAPH TO SEE VOXEL
        #
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(cube, facecolors=colors, edgecolor='grey')
        plt.savefig('ViewResult/view_' + str(count) + '.png')
        # plt.show()

        cube = np.zeros((RESO, RESO, RESO), dtype=bool)     # resetting the whole cube array


def method2_range255():
    img = Image.open('voxel_result/output256_6.png')
    data = np.array(img)
    data = np.resize(data, (TOTAL, TOTAL, TOTAL, 3))

    cube = np.zeros((RESO, RESO, RESO), dtype=bool)
    transparent = np.array([CutOff, CutOff, CutOff])

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                # it is TRUE when all value in the compare result array is TRUE
                if np.all(data[i][j][k] <= transparent):
                    cube[i][j][k] = True

    colors = np.divide(data, 255)

    #
    #  PLOTTING GRAPH TO SEE VOXEL
    #
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.voxels(cube, facecolors=colors)

    if not os.path.exists('ViewResult'):
        os.makedirs('ViewResult')
    plt.savefig('ViewResult/view_' + str(CutOff) + '_6.png')


def method_1():
    file_list = []

    if len(sys.argv) > 1:
        folder_name = sys.argv[1]
        file_list = glob.glob('voxel_result/*' + folder_name + '*.png')
        print(file_list)

    for file in file_list:
        img = Image.open(file)
        data = np.array(img)
        data = np.resize(data, (TOTAL, TOTAL, TOTAL, 3))
        colors = data[::RATIO, ::RATIO, ::RATIO, 0:]

        cube = np.zeros((RESO, RESO, RESO), dtype=bool)
        transparent = np.array([CutOff, CutOff, CutOff])

        for i in range(colors.shape[0]):
            for j in range(colors.shape[1]):
                for k in range(colors.shape[2]):
                    if np.all(colors[i][j][k] <= transparent):  # return TRUE when all the compare result is TRUE
                        cube[i][j][k] = True

        colors = colors / 256.0
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(cube, facecolors=colors)

        if not os.path.exists('ViewResult'):
            os.makedirs('ViewResult')
        plt.savefig('ViewResult/view_' + str(CutOff) + '_' + file[13:])


def finding_cut_off(cut_off, file, colors):
    #
    #  CHECKING FROM 128 TO cut_off
    #
    for iteration in range(128, cut_off, 10):
        cube = np.zeros((RESO, RESO, RESO), dtype=bool)
        transparent = np.array([iteration, iteration, iteration])

        for i in range(colors.shape[0]):
            for j in range(colors.shape[1]):
                for k in range(colors.shape[2]):
                    if np.all(colors[i][j][k] <= transparent):
                        cube[i][j][k] = True

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(cube, facecolors=(colors / 256.0))
        if not os.path.exists('ViewResult/' + file[13:-4]):
            os.makedirs('ViewResult/' + file[13:-4])
        plt.savefig('ViewResult/' + file[13:-4] + '/view' + str(iteration) + '.png')


def method3():
    file_list = []
    view_angle = ''
    CutOff = 192

    if len(sys.argv) > 2:
        folder_name = sys.argv[1]
        file_list = glob.glob('voxel_result/*' + folder_name + '*.png')
        print(file_list)
        view_angle = sys.argv[2]
        if len(sys.argv) > 3:
            CutOff = int(sys.argv[3])
    else:
        print('#\n#   USAGE: python visualizer.py [DataSet_folder_name] [Viewing_angle] [Target_transparency]\n#')

    for file in file_list:
        #
        #  OPEN AND CONVERT 2D PNG TO 3D VOXEL ARRAY
        #
        img = Image.open(file)
        data = np.array(img)
        data = data[::RATIO, ::RATIO, 0:]
        colors = np.resize(data, (RESO, RESO, RESO, 3))

        if len(sys.argv) == 4:
            finding_cut_off(CutOff, file, colors)
        elif len(sys.argv) == 3:
            cube = np.zeros((RESO, RESO, RESO), dtype=bool)
            transparent = np.array([CutOff, CutOff, CutOff])

            for i in range(colors.shape[0]):
                for j in range(colors.shape[1]):
                    for k in range(colors.shape[2]):
                        if np.all(colors[i][j][k] <= transparent):  # return TRUE when all the compare result is TRUE
                            cube[i][j][k] = True

            #
            #  PLOTTING GRAPH TO SEE VOXEL
            #
            colors = (colors / 256.0)
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.voxels(cube, facecolors=colors)

            #   -------------------
            #       view angle
            #   -------------------
            if view_angle == 'x':
                # ax.view_init(10, -85)
                ax.view_init(0, -90)
            elif view_angle == 'y':
                # ax.view_init(10, 8)
                ax.view_init(0, 0)
            elif view_angle == 'z':
                ax.view_init(5, 38)

            if not os.path.exists('ViewResult'):
                os.makedirs('ViewResult')
            plt.savefig('ViewResult/view' + view_angle + '_' + file[13:])


def find_centre(args):
    view_angle = args.angle
    cut_off = args.cutoff
    file_list = glob.glob('voxel_result/*.png')
    print(file_list)

    for file in file_list:
        #
        #  OPEN AND CONVERT 2D PNG TO 3D VOXEL ARRAY
        #
        img = Image.open(file)
        data = np.array(img)
        data = data[::RATIO, ::RATIO, 0:]
        colors = np.resize(data, (RESO, RESO, RESO, 3))

        cube = np.zeros((RESO, RESO, RESO), dtype=bool)
        flag = 0
        x_sum = y_sum = z_sum = 0.0

        for i in range(colors.shape[0]):
            for j in range(colors.shape[1]):
                for k in range(colors.shape[2]):
                    if np.all(colors[i][j][k] < cut_off):  # return TRUE when all the compare result is TRUE
                        flag += 1
                        x_sum += i
                        y_sum += j
                        z_sum += k
                        cube[i][j][k] = True

        colors = (colors / 256.0)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(cube, facecolors=colors)

        centre = [x_sum/flag, y_sum/flag, z_sum/flag]
        text = 'Estimated centre of cube[x, y, z]:\n' + str(centre)
        plt.annotate(text, xy=(40, 40), xycoords='figure pixels', fontsize=12)

        if view_angle == 'x':
            ax.view_init(0, -90)
        elif view_angle == 'y':
            ax.view_init(0, 0)
        elif view_angle == 'z':
            # ax.view_init(5, 38)
            ax.view_init(20, 45)

        if not os.path.exists('ViewResult'):
            os.makedirs('ViewResult')
        plt.savefig('ViewResult/view' + view_angle + '_' + file[13:])
        # plt.show()


def interpolation(args):
    cut_off = args.cutoff
    file_list = glob.glob('voxel_result/*.png')

    for file in file_list:
        base = os.path.basename(file)
        print(base)
        base = os.path.splitext(base)[0]
        img = Image.open(file)
        data = np.array(img)

        #
        #   INTERPOLATION PROCESS
        #
        intermediate = np.zeros((256, 256, 3))
        temp = RATIO * RATIO
        for a in range(intermediate.shape[0]):
            for b in range(intermediate.shape[1]):
                inter_sum = np.full(3, 0.0)
                for m in range(a*RATIO, a*RATIO + RATIO):
                    for n in range(b*RATIO, b*RATIO + RATIO):
                        inter_sum += data[m][n]
                if np.all(0 <= (inter_sum / temp)) and np.all((inter_sum / temp) < 256):
                    intermediate[a][b] = inter_sum / temp
                elif np.any((inter_sum / temp) >= 256):
                    intermediate[a][b] = np.full(3, 256)
                elif np.any((intermediate[a][b]) < 0):
                    intermediate[a][b] = np.full(3, 0)

        colors = np.resize(intermediate, (RESO, RESO, RESO, 3))
        furniture = np.zeros((RESO, RESO, RESO), dtype=bool)

        for i in range(colors.shape[0]):
            for j in range(colors.shape[1]):
                for k in range(colors.shape[2]):
                    if np.all(colors[i][j][k] < cut_off):
                        furniture[i][j][k] = 1

        fig = mlab.figure(1, fgcolor=(0.4, 0.4, 0.4), bgcolor=(0.9, 0.9, 0.9), size=(600, 600))
        xx, yy, zz = np.where(furniture == 1)
        s = np.arange(len(xx))
        lut = np.zeros((len(xx), 4))
        for row in s:
            temp = np.append((colors[xx[row]][yy[row]][zz[row]] + (256 - 216)), 255)
            lut[row, :] = temp

        currfig = mlab.points3d(xx, yy, zz, s, scale_mode='none', mode="cube", scale_factor=1)
        currfig.module_manager.scalar_lut_manager.lut.number_of_colors = len(s)
        currfig.module_manager.scalar_lut_manager.lut.table = lut

        fp = RESO / 2
        if args.angle == 'x':
            mlab.view(azimuth=270, elevation=90, distance=130, focalpoint=(fp, fp, fp))
        elif args.angle == 'y':
            mlab.view(azimuth=0, elevation=90, distance=130, focalpoint=(fp, fp, fp))
        elif args.angle == 'iso':
            mlab.view(azimuth=315, elevation=65, distance=130, focalpoint=(fp, fp, fp))
        fig.scene.camera.parallel_projection = True
        fig.scene.camera.parallel_scale = 55
        mlab.axes(figure=fig, nb_labels=5, extent=(0, RESO, 0, RESO, 0, RESO))
        mlab.outline(extent=(0, RESO, 0, RESO, 0, RESO))

        duration = 6  # duration of the animation in seconds (it will loop)

        def make_frame(t):
            """ Generates and returns the frame for time t. """
            mlab.view(azimuth=360 * t / duration)  # camera angle
            return mlab.screenshot(antialiased=True)  # return a RGB image

        output = 'ViewResult/' + base + '_out.gif'
        animation = mpy.VideoClip(make_frame, duration=duration).resize(0.5)
        # Video generation takes 10 seconds, GIF generation takes 25s
        animation.write_gif(output, fps=25)

        # GUI().process_events()
        # imgmap_RGB = mlab.screenshot(figure=fig, mode='rgb', antialiased=True)
        # img_RGB = np.uint8(imgmap_RGB)
        # img_RGB = Image.fromarray(img_RGB)
        # if not os.path.exists('ViewResult'):
        #     os.makedirs('ViewResult')
        # img_RGB.save(output)

        # mlab.show()
        mlab.clf()


def binvox_viewer():
    file_list = glob.glob('BINVOX/INPUT/*.binvox')

    for file in file_list:
        #
        #   VISUALIZE BINVOX FILE DIRECTLY
        #

        with open(file, 'rb') as f:
            model = binvox_rw.read_as_3d_array(f)
        print(model.data.shape)
        colors = np.ones(model.data.shape + (3,))
        colors[model.data, :] = (0.5, 0.5, 0.5)

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(model.data, facecolors=colors, edgecolor='k')
        plt.show()


def main():
    parser = argparse.ArgumentParser(description='Finding the centre point of the 3D cube')
    parser.add_argument('-a', '--angle', type=str, default='iso', choices=['x', 'y'],
                        help='The viewing angle of 3D space')
    parser.add_argument('-c', '--cutoff', type=int, default=192, help='The cut off value of the colour range')
    args = parser.parse_args()
    # find_centre(args)
    interpolation(args)


if __name__ == "__main__":
    main()
