import os
import shutil

def flatten_folder(folder_path, output_folder):
    for root, dirs, files in os.walk(folder_path):
        print(root)
        for file in files:
            shutil.move(os.path.join(root, file), os.path.join(output_folder, file))

# Replace with your actual folder paths
folder_path = '../../garrison/public/public/day/'
output_folder = '../../garrison/public/public/flatten/'

flatten_folder(folder_path, output_folder)