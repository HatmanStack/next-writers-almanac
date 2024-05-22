import requests
import json
import re
import time
from transformers import AutoTokenizer
from huggingface_hub import login
import boto3
import random

API_KEY = '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'
login(API_KEY)
bucket_name = 'garrison-generate-poems'
prefix_generation = 'public/generation/'
initialModel = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
secondaryModel = 'meta-llama/Llama-2-70b-chat-hf'
headers = {"Authorization": f"Bearer {API_KEY}"}
parameters = {"return_full_text":False,"max_new_tokens":4000}
options = {"use_cache": False, "wait_for_model": True}
context_window = 128000

s3 = boto3.client('s3')
object_key = 'main_dictionary'

s3.download_file(bucket_name, object_key, '/tmp/localfile')

with open('/tmp/localfile', 'r') as f:
    rdData = json.load(f)

poemNumber = str(random.randint(1, 6548))
authorNumber = str(random.randint(1, 1583)) 
dayNumber = str(random.randint(1, 9098))

s3.download_file(bucket_name, 'public/poem/' + rdData['poem'][poemNumber], '/tmp/poemfile')
s3.download_file(bucket_name, 'public/author/' + rdData['author'][authorNumber], '/tmp/authorfile')
s3.download_file(bucket_name, 'public/flatten/' + rdData['day'][dayNumber], '/tmp/dayfile')

with open('poemfile', 'r') as f:
    poem = json.load(f)

with open('/tmp/authorfile', 'r') as f:
    author = json.load(f)

with open('tmp/dayfile', 'r') as f:
    day = json.load(f)

def chat_setup(payload,queryNumber, modelId, json_data = "NotAvailable"):
    if modelId == initialModel:
        if queryNumber == 1:
            chat = [
                {"role": "user", "content": "You analyze source materials for poets. Don't reference the source material."},
                {"role": "assistant", "content": "What would you like me to do?"},
                {"role": "user", "content": f'Choose an idea that would be interesting to generate text from.  \
                Return it in one sentence formed as a question.  The writer will not have access to your source materials. \
                Choose your idea for a poem prompt from here : {payload}'},
                ]
        if queryNumber == 2:
            chat = [
                {"role": "user", "content": "You are a poet that uses unique approaches to different ideas."},
                {"role": "assistant", "content": "What would you like me to write about?"},
                {"role": "user", "content": f'Write a poem about the following topic {payload} using this poem as a template {json_data}'}
                ]
    if modelId == secondaryModel:
        if queryNumber == 1:
            chat = [
                {"role": "system", "content": "You analyze source materials for poets. Don't reference the source material."},
                {"role": "user", "content": f'Choose an idea that would be interesting to generate text from. \
                Return it in one sentence formed as a question. The writer will not have access to your source materials. \
                Choose your idea for a poem prompt from here : {payload}'},
                ]
        if queryNumber == 2:
            chat = [
                {"role": "system", "content": "You are a poet that uses unique approaches and exsisting material to create new poems."},
                {"role": "user", "content": f'Write a poem about the following topic {payload}'},
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
                return 'NotAvailable'
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
    
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix_generation)
    file_count = response['KeyCount']
    
    modelIdCreator = secondaryModel if  file_count % 2 == 0  else initialModel
    modelIdAnswer = initialModel if modelIdCreator == secondaryModel else secondaryModel
    
    json_data = 'Anything'
    json_log = {}
    json_log['datakeys'] = {"poem":poemNumber, "author":authorNumber, "day":dayNumber}
    inferenceData, havePoem = sources()
    response = query(inferenceData, 1, modelIdCreator, json_data)
    
    json_log["generate_question"] = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"
    
    #print(f'Question:   {json_log["generate_question"]}')

    pattern = r"\n\n\n\n"
    match = re.search(pattern, json_log["generate_question"])
    if match or response == "NotAvailable":
        response = "NotAvailable"
    else:
        if havePoem:
           json_data = day['poem'][0] 
           modelIdAnswer = initialModel
        else:
           modelIdAnswer = secondaryModel
           
        response = query(json_log["generate_question"], 2, modelIdAnswer, json_data)
    
    json_log["generate_answer"] = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"
    
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix_generation)
    file_count = response['KeyCount']

    with open('/tmp/' + file_count + '.json', 'w', encoding='utf-8') as file:
        json.dump(json_log, file, indent=4)
    object_key = prefix_generation + file_count + '.json'
    file_path = '/tmp/' + file_count + '.json'

    s3.upload_file(file_path, bucket_name, object_key)
    

def sources():
    source = ''
    havePoem = False
    if poem['poem'] != "NotAvailable":
        source += poem['poem']
    if  day['poem'][0] != "NotAvailable":
        havePoem = True
        source += day['poem'][0]
    else:
        source += str(day['notes'])
    return source, havePoem

run_inference()

