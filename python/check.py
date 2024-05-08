import json
import os















bad = ['Hillaire Belloc,' 'John Ormand', 'Lewis Carol', 'Timrod. Henry', 'W.D. Snodgrass', 'William Strafford']
good = ['Hilaire Belloc', 'John Ormond','Lewis Carroll', 'Henry Timrod', 'W. D. Snodgrass', 'William Stafford']
rootDir = '../../garrison/public/day'
def process_files(rootDir):
    count = 1
    for dirName, subdirList, fileList in os.walk(rootDir):
        #print(f'Found directory: {dirName}')
        for fname in fileList:
            if fname.endswith('.json'):  # Check if the file is a JSON file
                #print(f'\t{fname}')
                
                    if fname == '20001101.json':
                        return
                    with open(os.path.join(dirName, fname), 'r', encoding='utf-8') as f:
                        data = json.load(f)  # Load the data from the JSON file
                    for i in range(len(data['author'])):
                        
                        for j in range(len(bad)):
                            
                                 
                            if data['author'][i] == bad[j]:
                                  data['author'][i] = good[j]
                                  
                                  with open(os.path.join(dirName, fname), 'w', encoding='utf-8') as f:
                                    json.dump(data, f,  indent=4) 
                    for k in range(len(bad)):
                        if bad[k] in data['poembyline']:
                            data['poembyline'] = data['poembyline'].replace(bad[k], good[k])
                            with open(os.path.join(dirName, fname), 'w', encoding='utf-8') as f:
                                json.dump(data, f,  indent=4) 

                            

                            
                        #with open(os.path.join(dirName, fname), 'w', encoding='utf-8') as f:
                        #    json.dump(data, f,indent=4)  # Write the transformed data back to the JSON file
         
            

process_files(rootDir)