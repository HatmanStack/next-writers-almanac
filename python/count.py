import json
import os
import requests
from bs4 import BeautifulSoup

def count_not_available(json_data):
    count = 0
    
    for poet in json_data:
        holder = 0
        for key, value in json_data[poet].items():
            if value == "NotAvailable":
                holder += 1
        if holder == 4:
            count += 1
    return count

# Load JSON data
with open('new_data.json') as f:
    vs_data = json.load(f)

with open('poembyline.json', 'r' , encoding='utf-8') as f:
    poembyline = json.load(f)
base_url = "https://www.poetryfoundation.org/poets/"
holder = []
def transform_data(data, dirName, fname):
    for i in range(len(data["author"])):
        if data["author"][i] == 'Various Famous Headstones':
            continue
        if data["author"][i] not in vs_data.keys():
            poembyline[data["author"][i]] = {}
            keys = ["poets.org", "poetry foundation" , "all poetry", "wikipedia", "writersalmanac"]
            for j in keys:
                if j == "writersalmanac":
                    poembyline[data["author"][i]][j] = data["poembyline"]
                elif j == "poetry foundation":
                    item = data["author"][i].replace(' ', '-')
                    url = base_url + item
                    response = requests.get(url)
                    if response.status_code == 200:
                        poembyline[data["author"][i]][j] = {}
                        print(data["author"][i])
                        soup = BeautifulSoup(response.text, 'html.parser')
                        if soup.find('p') != None:  
                            poembyline[data["author"][i]][j]["biography"] = str(soup.find('p'))
                        img = soup.find_all('img')
                        for s in img:
                            if 'srcset' in s.attrs:
                                array = str(s.get('srcset')).split(',')
                                
                                poembyline[data["author"][i]][j]["photo"] = array
                    else:
                        poembyline[data["author"][i]][j] = "NotAvailable"   
                else:
                    print(poembyline[data["author"][i]])
                    poembyline[data["author"][i]][j] = "NotAvailable"
                
            
            
        if data["author"][i] == "Louise Gl�ck":
            data["author"][i] = "Louise Gl\u00fcck"
            with open(os.path.join(dirName, fname), 'w') as f:
                json.dump(data, f) 
        if data["author"][i] == "C&eacute;sar Vallejo":
            data["author"][i] = "C\u00e9sar Vallejo"
            with open(os.path.join(dirName, fname), 'w') as f:
                json.dump(data, f) 


rootDir = '../../../GarrisonNew/public/'
poem_write_dir = '../../../GarrisonNew/public/newPoem'

#with open('poets.json', encoding="UTF-8") as f:
#    poet_data = json.load(f)
with open('poemlist.json') as f:
    poemlist = json.load(f)

import os
import json
year = ['1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017']
month = ['01','02','03','04','05','06','07','08','09','10','11','12']
day = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
def get_file_names(poemtitle):
    holder = []
    for x in year:
        for y in month:
            for z in day:
                path = rootDir + x +'/'+ y +'/'+ x+y+z + '.json'
                
                if os.path.exists(path):
                
                    with open(path, 'r', encoding='utf-8') as f:
                        file_data = json.load(f)
                        
                        for i in range(len(file_data['poemtitle'])):
                            
                            if file_data['poemtitle'][i] == poemtitle:
                                
                                holder.append(file_data['filename'])
    return holder

def transform(data):
    for i in range(len(data['poemtitle'])):
        key = next((k for k, v in poemlist.items() if v == data['poemtitle'][i]), None)
        # Construct the path to the JSON file for the current poem
        poem_json_path = os.path.join(poem_write_dir, f"{key}.json")
        
        # Check if the JSON file exists
        if not os.path.exists(poem_json_path):
            holder = {}
            # If the JSON file doesn't exist, find the key in poemlist where the value is data['poemtitle'][i]
            holder['poemId'] = key
            holder['poemtitle'] = data['poemtitle'][i]
            holder['author'] = data['author'][i] if len(data['author']) > 1 else data['author'][0]
            holder['dates'] = get_file_names(data['poemtitle'][i])
            holder['poem'] = data['poem'][i]
            holder['analysis'] = 'NotAvailable' if get_analysis(data['poemtitle'][i]) == None else get_analysis(data['poemtitle'][i])
            print(poem_json_path)
            with open(poem_json_path, 'w' , encoding='utf-8') as f:
                json.dump(holder, f, indent=4) 
            

        
input_folder = "C:\\Users\\Whom\\Desktop\\GarrisonNew\\public\\poem"        
    


def process_files(rootDir):
    count = 1
    for dirName, subdirList, fileList in os.walk(rootDir):
        #print(f'Found directory: {dirName}')
        for fname in fileList:
            if fname.endswith('.json'):  # Check if the file is a JSON file
                #print(f'\t{fname}')
                if fname == 'A. A. Milne.json':
                    return
                with open(os.path.join(dirName, fname), 'r', encoding='utf-8') as f:
                    data = json.load(f)  # Load the data from the JSON file

                data= transform(data)  # Transform the data
                
                #with open(os.path.join(dirName, fname), 'w') as f:
                #    json.dump(data, f)  # Write the transformed data back to the JSON file
                 
def get_analysis(poemtitle): 
    for dirName, subdirList, fileList in os.walk(input_folder):
    #print(f'Found directory: {dirName}')
        for fname in fileList:
            if fname == poemtitle + '.json':
                with open(os.path.join(dirName, fname), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'analysis' in data.keys() and data['analysis'] != 'None':
                            return data['analysis']
                        else:
                            return 'NotAvailable'



process_files(rootDir)
#with open('poemlist.json', 'w' , encoding='utf-8') as f:
#    json.dump(poemlist, f, indent=4) 

# Count "NotAvailable" values
#count = count_not_available(data)
#print(f'Number of "NotAvailable" values: {count}')