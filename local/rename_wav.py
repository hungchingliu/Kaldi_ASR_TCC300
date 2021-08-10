import os
import sys
import shutil

def rename_data_with_group(path, target):


    for group_dir in os.listdir(path):
        group_path = os.path.join(path, group_dir)
        if group_dir[-2] == 'G':
            group_num = int(group_dir[-1:])
        elif group_dir[-3] == 'G':
            group_num = int(group_dir[-2:])
        for file in os.listdir(group_path):
            file_path = os.path.join(group_path, file)
            new_file_name = file[0:3] + "{:0>2d}".format(group_num) + file[3:]
            shutil.copy(file_path, os.path.join(target, new_file_name))



if __name__ == "__main__":
    if(len(sys.argv) == 3):
        path, target = sys.argv[1], sys.argv[2]
        rename_data_with_group(path, target)
