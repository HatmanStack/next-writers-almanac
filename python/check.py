import json
import os


with open('randomizedData.json', 'r', encoding='utf-8') as f:
    template = json.load(f)











rootDir = '../../garrison/public/day'
searchDir = '../../garrison/public/poem'

def find_poem(name):
    for i in range(1,6548):
        poem_search = template['poem'][str(i)].replace('.json','')
        file_path = f'{searchDir}/{poem_search}.json'
        
            
        with open(f'{searchDir}/{poem_search}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data['poemtitle'] == name:
            
            return poem_search

def process_files(rootDir):
    count = 1
    for dirName, subdirList, fileList in os.walk(rootDir):
        #print(f'Found directory: {dirName}')
        for fname in fileList:
            if fname.endswith('.json'):  # Check if the file is a JSON file
                #print(f'\t{fname}')
                    print(fname)
                    
                    with open(os.path.join(dirName, fname), 'r', encoding='utf-8') as f:
                        data = json.load(f)  # Load the data from the JSON file
                    
                    data['poemid'] = []
                    for title in data['poemtitle']:
                        poem_id = find_poem(title)
                        
                        if poem_id is not None:
                            data['poemid'].append(poem_id)
                    
                          
                   
                            
                        with open(os.path.join(dirName, fname), 'w', encoding='utf-8') as f:
                            json.dump(data, f,indent=4)  # Write the transformed data back to the JSON file
         
            

process_files(rootDir)