import os
import json
import re
import subprocess

def transform_data(data):
    if data['poet'] == 'Liam Rector':
        subprocess.run(["/home/hatman/Desktop/Git/next-writers-almanac/python/venv/bin/python", "inference_biography_with_research.py" , data['poet']])
    
       
with open('holder.json', 'r', encoding='utf-8') as f:
    poetBio = json.load(f)        

# Specify the directory you want to start from
rootDir = '../../garrison/public/author'

#with open('poets.json', encoding="UTF-8") as f:
#    poet_data = json.load(f)

def process_files(rootDir):
    count = 0
    arr = []
    for dirName, subdirList, fileList in os.walk(rootDir):
        #print(f'Found directory: {dirName}')
        
        for fname in fileList:
            
            if fname.endswith('.json'):  # Check if the file is a JSON file
                #print(f'\t{fname}')
                
                with open(os.path.join(dirName, fname), 'r', encoding='utf-8') as f:
                    data = json.load(f)  # Load the data from the JSON file
                #if data['biography'] == "NotAvailable":
                #transform_data(data)
                test = fname.split('.')[0]
                
                
                if test not in poetBio['test']:
                    print(fname)
                
                
                #if test in poetBio.keys():
                    #data['biography'] = poetBio[test]['reflected_response']
                    #print(data['poet'])
                #transform_data(data)
                    
                    #print(data['poet'])
                #data = transform_data(data, count)  # Transform the data
                
    
     # Write the transformed data back to the JSON file
    
process_files(rootDir)

#with open('poembyline', 'w') as f:
#                json.dump(poet_data, f) 