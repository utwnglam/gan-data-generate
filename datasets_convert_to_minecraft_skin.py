import numpy as np
from PIL import Image

import os
import sys
import glob

def interpolation(data):
    return_list = []
    for row_in_data in range(0, data.shape[0], 16):
        for col_in_data in range(0, data.shape[1], 16):
            rgba = data[row_in_data][col_in_data]
            r = g = b = 0
            for row_in_current_interpolation in range(16):
                for col_in_current_interpolation in range(16):
                    rgba = data[row_in_data + row_in_current_interpolation][col_in_data + col_in_current_interpolation]
                    r = r + rgba[0]
                    g = g + rgba[1]
                    b = b + rgba[2]
            r = r / (16*16) 
            g = g / (16*16) 
            b = b / (16*16)  
            if(r >= 128 and g >= 128 and b>= 128): # which mean that pixel is transparent
                return_list.append([255,255,255,0])
            else:
                return_list.append([r * 2,g * 2,b * 2,255])
    return_list = np.uint8(return_list)
    return_list = np.asarray(return_list)           
    return_list = return_list.reshape((64, 64, 4))
    return return_list

def converting(folder_location):
    count = 0
    file_list = glob.glob(folder_location + '/*.png')
    for file in file_list:
        print('converting ' + file + ' ' + str(count))
        img = Image.open(file)
        data = np.array(img)
        after_interpo = interpolation(data)
        new = Image.fromarray(after_interpo)
        count = count + 1
        new.save('convert_back_to_dataset/' + folder_location +'/convert_back_' + str(count) + ".png")
    print('done')

def main():
    if not os.path.exists('convert_back_to_dataset'):
            os.makedirs('convert_back_to_dataset')
    
    if len(sys.argv) == 2:
        print(sys.argv)
        folder_location = sys.argv[1]
        print(folder_location)
        if not os.path.exists('convert_back_to_dataset/' + folder_location):
            os.makedirs('convert_back_to_dataset/' + folder_location)
        converting(folder_location)
    else:
        print('#\n#   USAGE: python datasets_convert_to_minecraft_skin.py [path_of_target_folder] \n' +
        '#   Path_of_target_folder: the path of your minecraft skins located\n' +
        '#   * ALL ARGV IS COMPULSORY.\n#')

if __name__ == "__main__":
    main()
    