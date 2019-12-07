# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

"""Minimal script for reproducing the figures of the StyleGAN paper using pre-trained generators."""

import os
import pickle
import numpy as np
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import config

import matplotlib.pyplot as plt
from PIL import Image
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import sys
import glob
#----------------------------------------------------------------------------
# Helpers for loading and using pre-trained generators.

synthesis_kwargs = dict(output_transform=dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True), minibatch_size=8)

_Gs_cache = dict()

def load_Gs(url):
    with open('network-snapshot-006720.pkl', 'rb') as f:
        _G, _D, Gs = pickle.load(f)
    return Gs

#----------------------------------------------------------------------------
# Figure 3: Style mixing.

def draw_style_mixing_figure(png, Gs, w, h, src_seeds, dst_seeds, style_ranges):
    print(png)
    src_latents = np.stack(np.random.RandomState(seed).randn(Gs.input_shape[1]) for seed in src_seeds)
    dst_latents = np.stack(np.random.RandomState(seed).randn(Gs.input_shape[1]) for seed in dst_seeds)
    src_dlatents = Gs.components.mapping.run(src_latents, None) # [seed, layer, component]
    dst_dlatents = Gs.components.mapping.run(dst_latents, None) # [seed, layer, component]
    src_images = Gs.components.synthesis.run(src_dlatents, randomize_noise=False, **synthesis_kwargs)
    dst_images = Gs.components.synthesis.run(dst_dlatents, randomize_noise=False, **synthesis_kwargs)

    canvas = PIL.Image.new('RGB', (w * (len(src_seeds) + 1), h * (len(dst_seeds) + 1)), 'white')
    count = 0
    for col, src_image in enumerate(list(src_images)):
        img = PIL.Image.fromarray(src_image, 'RGB')
        img.save('tmp_style_change/output_' + str(count) + ".png")
        path = 'tmp_style_change/output_' + str(count) + ".png"
        img = convert_2D_to_3D(path)
        img.save('tmp_style_change/resize_view_' + str(count) + ".png")
        count = count + 1
        canvas.paste(img, ((col + 1) * w, 0))
    for row, dst_image in enumerate(list(dst_images)):
        img = PIL.Image.fromarray(dst_image, 'RGB')
        img.save('tmp_style_change/output_' + str(count) + ".png")
        path = 'tmp_style_change/output_' + str(count) + ".png"
        img = convert_2D_to_3D(path)
        img.save('tmp_style_change/resize_view_' + str(count) + ".png")
        count = count + 1
        canvas.paste(img, (0, (row + 1) * h))
        row_dlatents = np.stack([dst_dlatents[row]] * len(src_seeds))
        row_dlatents[:, style_ranges[row]] = src_dlatents[:, style_ranges[row]]
        row_images = Gs.components.synthesis.run(row_dlatents, randomize_noise=False, **synthesis_kwargs)
        for col, image in enumerate(list(row_images)):
            img = PIL.Image.fromarray(image, 'RGB')
            img.save('tmp_style_change/output_' + str(count) + ".png")
            path = 'tmp_style_change/output_' + str(count) + ".png"
            img = convert_2D_to_3D(path)
            img.save('tmp_style_change/resize_view_' + str(count) + ".png")
            count = count + 1
            canvas.paste(img, ((col + 1) * w, (row + 1) * h))
    canvas.save(png)

#----------------------------------------------------------------------------
# Figure 8: Truncation trick.

def draw_truncation_trick_figure(png, Gs, w, h, seeds, psis):
    print(png)
    latents = np.stack(np.random.RandomState(seed).randn(Gs.input_shape[1]) for seed in seeds)
    dlatents = Gs.components.mapping.run(latents, None) # [seed, layer, component]
    dlatent_avg = Gs.get_var('dlatent_avg') # [component]

    canvas = PIL.Image.new('RGB', (w * len(psis), h * len(seeds)), 'white')
    for row, dlatent in enumerate(list(dlatents)):
        row_dlatents = (dlatent[np.newaxis] - dlatent_avg) * np.reshape(psis, [-1, 1, 1]) + dlatent_avg
        row_images = Gs.components.synthesis.run(row_dlatents, randomize_noise=False, **synthesis_kwargs)
        for col, image in enumerate(list(row_images)):
            img = PIL.Image.fromarray(image, 'RGB')
            img.save('tmp_style_change/output_tmp.png')
            path = 'tmp_style_change/output_tmp.png'
            img = convert_2D_to_3D(path)
            img.save('tmp_style_change/output_tmp.png')
            canvas.paste(img, (col * w, row * h))
    canvas.save(png)


#----------------------------------------------------------------------------
# 2D to 3D

RESO = 40
RATIO = 4
TOTAL = RESO * RATIO

def convert_2D_to_3D(img):
    file_list = [img]
    CutOff = 192

    for file in file_list:
        #
        #  OPEN AND CONVERT 2D PNG TO 3D VOXEL ARRAY
        #
        img = Image.open(file)
        data = np.array(img)
        data = data[::RATIO, ::RATIO, 0:]
        colors = np.resize(data, (RESO, RESO, RESO, 3))
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
        colors = colors / 255.0
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(cube, facecolors=colors)

        if not os.path.exists('tmp_style_change'):
            os.makedirs('tmp_style_change')
        plt.savefig('tmp_style_change/view_' + str(CutOff) + '.png')
        #------------------------------------------------------------------------------
        # for resize the image to 1024x1024
        im = Image.open(('tmp_style_change/view_' + str(CutOff) + '.png'))
        im = im.resize((1024, 1024),Image.BILINEAR)
        #im = im.save('ViewResult/resize_view_' + str(CutOff) + file[13:])
        return im
        #------------------------------------------------------------------------------
        # plt.show()
#----------------------------------------------------------------------------
# Main program.

def main():
    tflib.init_tf()
    result_folder = 'Style_change_result'
    os.makedirs(result_folder, exist_ok=True)
    draw_style_mixing_figure(os.path.join(result_folder, 'figure03-style-mixing.png'), load_Gs('url_ffhq'), w=1024, h=1024, src_seeds=[639,701,687,615,2268], dst_seeds=[888,829,1898,1733,1614,845], style_ranges=[range(0,4)]*3+[range(4,8)]*2+[range(8,18)])
    draw_truncation_trick_figure(os.path.join(result_folder, 'figure08-truncation-trick.png'), load_Gs('url_ffhq'), w=1024, h=1024, seeds=[91,388], psis=[1, 0.7, 0.5, 0, -0.5, -1])

#----------------------------------------------------------------------------

if __name__ == "__main__":
    main()

#----------------------------------------------------------------------------
