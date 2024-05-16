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

warnings.filterwarnings('ignore')

load_dotenv()
API_KEY = os.getenv('HUGGINGFACE_API_KEY')
initialModel = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
secondaryModel = 'meta-llama/Llama-2-70b-chat-hf'

headers = {"Authorization": f"Bearer {API_KEY}"}
parameters = {"return_full_text":False,"max_new_tokens":4000}
options = {"use_cache": False, "wait_for_model": True}
context_window = 128000

with open('main_dictionary.json', 'r') as f:
    rdData = json.load(f)

if len(sys.argv) > 1:
    count = sys.argv[1]
    poemNumber = sys.argv[2]
    authorNumber = sys.argv[3]
    dayNumber = sys.argv[4]

with open('../data/public/poem/' + rdData['poem'][poemNumber], 'r') as f:
    poem = json.load(f)

with open('../data/public/author/' + rdData['author'][authorNumber], 'r') as f:
    author = json.load(f)

with open('../data/public/flatten/' + rdData['day'][dayNumber], 'r') as f:
    day = json.load(f)

def chat_setup(payload,queryNumber, modelId, json_data = "NotAvailable"):
    if modelId == 'mistralai/Mixtral-8x7B-Instruct-v0.1':
        if queryNumber == 1:
            chat = [
                {"role": "user", "content": "You analyze source materials for creative writers. Don't reference the source material."},
                {"role": "assistant", "content": "What would you like me to do?"},
                {"role": "user", "content": f'Choose an idea that would be interesting to generate text from.  \
                Return it in one sentence formed as a question.  The writer will not have access to your source materials. \
                Choose your idea for a creative writing prompt from here : {payload}'},
                ]
        if queryNumber == 2:
            chat = [
                {"role": "user", "content": "You are an expert creative writer that uses unique approaches to different ideas."},
                {"role": "assistant", "content": "What would you like me to write about?"},
                {"role": "user", "content": payload},
                ]
    if modelId == 'meta-llama/Llama-2-70b-chat-hf':
        if queryNumber == 1:
            chat = [
                {"role": "system", "content": "You analyze source materials for creative writers. Don't reference the source material."},
                {"role": "user", "content": f'Choose an idea that would be interesting to generate text from. \
                Return it in one sentence formed as a question. The writer will not have access to your source materials. \
                Choose your idea for a creative writing prompt from here : {payload}'},
                ]
        if queryNumber == 2:
            chat = [
                {"role": "system", "content": "You are an expert creative writer that uses unique approaches to different ideas."},
                {"role": "user", "content": f'Write about about the following topic {payload}'},
                ]
    
    return chat

def query(payload, queryNumber, modelId, json_data='NotAvailable', attempt=1):
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(modelId)
        input = tokenizer.apply_chat_template(chat_setup(payload, queryNumber, modelId, json_data), tokenize=False)
        API_URL = f'https://api-inference.huggingface.co/models/{modelId}'
        
        response = requests.post(API_URL, headers=headers, \
                                 json={"inputs":input, "parameters": parameters,"options": options})
        
        if response.status_code != 200:
            print(response.json().get("error_type"), response.status_code)
            time.sleep(2)
            if attempt == 3:
                return "NotAvailable"
            if response.status_code == 429 and attempt < 5:
                time.sleep(3)
                return query(payload, queryNumber, modelId, attempt + 1)
            if response.status_code == 422:
                time.sleep(3)
            if attempt > 2:
                modelId = "CohereForAI/c4ai-command-r-plus"
            if attempt > 5:
                modelId = "meta-llama/Llama-2-70b-chat-hf"
            if attempt > 7:
                return "NotAvailable"
            return query(payload, queryNumber, modelId, attempt + 1)
        if not response.json()[0].get("generated_text"):
            print("No Text")
            time.sleep(2)
            if attempt < 3:
                return query(payload, queryNumber,modelId, attempt + 1)
            else:
                return "NotAvailable"

        return response.json()
    except Exception as e:
        print("An error occurred:", str(e))
        time.sleep(20)  # Wait for 20 seconds before retrying
        return query(payload, queryNumber,modelId,attempt)

def run_inference():   
    print(f'Count : {count}')
    
    modelIdCreator = secondaryModel if  int(count) % 2 == 0  else initialModel
    modelIdAnswer = initialModel if modelIdCreator == secondaryModel else secondaryModel
    
    with open('inference_fine_tune_generate.json', 'r', encoding='utf-8') as file:
        json_log = json.load(file)

    json_data = 'Anything'
    json_log[count] = {}
    json_log[count]['datakeys'] = {"poem":poemNumber, "author":authorNumber, "day":dayNumber}
   
    response = query(sources(), 1, modelIdCreator, json_data)
    
    json_log[count]["generate_question"] = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"
    
    #print(f'Question:   {json_log[count]["generate_question"]}')

    pattern = r"\n\n\n\n"
    match = re.search(pattern, json_log[count]["generate_question"])
    if match or response == "NotAvailable":
        response = "NotAvailable"
    else:
        response = query(json_log[count]["generate_question"], 2, modelIdAnswer, json_data)
    
    json_log[count]["generate_answer"] = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"
    #print(f'ANSWER:   {json_log[count]["generate_answer"]}')
    with open('inference_fine_tune_generate.json', 'w', encoding='utf-8') as file:
        json.dump(json_log, file, indent=4)


def fewer_sources(data):
    if data[count]['poem'] != 'NotAvailable':
        return data[count]['poem']
    if data[count]['author'] != 'NotAvailable':
        return data[count]['author']
    return data[count]['day']
   

def sources():
    source = ''
    if poem['poem'] != "NotAvailable":
        source += poem['poem']
    if  day['poem'][0] != "NotAvailable":
        source += day['poem'][0]
    else:
        source += str(day['notes'])
    return source

run_inference()
