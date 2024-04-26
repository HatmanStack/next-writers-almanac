import json
import requests
import os
from bs4 import BeautifulSoup

# Load the data from the JSON file
with open('poems_sorted.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

input_folder = "C:\\Users\\Whom\\Desktop\\Garrison\\public\\poem"

output_folder = "C:\\Users\\Whom\\Desktop\\GarrisonNew\\public\\poem"

base_url = "https://allpoetry.com/"

for item in data:
    holder = {}
    try:
        with open(os.path.join(input_folder, f"{item}.json"), 'r') as f:
            input_data = json.load(f)
        holder['writersalmanac'] = input_data
        item = item[:7].translate(str.maketrans('', '', '0123456789')) + item[10:]
        item = item.replace(' ', '-')
        
        url = base_url + item
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')      
            hr_tag = soup.find('hr')
            if hr_tag:
                div_tag = hr_tag.find_next_sibling('div')
                if div_tag:
                    
                    holder['analysis'] = div_tag.text
                    holder['allpoetryurl'] = url
                
                
                
        with open(os.path.join(output_folder, f"{item}.json"), 'w') as f:
            f.write(json.dumps(holder, indent=4))
    except Exception as e:
        print(e)
        print(item)
        continue