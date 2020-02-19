import os
import glob
import argparse


def to_vox(args):
    file_list = glob.glob('BINVOX/IKEA_' + args.folder + '/*')
    print(file_list)

    for file in file_list:
        os.system('./BINVOX/binvox -d 64 ' + file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=str, help='The target IKEA folder to convert')
    args = parser.parse_args()
    to_vox(args)


if __name__ == "__main__":
    main()