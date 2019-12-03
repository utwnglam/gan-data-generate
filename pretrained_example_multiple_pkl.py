import os
import pickle
import numpy as np
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import config
import os
import glob
import sys

def main():
    # Initialize TensorFlow.
    file_name = 'pkl_file_z_axis_dataset1000'
    tflib.init_tf()
    input_var = '*'
    if len(sys.argv) > 1:
        input_var = sys.argv[1]
    # Load pre-trained network.
    #url = 'https://drive.google.com/uc?id=1MEGjdvVpUsu1jB4zrXZN7Y4kBBOzizDQ' # karras2019stylegan-ffhq-1024x1024.pkl
    path = './' + str(file_name) + '/network-snapshot-' + '*' +'.pkl'
    pkl_list = glob.glob(path)
    if(input_var == '*'):
        input_var = 0
    sorted_pkl_list = []
    for pkl in pkl_list:
        if (int(pkl[-10:-4]) >= int(input_var)):
            sorted_pkl_list.append(pkl)

    for pkl in sorted_pkl_list:
        with open(pkl, 'rb') as f:
            _G, _D, Gs = pickle.load(f)
        Gs.print_layers()

        rnd = np.random.RandomState(4)
        latents = rnd.randn(1, Gs.input_shape[1])  #output 1 row of this shape:Gs.input_shape[1]
        # print(Gs.input_shape[1])  #512
        print(latents)
        # print(len(latents))
        # print(len(latents[0]))
        # os.system("pause")
        # Generate image.
        fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
        images = Gs.run(latents, None, truncation_psi=0.7, randomize_noise=False, output_transform=fmt) # noise = False

        # Save image.
        os.makedirs('multiple_pkl_result', exist_ok=True)

        png_filename = os.path.join('multiple_pkl_result', 'example_without_noise_' + pkl[-10:-4] + '_.png')
        PIL.Image.fromarray(images[0], 'RGB').save(png_filename)
        print('saved image' + pkl[-10:-4])

    # with open('network-snapshot-007050.pkl', 'rb') as f:
    #     _G, _D, Gs = pickle.load(f)
    #     # _G = Instantaneous snapshot of the generator. Mainly useful for resuming a previous training run.
    #     # _D = Instantaneous snapshot of the discriminator. Mainly useful for resuming a previous training run.
    #     # Gs = Long-term average of the generator. Yields higher-quality results than the instantaneous snapshot.

    # # Print network details.
    # Gs.print_layers()

    # # Pick latent vector.
    # for count in range(20):
    #     rnd = np.random.RandomState(count)
    #     latents = rnd.randn(1, Gs.input_shape[1])  #output 1 row of this shape:Gs.input_shape[1]
    #     # print(Gs.input_shape[1])  #512
    #     # print(latents)
    #     # print(len(latents))
    #     # print(len(latents[0]))
    #     # os.system("pause")
    #     # Generate image.
    #     fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
    #     images = Gs.run(latents, None, truncation_psi=0.7, randomize_noise=False, output_transform=fmt) # noise = False

    #     # Save image.
    #     os.makedirs(config.result_dir, exist_ok=True)
    #     png_filename = os.path.join(config.result_dir, 'example_without_noise_' + str(count) + '_.png')
    #     PIL.Image.fromarray(images[0], 'RGB').save(png_filename)

if __name__ == "__main__":
    main()