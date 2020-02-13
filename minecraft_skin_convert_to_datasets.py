import numpy as np
from PIL import Image

import os
import sys
import glob

def converting(folder_location):
    count = 0
    file_list = glob.glob(folder_location + '/*.png')
    for file in file_list:
        print('converting ' + file + ' ' + str(count))
        img = Image.open(file)
        data = np.array(img)
        if(data.shape != (64,64,4)):
            print('The file dimension is not correct!!!')
            continue
        flat_img_list = []
        for row in data:
            # print(i.shape)
            for rgba in row:
                alpha = rgba[3]
                if(alpha >= 128): # which means the pixel exist
                    rgba = rgba[:3]/2
                    flat_img_list.append(rgba)
                elif(alpha <= 127): # which means the pixel does not exist
                    flat_img_list.append(np.array([255,255,255]))
                    
                else:
                    flat_img_list.append(np.array([255,255,255]))
                    print('The alpha value is: ' + str(alpha))
                    print('The png alpha value is either 0 nor 255. There must be some problem exist!!!')
                    # exit()
        int_img_list = np.uint8(flat_img_list)
        output = int_img_list.reshape((64, 64, 3))
        output = output.repeat(16, axis=0)
        output = output.repeat(16, axis=1)
        new = Image.fromarray(output)
        count = count + 1
        new.save('gen_output' + '/gen_' + str(count) + ".png")
    print('done')
def main():
    if not os.path.exists('gen_output'):
            os.makedirs('gen_output')
    if len(sys.argv) == 2:
        print(sys.argv)
        folder_location = sys.argv[1]
        print(folder_location)
        converting(folder_location)
    else:
        print('#\n#   USAGE: python minecraft_skin_convert_to_datasets.py [path_of_target_folder] \n' +
        '#   path_of_target_folder: the path of your minecraft skins located\n' +
        '#   * ALL ARGV IS COMPULSORY.\n#')

if __name__ == "__main__":
    main()
    