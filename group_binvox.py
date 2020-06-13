import os
import shutil
import glob

import numpy as np
from PIL import Image

target_folder = '04379243(table)'
combined_path = 'ShapeNetCore.v2/' + target_folder + '/**/texture*.jpg'
file_list = glob.glob('ShapeNetCore.v2/Collection/Texture_table/*', recursive=True)


def group(data):
    print(data.split('/')[2])
    new_folder = 'chair'
    old_path = os.path.splitext(data)[0] + '.solid.binvox'
    new_path = 'ShapeNetCore.v2/Collection/' + new_folder + '/' + data.split('/')[2]

    if not os.path.exists('ShapeNetCore.v2/Collection/' + new_folder):
        os.makedirs('ShapeNetCore.v2/Collection/' + new_folder)
    shutil.copy(data, new_path + '.obj')
    shutil.copy(old_path, new_path + '.binvox')


def texture(path):
    count = 0

    new_file = 'ShapeNetCore.v2/Collection/Texture_table/' + path.split('/')[2] + '_'
    temp = new_file + str(count) + os.path.splitext(path)[-1]

    while os.path.exists(temp):
        count += 1
        temp = new_file + str(count) + os.path.splitext(path)[-1]

    new_file += str(count) + os.path.splitext(path)[-1]
    print(new_file)
    shutil.move(path, new_file)


def filtering(num, path):
    img = Image.open(path)
    data = np.array(img)

    if data.shape[0] < 64 or data.shape[1] < 64:
        print(num, data.shape)
        new_file = 'ShapeNetCore.v2/Collection/no_need/' + os.path.basename(path)
        shutil.move(path, new_file)


if __name__ == "__main__":
    for number, file in enumerate(file_list):
        filtering(number, file)
