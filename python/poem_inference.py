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
parameters = {"return_full_text":False,"max_new_tokens":2000}
options = {"use_cache": False, "wait_for_model": True}
context_window = 50000
output_folder = "C:\\Users\\Whom\\Desktop\\GarrisonNew\\public\\author"

with open('poembyline.json', 'r') as f:
    poets = json.load(f)

if len(sys.argv) > 1:
    count = sys.argv[1]

with open('poems/' + count + '.json', 'r') as f:
    poem = json.load(f)

def chat_setup(payload):
    chat = [
        {"role": "system", "content": "Take a deep breath, You are an expert at writing \
         analysis of poems. You focus on the style of the poet and intersting ideas \
         about the imagery in the poems."},
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
            time.sleep(2)
            if response.status_code == 422:
                time.sleep(3)
            return query(payload)
        if not response.json()[0].get("generated_text"):
            print("No Text")
            time.sleep(2)
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
    print(f'{poem['poemtitle']} : {count}')
    with open('poem_inference_data.json', 'r', encoding='utf-8') as file:
        json_log = json.load(file)

    data = f'Write a 400 - 800 word analysis of the poem {poem['poemtitle']} by \
        {poem['author']} . Give analysis that focuses on the style and if \
        it differs from other works of the author. \
        Here is the poem to analyze: {poem['poem']} ' 
    
    json_log[count] = {}
    if poem['analysis'] != 'NotAvailable':
        json_log[count]['response'] = 'NotAvailable'
        json_log[count]['reflected_response'] = 'NotAvailable'
        json_log[count]['data'] = data
        return
    
    response = query(data)
    json_log[count]["response"] = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"

    pattern = r"\n\n\n\n"
    match = re.search(pattern, json_log[count]["response"])
    if match or response == "NotAvailable":
        reflected_response = "NotAvailable"
    else:
        reflected_response = reflection(response[0]["generated_text"], poem['poemtitle'], poem['author'], poem['poem'])

    json_log[count]["reflected_response"] = reflected_response[0]["generated_text"] if reflected_response != "NotAvailable" else "NotAvailable"
    
    
    with open('poem_inference_data.json', 'w', encoding='utf-8') as file:
        json.dump(json_log, file, indent=4)
    
    poem['analysis'] = json_log[count]["reflected_response"]
    
    
    with open('poem/' +  f"{count}.json", 'w', encoding='utf-8') as f:
            json.dump(poem, f) 
    

def reflection(payload, poemtitle, author, poem):
    data = f"This is an analysis of a poem {poemtitle} by {author}. \
            I will give you the full text of the poem followed by the \
            analysis. Check the analysis for clarity, sentence structure and \
            correctness.  Fix any spelling errors or logic problems you find \
            in the analysis and return the analysis in paragraph form. \
            Do not list any changes. \
            Here is the full text of the poem: {poem} \
            Here is the analysis: {payload}"
    
    reflected_response = query(data)
    
    return reflected_response




run_inference()
