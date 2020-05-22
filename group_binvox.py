import os
import shutil
import glob

target_folder = '03001627(chair)'
new_folder = 'chair'

combined_path = 'ShapeNetCore.v2/' + target_folder + '/**/*.obj'
file_list = glob.glob(combined_path, recursive=True)

for file in file_list:
    old_path = os.path.splitext(file)[0] + '.solid.binvox'
    new_path = 'ShapeNetCore.v2/Collection/' + new_folder + '/' + file.split('/')[2]
    print(file.split('/')[2])

    if not os.path.exists('ShapeNetCore.v2/Collection/' + new_folder):
        os.makedirs('ShapeNetCore.v2/Collection/' + new_folder)

    # os.rename(file, new_path + '.obj')
    # os.rename(old_path, new_path + '.binvox')

    shutil.copy(file, new_path + '.obj')
    shutil.copy(old_path, new_path + '.binvox')
