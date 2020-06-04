import glob
import binvox_rw
import os
import PIL.Image
import numpy as np
import argparse
from shutil import copyfile
import binvox_rw
from mayavi import mlab
from PIL import Image
from image2D_to_image3D import convent_from_3Darray_color_to_boolean
from pyface.api import GUI

def making_3Darray_from_2D_color_array(image2D, color_mode=False, mode="slice", cufoff = 128):
    model = np.zeros((64, 64, 64, 3))
    for i in range(8):
        for j in range(8):
            for a in range(64):
                for b in range(64):
                    if np.all(image2D[i * 64 + a][j * 64 + b] < cufoff):
                        model[a][b][ (7 - i) * 8 + ( 7 - j)] = image2D[i * 64 + a][j * 64 + b]
                    else:
                        model[a][b][ (7 - i) * 8 + ( 7 - j)] = [255,255,255]
    boolean_table = convent_from_3Darray_color_to_boolean(model)
    return boolean_table

def making_3Dview_from_array(array3D):

    xx, yy, zz = np.where(array3D == 1)
    fig = mlab.figure(1, size=(512, 555))
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
    GUI().process_events()
    imgmap_RGB = mlab.screenshot(figure=fig, mode='rgb', antialiased=True)
    img_RGB = np.uint8(imgmap_RGB)
    img_RGB = Image.fromarray(img_RGB)
    return img_RGB

def makeing_3Darray_from_binvox(binvox_file):
    with open(binvox_file, 'rb') as f:
        model = binvox_rw.read_as_3d_array(f)
    return model.data

def comparing_two_images(image1, image2):
    simliarity_table = np.equal(image1,image2)
    simliarity = np.count_nonzero(simliarity_table == True)
    return simliarity / (image1.shape[0] * image1.shape[1] * image1.shape[2]) * 100

def comparing_two_folders(args):
    input_file_list = glob.glob(args.input_folder + '/*.png')
    binvox_file_list = glob.glob(args.binvox_folder + '/*.binvox')
    print("length of input list : " + str(len(input_file_list)))
    print("length of binvox list : " + str(len(binvox_file_list)))
    for input_file in input_file_list:
        input_base = os.path.basename(input_file)
        input_base = os.path.splitext(input_base)[0]
        print("current input : " + input_base)
        input_image = Image.open(input_file)
        input_image = np.array(input_image)
        highest_similarity, highest_similarity_binvox = (0, None)
        for binvox_file in binvox_file_list:
            binvox_base = os.path.basename(binvox_file)
            binvox_base = os.path.splitext(binvox_base)[0]
            current_similarity_binvox = binvox_base
            current_similarity = comparing_two_images(making_3Darray_from_2D_color_array(input_image),makeing_3Darray_from_binvox(binvox_file))
            
            print("current current_similarity_binvox : " + binvox_base)
            print("current current_similarity : " + str(current_similarity))

            if(highest_similarity < current_similarity):
                highest_similarity = current_similarity
                highest_similarity_binvox = current_similarity_binvox
        print("highest_similarity : " + str(highest_similarity))
        print("highest_similarity_binvox : " + highest_similarity_binvox)
        if not os.path.exists('OUTPUT/' + input_base):
            os.makedirs('OUTPUT/' + input_base)
        copyfile(input_file, 'OUTPUT/' + input_base + '/' + input_base + '_src.png')
        dst_img_RGB = making_3Dview_from_array(makeing_3Darray_from_binvox(binvox_file))
        dst_img_RGB.save('OUTPUT/' + input_base + '/' + highest_similarity_binvox + '_dst.png')

        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('binvox_folder', type=str, help='enter the path of the binvox files')
    parser.add_argument('input_folder', type=str, help='enter the path of the images located which you want to compare with')
    args = parser.parse_args()
    comparing_two_folders(args)
    

if __name__ == "__main__":
    main()
