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
modelId = "CohereForAI/c4ai-command-r-plus"

tokenizer = AutoTokenizer.from_pretrained(modelId)
API_URL = f'https://api-inference.huggingface.co/models/{modelId}'


headers = {"Authorization": f"Bearer {API_KEY}"}
parameters = {"return_full_text":False,"max_new_tokens":50000}
options = {"use_cache": False, "wait_for_model": True}
context_window = 128000
output_folder = "C:\\Users\\Whom\\Desktop\\GarrisonNew\\public\\author"

with open('randomizedData.json', 'r') as f:
    rdData = json.load(f)

if len(sys.argv) > 1:
    count = sys.argv[1]
    authorNumber = sys.argv[2]
    poemNumber = sys.argv[3]
    dayNumber = sys.argv[4]

with open('poems/' + rdData['poem'][poemNumber], 'r') as f:
    poem = json.load(f)

with open('author/' + rdData['author'][authorNumber], 'r') as f:
    author = json.load(f)

with open('days/' + rdData['day'][dayNumber], 'r') as f:
    day = json.load(f)

def chat_setup(payload,type):
    if type == 1:
        chat = [
            {"role": "system", "content": "You are an expert at writing questions for an Assistant. \
            The response should not contain any tokens other than the question"},
            {"role": "user", "content": payload},
            ]
    if type == 2:
        chat = [
            {"role": "system", "content": "You are an expert at researching and retrieving information. \
            You are a helpful assistant but are not eager or overbearing.  You are reserved and have a dry sense \
            of humor. The response should not contain any tokens other than the answer"},
            {"role": "user", "content": payload},
            ]
    return chat

def query(payload, type,attempt=1):
    try:
        input = tokenizer.apply_chat_template(chat_setup(payload, type), tokenize=False)
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
    print(f'Count : {count}')
    print(f'Poem : {poem}')
    print(f'Author : {author}')
    print(f'Day : {day}')
    with open('fine_tune.json', 'r', encoding='utf-8') as file:
        json_log = json.load(file)

    data = f'Create a question for an Assistant.  The response should \
        not contain any tokens other than the question. Use the following  \
        three jsons as sources for the question: {poem}, {author}, {day}' 
    
    json_log[count] = {}
    json_log[count]['datakeys'] = {"poem":poemNumber, "author":authorNumber, "day":dayNumber}
    json_log[count]['system'] = 'NotAvailable'
    json_log[count]['user'] = 'NotAvailable'
    json_log[count]['assistant'] = 'NotAvailable'
    
    response = query(data, 1)
    json_log[count]["user"] = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"

    data = f'{json_log[count]["user"]}. The response should \
        not contain any tokens other than the answer. Use the following  \
        three jsons as sources for the answer: {poem}, {author}, {day}' 

    pattern = r"\n\n\n\n"
    match = re.search(pattern, json_log[count]["question"])
    if match or response == "NotAvailable":
        response = "NotAvailable"
    else:
        response = query(data, 2)

    json_log[count]["assistant"] = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"
     
    with open('fine_tune.json', 'w', encoding='utf-8') as file:
        json.dump(json_log, file, indent=4)
    

run_inference()
