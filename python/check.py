import json
import os
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote


rootDir = 'C:\\Users\\Whom\\Desktop\\GarrisonNew\\public'
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
                    for i in range(len(data['poem'])):

                        if data['poem'][i] != 'NotAvailable':
                            count += 1

                            
                        #with open(os.path.join(dirName, fname), 'w', encoding='utf-8') as f:
                        #    json.dump(data, f)  # Write the transformed data back to the JSON file
        print(count)           
            

process_files(rootDir)