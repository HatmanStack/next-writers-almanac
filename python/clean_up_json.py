import requests
import json
import re
import os
import time
import sys
from transformers import AutoTokenizer
from huggingface_hub import login
from dotenv import load_dotenv
import warnings

load_dotenv()
API_KEY = os.getenv('HF_API_KEY')
initialModel = 'mistralai/Mixtral-8x7B-Instruct-v0.1'

secondaryModel = 'CohereForAI/c4ai-command-r-plus'
headers = {"Authorization": f"Bearer {API_KEY}"}
parameters = {"return_full_text":False,"max_new_tokens":4000}
options = {"use_cache": False, "wait_for_model": True}
context_window = 128000


initialModel = 'mistralai/Mixtral-8x7B-Instruct-v0.1'

with open('inference_biography_without_research.json', 'r', encoding="utf-8") as f:
    data = json.load(f)


def inference(payload, attempt = 1):
    chat = [
        {"role": "user", "content": "You are an expert at Biographies. I will give you two different biographies of a poet. \
        If the first biography is better return the number 888, this is not a ranking it is a hash.  If the second biography is better \
        return the number 999, this is not a ranking it is a hash. Return only the number."},
        {"role": "assistant", "content": "What are the biographies?"},
        {"role": "user", "content": payload},
        ]

    try:
        tokenizer = AutoTokenizer.from_pretrained(initialModel)
        input = tokenizer.apply_chat_template(chat, tokenize=False)
        API_URL = f'https://api-inference.huggingface.co/models/{initialModel}'
        
        response = requests.post(API_URL, headers=headers, \
                                 json={"inputs":input, "parameters": parameters,"options": options})
        return response.json()
    except Exception as e:
        print("An error occurred:", str(e))
        time.sleep(20)  # Wait for 20 seconds before retrying
        return inference(payload, attempt + 1)


def run_inference():
    for i in data:
        if 'biography' in data[i]:
            continue
        
        response = inference(data[i]['response'] + ' ' + data[i]['reflected_response'])
        
        data[i]['biography'] = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"
        print(data[i]['biography'])
        with open('inference_biography_without_research.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

def alter_files():
    for i in data:
       
        if '888' in data[i]['biography']:
            data[i]['biography'] = data[i]['response']
        elif '999' in data[i]['biography']:
            data[i]['biography'] = data[i]['reflected_response']
            
        
        biography = data[i]['biography'] 
        if ':' in biography[:100]:
            biography = biography.split(':')[1]

        if '<|CHATBOT_TOKEN|>' in biography:
            biography = biography.split('<|CHATBOT_TOKEN|>')[1]
        biography = biography[:50].replace('\n', '') + biography[50:]
        biography = biography.strip()
        biography
        with open( '../../garrison/public/author/' + i + '.json', 'r', encoding='utf-8') as file:
            filedata = json.load(file)
        
        filedata['biography'] = biography
        with open( '../../garrison/public/author/' + i + '.json', 'w', encoding='utf-8') as file:
            json.dump(filedata, file, indent=4)
        


       
    #with open('inference_biography_without_research.json', 'w', encoding='utf-8') as file:
    #    json.dump(data, file, indent=4)

alter_files()
#run_inference()