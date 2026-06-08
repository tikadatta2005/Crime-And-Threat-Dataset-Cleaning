import os

def count_files_per_dir(root_dir):
    result = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        result[dirpath] = len(filenames)

    return result