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

secondaryModel = 'CohereForAI/c4ai-command-r-plus'
headers = {"Authorization": f"Bearer {API_KEY}"}
parameters = {"return_full_text":False,"max_new_tokens":4000}
options = {"use_cache": False, "wait_for_model": True}
context_window = 128000


with open('main_dictionary.json', 'r') as f:
    rdData = json.load(f)

with open('author_research.json', 'r') as f:
    poembyline = json.load(f)


if len(sys.argv) > 1:
    count = sys.argv[1]
    poemNumber = sys.argv[2]
    authorNumber = sys.argv[3]
    dayNumber = sys.argv[4]

#with open('data/public/poem/' + rdData['poem'][poemNumber], 'r') as f:
#    poem = json.load(f)

with open('../data/public/author/' + rdData['author'][authorNumber], 'r') as f:
    author = json.load(f)

#with open('data/public/flatten/' + rdData['day'][dayNumber], 'r') as f:
#    day = json.load(f)

def chat_setup(payload,queryNumber, modelId, json_data = "NotAvailable"):
    
    if modelId == 'mistralai/Mixtral-8x7B-Instruct-v0.1':
        if queryNumber == 1:
            chat = [
                {"role": "user", "content": "You are an expert at writing Biographies. I'd like you to write me a biography for a poet."},
                {"role": "assistant", "content": "What poet would you like me to write about?"},
                {"role": "user", "content": payload},
                ]
        if queryNumber == 2:
            chat = [
                {"role": "user", "content": "You are an expert at rewriting biographies. Use your editing skills to rewrite this biography of a poet."},
                {"role": "assistant", "content": "Who's the poet and what's the biography"},
                {"role": "user", "content": payload},
                ]
    
    else:   
        if queryNumber == 1:
            chat = [
                {"role": "system", "content": "You are an expert at writing biographies. Write me a biography of this poet."},
                {"role": "user", "content": payload},
                ]
        if queryNumber == 2:
            chat = [
                {"role": "system", "content": "You are an expert at editing biographies. \
                I will give you the information about the person then the biography.  Rewrite the biography."},
                {"role": "user", "content": payload},
                ]
    
    return chat

def query(payload, queryNumber, modelId, json_data='NotAvailable', attempt=1):
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(modelId)
        input = tokenizer.apply_chat_template(chat_setup(payload, queryNumber, modelId, json_data), tokenize=False)
        API_URL = f'https://api-inference.huggingface.co/models/{modelId}'
        print('response')
        response = requests.post(API_URL, headers=headers, \
                                 json={"inputs":input, "parameters": parameters,"options": options})
        
        if response.status_code != 200:
            print(response.json().get("error_type"), response.status_code)
            time.sleep(2)
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
        print('response.json()')
        return response.json()
    except Exception as e:
        print("An error occurred:", str(e))
        time.sleep(20)  # Wait for 20 seconds before retrying
        return query(payload, queryNumber,modelId,attempt)

def run_inference():   
    print(f'Count : {count}')
    
    modelId = secondaryModel if  int(count) % 2 == 0  else initialModel
    
    if author['biography'] != "NotAvailablele":
        return
    
    with open('inference_biography_without_research.json', 'r', encoding='utf-8') as file:
        json_log = json.load(file)
    
    '''
    data = f'Create a question for an Assistant.  The response should \
        not contain any tokens other than the question. Use the following \
        three jsons as sources for the question: {poem}, {author}, {day}' 
    
    
    json_log[count] = {}
    json_log[count]['datakeys'] = {"poem":poemNumber, "author":authorNumber, "day":dayNumber}
    json_log[count]['system'] = 'NotAvailable'
    json_log[count]['user'] = 'NotAvailable'
    json_log[count]['assistant'] = 'NotAvailable'
    '''
    json_data = ''
    json_log[author['poet']] = {}
    
    data = poembyline[author['poet']]['writersalmanac']
    
    response = query(data, 1, modelId, json_data)
    json_log[author['poet']]["poetId"] = count
    json_log[author['poet']]['modelId'] = modelId
    json_log[author['poet']]["response"] = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"
    
    print(f'RESPONSE:   {json_log[author["poet"]]["response"]}')
    holder = json_log[author['poet']]["response"]
    data = f'{data} Here is the proposed biography: {holder}' 

    pattern = r"\n\n\n\n"
    match = re.search(pattern, json_log[author['poet']]["response"])
    if match or response == "NotAvailable":
        response = "NotAvailable"
    else:
        response = query(data, 2, modelId, json_data)
    
    json_log[author['poet']]["reflected_response"] = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"
    #print(f'ANSWER:   {json_data["assistant1"]}')
    author['biography'] = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"
    print(author['biography'])
    with open('inference_biography_without_research.json', 'w', encoding='utf-8') as file:
        json.dump(json_log, file, indent=4)
    

run_inference()
