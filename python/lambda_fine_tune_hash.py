import json
import requests
import json
import re
import time
from transformers import AutoTokenizer
from huggingface_hub import login
import boto3
import random
import jinja2
import numpy

def chat_setup(payload,queryNumber, modelId, json_data = "NotAvailable"):
    if modelId == 'mistralai/Mixtral-8x7B-Instruct-v0.1':
        if queryNumber == 1:
            chat = [
                {"role": "user", "content": "You analyze source materials and distill it down to one word."},
                {"role": "assistant", "content": "I will only return one word without an explanation on what the material is about. I will focus on the general idea of the json not the format. I won't return any puncutation or special characters. What would you like me to do?"},
                {"role": "user", "content": f'Analyze this json and return one word that encompasses the the entire json.  Only return that word.  Here is the Json: {payload}'},
                ]
    if modelId == 'meta-llama/Llama-2-70b-chat-hf':
        if queryNumber == 1:
            chat = [
                {"role": "system", "content": "You analyze source materials and distill it down to one word. You will only return one word without an explanation on what the material is about. The word should focus on the general idea of the json not the format. Do not return any punctuation or special characters."},
                {"role": "user", "content": f'Analyze this json and return one word that encompasses the the entire json.  Only return that word.  Here is the Json: {payload}'},
                ]
    
    return chat

def query(payload, queryNumber, modelId, API_KEY,json_data='NotAvailable',attempt=1 ):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    parameters = {"return_full_text":False,"max_new_tokens":4000}
    options = {"use_cache": False, "wait_for_model": True}
    print(f'TRY START')
    try:
        tokenizer = AutoTokenizer.from_pretrained(modelId)
        print(f'TOKENIZER: ')
        input = tokenizer.apply_chat_template(chat_setup(payload, queryNumber, modelId, json_data), tokenize=False)
        print(f'INPUT: ')
        API_URL = f'https://api-inference.huggingface.co/models/{modelId}'
        print(f'API_URL: ')
        response = requests.post(API_URL, headers=headers, \
                                 json={"inputs":input, "parameters": parameters,"options": options})    
        print(f'STATUS CODE: {response.status_code}')
        if response.status_code != 200:
            print(response.json().get("error_type"), response.status_code)  
            if response.status_code == 429 and attempt < 3:
                time.sleep(3)
                return query(payload, queryNumber, modelId, attempt + 1)
            if response.status_code == 422 and attempt < 3:
                time.sleep(3)
                return query(payload, queryNumber, modelId, attempt + 1)
            return json_data          
        if not response.json()[0].get("generated_text"):
            print("No Text")
            if attempt < 3:
                return query(payload, queryNumber,modelId, attempt + 1)           
            return json_data
        print(f'RESPONSE: {response.json()}')
        return response.json()
    except Exception as e:
        print("An error occurred:", str(e))
        return json_data

def run_inference(): 
    API_KEY = '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'
    login(API_KEY)
    bucket_name = 'garrison-generate-poems'
    prefix_write = 'hashed/'
    prefix_source = 'source/'
    initialModel = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
    secondaryModel = 'meta-llama/Llama-2-70b-chat-hf'
    
    s3 = boto3.client('s3')

    print(f'DOWNLOAD S3_OBJECTKEY')
    s3.download_file(bucket_name, 'objectKey.json', '/tmp/objectKey.json')
    
    with open('/tmp/objectKey.json', 'r') as f:
        s3_objectKey = json.load(f)
    print(f'S3_OBJECTKEY: {str(s3_objectKey)}')
    file_count = len(s3_objectKey["objectKeys"])
    if file_count == 13341:
        return

    s3.download_file(bucket_name, 'objects.json', '/tmp/object.json')

    with open('/tmp/object.json', 'r') as f:
        s3_object = json.load(f)
    # Choose a random object
    object_key = random.choice(s3_object)['Key']
    while object_key in s3_objectKey["objectKeys"]:
        object_key = random.choice(objects)['Key'] 
    print(f'OBJECT KEY: {object_key}')

    s3_objectKey["objectKeys"].append(object_key)
    with open('/tmp/objectKey.json', 'w') as f:
        json.dump(s3_objectKey, f)
    print(f'APPENDED: {s3_objectKey["objectKeys"]}')

    s3.upload_file('/tmp/objectKey.json', bucket_name, 'objectKey.json')

    print(f'UPLOADED')
    s3.download_file(bucket_name, object_key, '/tmp/localfile')
    print(f'DOWNLOADED OBJECT: {object_key}')
    with open('/tmp/localfile', 'r') as f:
        data = json.load(f)
    
    print(f'LOADED: {object_key}') 
    response = query(data, 1, initialModel, API_KEY)
    
    summary_1 = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"
    print(f'SUMMARY 1: {summary_1}')

    '''
    if response == "NotAvailable":
        response = "NotAvailable"
    else:      
        response = query(data, 1, secondaryModel, API_KEY)
    
    summary_2 = response[0]["generated_text"] if response != "NotAvailable" else "NotAvailable"
    print(f'SUMMARY 2: {summary_2}')
    '''
    data["summary_1"] = summary_1
    #data["summary_2"] = summary_2

    
    objects = object_exists(s3, bucket_name, str(file_count) + '.json')
    if objects:
        file_count += 100000
    with open('/tmp/' + str(file_count) + '.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    object_key = prefix_write + str(file_count) + '.json'
    file_path = '/tmp/' + str(file_count) + '.json'

    s3.upload_file(file_path, bucket_name, object_key)

def object_exists(s3, bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except:
        return False

    
def lambda_handler(event, context):

    run_inference()   

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

