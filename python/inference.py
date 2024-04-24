import requests
import json
import re
import os
import time
import sys
from transformers import AutoTokenizer
from huggingface_hub import login
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('HUGGINGFACE_API_KEY')
login(API_KEY)
modelId = "CohereForAI/c4ai-command-r-plus"

tokenizer = AutoTokenizer.from_pretrained(modelId)
API_URL = f'https://api-inference.huggingface.co/models/{modelId}'


headers = {"Authorization": f"Bearer {API_KEY}"}
parameters = {"return_full_text":False,"max_new_tokens":1500}
options = {"use_cache": False, "wait_for_model": True}
context_window = 50000
output_folder = "C:\\Users\\Whom\\Desktop\\GarrisonNew\\public\\author"

with open('poembyline.json', 'r') as f:
    poets = json.load(f)
    poets_array = list(poets.keys())

if len(sys.argv) > 1:
    count = int(sys.argv[1])

def chat_setup(payload):
    chat = [
        {"role": "system", "content": "You are an expert at writing biographies of poets. \
          They focus on the style of the poet and intersting facts about their life."},
        {"role": "user", "content": payload},
        ]
    return chat

def query(payload, attempt=1):
    try:
        input = tokenizer.apply_chat_template(chat_setup(payload), tokenize=False)
        response = requests.post(API_URL, headers=headers, \
                                 json={"inputs":input, "parameters": parameters,"options": options})
        
        if response.status_code != 200:
            print(response.json().get("error_type"), response.status_code)
            time.sleep(20)
            if response.status_code == 422:
                time.sleep(300)
            return query(payload)
        if not response.json()[0].get("generated_text"):
            print("No Text")
            time.sleep(20)
            if attempt < 3:
                return query(payload, attempt + 1)
            else:
                return "NotAvailable"

        return response.json()
    except Exception as e:
        print("An error occurred:", str(e))
        time.sleep(20)  # Wait for 20 seconds before retrying
        return query(payload, attempt)

def run_inference():   
    poet = poets_array[count]
    info = poets[poet]
    print(f'{poet} : {count}')
    poetsorg =  "NotAvailable" if info["poets.org"] == "NotAvailable" else re.sub('<.*?>', '', info["poets.org"]["biography"])
    allpoetry = "NotAvailable" if info["all poetry"] == "NotAvailable" else re.sub('<.*?>', '', info["all poetry"]["biography"])
    poetryfoundation = "NotAvailable" if info["poetry foundation"] == "NotAvailable" else re.sub('<.*?>', '', info["poetry foundation"]["biography"])
    wikimeta = "NotAvailable" if info["wikipedia"] == "NotAvailable" else re.sub('<.*?>', '', info["wikipedia"]["poet_meta_data"]) if isinstance(info["wikipedia"]["poet_meta_data"], str) else "NotAvailable"
    wiki = "NotAvailable" if info["wikipedia"] == "NotAvailable" else re.sub('<.*?>', '', info["wikipedia"]["biography"])
    byline = info["writersalmanac"]
    
    variables = [var for var in [wikimeta, poetsorg, allpoetry, poetryfoundation, wiki] if var != "NotAvailable"]
    
    data = f'Write a 400 - 800 word biography of the poet {poet}. They wrote \
        things like {byline}. Supplement your biography with any relevant \
        information from the following: {", ".join(variables)}.' 
    def limit_query(data, variables):
        word_count = len(data.split())
        if word_count <= context_window:
            return data
        else:
            if variables:
                variables.pop()
                data = f'Write a 400 - 800 word biography of the poet {poet}. \
                    They wrote things like {byline}.\nInclude facts about their life \
                    and writing style use relevant information from \
                    the following: {", ".join(variables)}.' 
                return limit_query(data, variables)
    
    
    response = query(limit_query(data, variables))

    with open('data.json', 'r') as file:
        json_log = json.load(file)
    
    json_log[poet] = {}
    json_log[poet]["data"] = data
    json_log[poet]["response"] = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"

    pattern = r"\n\n\n\n"
    match = re.search(pattern, json_log[poet]["response"])
    if match or response == "NotAvailable":
        reflected_response = "NotAvailable"
    else:
        reflected_response = reflection(response[0]["generated_text"])

    json_log[poet]["reflected_response"] = reflected_response[0]["generated_text"] if reflected_response != "NotAvailable" else "NotAvailable"
    
    
    with open('data.json', 'w') as file:
        json.dump(json_log, file, indent=4)
    
    holder = {}
    holder["poet"] = poet
    holder["photos"] = {}
    holder["poems"] = {}
    holder["biography"] = reflected_response[0]["generated_text"] if reflected_response != "NotAvailable" else "NotAvailable"
    sources = ["poets.org", "all poetry", "poetry foundation", "wikipedia"]
    source_variables = [poetsorg, allpoetry, poetryfoundation, wiki]

    for source_var, source_name in zip(source_variables, sources):
        if source_var != "NotAvailable":
            if source_name == "poetry foundation" and poets[poet][source_name]["photo"] not in ["None", "NotAvailable"]:
                holder["photos"][source_name.replace(" ", "")] = poets[poet][source_name]["photo"][3]  
            elif poets[poet][source_name]["photo"] not in ["None", "NotAvailable"]:
                holder["photos"][source_name.replace(" ", "")] = poets[poet][source_name]["photo"]
            if poets[poet][source_name]["poems"] not in ["None", "NotAvailable"]:
                holder['poems'][source_name.replace(" ", "")] = poets[poet][source_name]["poems"]

    
    with open(os.path.join(output_folder, f"{poet}.json"), 'w') as f:
            json.dump(holder, f) 
    

def reflection(payload):
    data = "Check this response for clarity, sentence structure and \
                                correctness.  Fix any spelling errors or logic problems you find \
                                and return the response in a paragraph form. \
                                Do not list any changes. \
                                Here is the Text to check : " + payload
    
    reflected_response = query(data)
    
    return reflected_response




run_inference()
