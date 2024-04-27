import json
import os
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote


with open('poemlist.json', 'r', encoding='utf-8') as f:
    poemlist = json.load(f)

rootDir = 'C:\\Users\\Whom\\Desktop\\GarrisonNew\\public'
poem_folder = 'C:\\Users\\Whom\\Desktop\\GarrisonNew\\public\\apoem'


def process_files(rootDir):
    count = 1
    for dirName, subdirList, fileList in os.walk(rootDir):
        #print(f'Found directory: {dirName}')
        for fname in fileList:
            if fname.endswith('.json'):  # Check if the file is a JSON file  
                #sketch = fname.split('.')[0]
                #if int(sketch) > 19960301:
                    #if fname == '19960323.json':           
                    if fname == '20001101.json':
                        return
                    with open(os.path.join(dirName, fname), 'r', encoding='utf-8') as f:
                        data = json.load(f)  # Load the data from the JSON file
                    
                    for i in range(len(data['poem'])):
                        
                        if data['poem'][i] != "NotAvailable": 
                            
                                                                    
                            key = next((k for k, v in poemlist.items() if v == data['poemtitle'][i]), None)
                            if data['poemtitle'][i] == '812 A Light exists in Spring':
                                print(key)
                            if key is not None:
                                with open(os.path.join(poem_folder, key+'.json'), 'r', encoding='utf-8') as f:
                                    poem_data = json.load(f)
                                if poem_data['poem'] == 'NotAvailable':
                                    
                                    poem_data['poem'] = data['poem'][i]
                                    with open(os.path.join(poem_folder, key+'.json'), 'w', encoding='utf-8') as f:
                                        json.dump(poem_data, f)
        print(count)



process_files(rootDir)