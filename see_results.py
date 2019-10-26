# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

"""Minimal script for generating an image using pre-trained StyleGAN generator."""

import os
import pickle
import numpy as np
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import config
import glob
import sys

def main():
    if len(sys.argv) > 1:
        target_ID_list = []
        for count in range(len(sys.argv)):
            print(sys.argv[count])
            # Initialize TensorFlow.
    tflib.init_tf()
    path = "./results/00005-sgan-voxel-30-black-4gpu/network*.pkl"
    pkl_list = glob.glob(path)
    # Load pre-trained network.
    for pkl in pkl_list:
        print(pkl)
        pkl_dir = pkl.split('/')
        fh = open(pkl, 'rb')
        _G, _D, Gs = pickle.load(fh)
            # _G = Instantaneous snapshot of the generator. Mainly useful for resuming a previous training run.
            # _D = Instantaneous snapshot of the discriminator. Mainly useful for resuming a previous training run.
            # Gs = Long-term average of the generator. Yields higher-quality results than the instantaneous snapshot.

        # Print network details.
        Gs.print_layers()

        # Pick latent vector.
        rnd = np.random.RandomState(5)
        # print("rnd:")
        # print(rnd)
        latents = rnd.randn(1, Gs.input_shape[1])
        # print("latents:")
        # print(latents)

        # Generate image.
        fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
        images = Gs.run(latents, None, truncation_psi=0.7, randomize_noise=False, output_transform=fmt)

        # Save image.
        os.makedirs(config.result_dir, exist_ok=True)
        png_filename = os.path.join("voxel_result", pkl_dir[2] + pkl_dir[3][-10:-4] + '.png')
        PIL.Image.fromarray(images[0], 'RGB').save(png_filename)
        
    else:
        print("argv[1] = \'-g3\' / \'-g2\' / \'-v\'")
        print('-g3: generate png which represent 3D voxel cube\n-g2: generate png which there is a 2D square')
        print('-v: visualizer - under construction')
        print('argv[2] for \'-g3\' and \'-g2\': NUMBER of png you would like to generate')


if __name__ == "__main__":
    main()
