import json
import os
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote

rootDir = 'C:\\Users\\Whom\\Desktop\\GarrisonNew\\public'
base_url = ''
with open('google_response.json', 'r', encoding='utf-8') as f:
    google_responses = json.load(f)
 
def transform(data, count, dirName, fname):
    name = fname.split('.json')[0]
    print(name)
    for i in range(len(data['poemtitle'])):
        if data['poem'][i] != 'NotAvailable':
            continue
        poemtitle = data['poemtitle'][i] 
        author = data['author'][i] if len(data['author']) > 1 else data['author'][0] 
        searchterm = poemtitle + ' ' + author
        if "NotAvailable" in searchterm:
                continue
        if i > 0:
            
            name = name + '-' + str(i)
            encoded_url = quote(searchterm)
            google_url = f'https://www.google.com/search?q={encoded_url}'
            google_responses[name] = {}
            google_responses[name]['searchterm'] = searchterm
            google_responses[name]['search_url'] = google_url
            google_responses[name]['response'] = 'NotAvailable'

    
    
            
        google_url = google_responses[name]['search_url']
        
        response = requests.get(google_url.replace('https://www.google.com/search?q=', 'https://search.yahoo.com/search?p=') + '&ia=web')
        time.sleep(2)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            google_responses[name]['yahoo'] = response.text
            ref = ['allpoetry.com', 'poets.org/poem','poetryfoundation.org/poems/']
            for link in soup.find_all('a'):
                
                if data['poem'][i] != 'NotAvailable':
                    break
                link_url = link.get('href')
                for q in ref:
                    if q in link_url:
                        good_link = link_url.split('url?q=')
                        
                        try:
                            response = requests.get(link_url)
                            if response.status_code == 200:
                                soup = BeautifulSoup(response.text, 'html.parser')

                                if q == ref[0]:
                                    div = soup.find('div', class_='preview poem_body')                              
                                    if div is not None:
                                        data['poem'][i] = div.text
                                if q == ref[1]:
                                    div = soup.find('article')
                                    if div is not None:
                                        data['poem'][i] = div.text                          
                                if q == ref[2]:
                                    div = soup.find('div', class_='o-poem ')
                                    if div is not None:
                                        data['poem'][i] = div.text
                                data['poem'][i] = data['poem'][i].replace('\n', '<br>').replace('\n\n', '<br><br>')
                                if data['poem'][i] != 'NotAvailable':
                                    with open(os.path.join(dirName, fname), 'w') as f:
                                        json.dump(data, f)
                                               
            
                        except:
                            print(f'GOOD_LINK:   {good_link}')
     
    
                
            
        '''
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.find('p') != None:  
                poembyline[data["author"][i]][j]["biography"] = str(soup.find('p'))
            img = soup.find_all('img')
            for s in img:
                if 'srcset' in s.attrs:
                    array = str(s.get('srcset')).split(',')  
            data['poem'] = bs4.             
        '''

def process_files(rootDir):
    count = 1
    for dirName, subdirList, fileList in os.walk(rootDir):
        #print(f'Found directory: {dirName}')
        for fname in fileList:
            if fname.endswith('.json'):  # Check if the file is a JSON file
                #print(f'\t{fname}')
                #sketch = fname.split('.')[0]
                #if int(sketch) > 19970423:
                    if fname == '20001101.json':
                        return
                    with open(os.path.join(dirName, fname), 'r', encoding='utf-8') as f:
                        data = json.load(f)  # Load the data from the JSON file
                    
                    data= transform(data, count, dirName, fname)  # Transform the data
                    count += 1
                    #with open(os.path.join(dirName, fname), 'w') as f:
                    #    json.dump(data, f)  # Write the transformed data back to the JSON file


process_files(rootDir)

with open('google_response.json', 'w', encoding='utf-8') as f:
        json.dump(google_responses, f, indent=4) 