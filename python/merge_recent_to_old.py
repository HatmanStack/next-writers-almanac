import json
import os
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote

rootDir = 'C:\\Users\\Whom\\Desktop\\GarrisonNew\\public'
baseDir = '../../../GarrisonNew/public/'

def get_path(data):
    year_folder = data[:4]
    month_folder = data[5:7]
    path = baseDir + year_folder + '/' + month_folder + '/' + data + '.json'
    return path

def process_files(rootDir):
    count = 1
    
    for dirName, subdirList, fileList in os.walk(rootDir):
        #print(f'Found directory: {dirName}')
        for fname in fileList:
            if fname.endswith('.json'):
                if fname == '20001101.json':
                        return
                
                with open(os.path.join(dirName, fname), 'r', encoding="utf-8") as f:
                    data = json.load(f)                 
                    if data['poem'] != 'NotAvailable': #and len(data['dates']) > 1:
                        for i in range(len(data['poem'])):
                            if '©' in data['poem'][i]:
                                print(fname)
                                data['poem'][i] = data['poem'][i].split('Copyright ©')[0]
                            if '©' in data['poem'][i]:
                                data['poem'][i] = data['poem'][i].split('copyright ©')[0]
                            if '©' in data['poem'][i]:
                                data['poem'][i] = data['poem'][i].split('©')[0]
                            
                            with open(os.path.join(dirName, fname), 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=4)
                        '''
                        for i in reversed(range(len(data['dates']))):
                            fresh_path = get_path(data['dates'][i])
                            if os.path.exists(fresh_path):
                                with open(fresh_path, 'r', encoding='utf-8') as f:
                                    fresh_data = json.load(f)
                                    for j in range(len(fresh_data['poemtitle'])):
                                        if fresh_data['poemtitle'][j] == data['poemtitle']:
                                            if found:
                                                fresh_data['poem'][j] = holder_poem                                             
                                            if fresh_data['poem'][j] != 'NotAvailable':
                                                found = True
                                                holder_poem = fresh_data['poem'][j]
                                                data['poem'] = fresh_data['poem'][j]
                                                with open(os.path.join(dirName, fname), 'w', encoding='utf-8') as f:
                                                    json.dump(data, f, ensure_ascii=False, indent=4)
                                            with open(fresh_path, 'w', encoding='utf-8') as f:
                                                json.dump(fresh_data, f, indent=4)
                            '''            
        print(count)                
                            
                 




process_files(rootDir)