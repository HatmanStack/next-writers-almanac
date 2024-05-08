import os
import json

def count_files(directory):
    file_dict = {}
    file_counter = 1
    for r, d, files in os.walk(directory):
        for file in files:
            file_dict[file_counter] = file
            file_counter += 1
    return file_dict

data = {
    'poem': count_files('../../garrison/public/poem'),
    'author': count_files('../../garrison/public/author'),
    'day': count_files('../../garrison/public/day')
}

with open('file_counts.json', 'w') as f:
    json.dump(data, f, indent=4)