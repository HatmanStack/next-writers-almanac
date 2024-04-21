import os
import json
import re

def transform_data(data):
    
    for poet in data['author']:
        if poet not in poet_data:
            continue
        working_data = poet_data[poet]
        cleaned_poembyline = re.sub('<.*?>', '', data['poembyline'])
        
        working_data['writersalmanac'] = cleaned_poembyline
        poet_data[poet] = working_data
        

# Specify the directory you want to start from
rootDir = '../../../Garrison/public'

with open('poets.json', encoding="UTF-8") as f:
    poet_data = json.load(f)

def process_files(rootDir, poet_data):
    for dirName, subdirList, fileList in os.walk(rootDir):
        #print(f'Found directory: {dirName}')
        for fname in fileList:
            if fname.endswith('.json'):  # Check if the file is a JSON file
                print(f'\t{fname}')
                if fname == 'A. A. Milne.json':
                    return
                with open(os.path.join(dirName, fname), 'r', encoding='utf-8') as f:
                    data = json.load(f)  # Load the data from the JSON file

                data = transform_data(data)  # Transform the data
                
                #with open(os.path.join(dirName, fname), 'w') as f:
                #    json.dump(data, f)  # Write the transformed data back to the JSON file

process_files(rootDir, poet_data)

with open('poembyline', 'w') as f:
                json.dump(poet_data, f) 