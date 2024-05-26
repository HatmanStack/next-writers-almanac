import os
import json
import re
import subprocess
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

def transform_data(writeData, readData):
    writeData['summary3'] = readData['summary_3']
    
    return writeData    
    
API_KEY = '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'
login(API_KEY)
# Specify the directory you want to start from
rootDir = '../../garrison/public/author'

#with open('poets.json', encoding="UTF-8") as f:
#    poet_data = json.load(f)

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
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(modelId)
        
        input = tokenizer.apply_chat_template(chat_setup(payload, queryNumber, modelId, json_data), tokenize=False)
        
        API_URL = f'https://api-inference.huggingface.co/models/{modelId}'
        
        response = requests.post(API_URL, headers=headers, \
                                 json={"inputs":input, "parameters": parameters,"options": options}, timeout=5)    
        print(f'STATUS CODE: {response.status_code}')
        if response.status_code != 200:
            print(response.json().get("error_type"), response.status_code) 
            return 'NotAvailable' 
        return response.json()
    except Exception as e:
        print("An error occurred:", str(e))
        return json_data


def run_inference(data, i): 
    
    
    initialModel = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
    #initialModel = 'meta-llama/Llama-2-70b-chat-hf'
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
    #data["summary_1"] = summary_1
    data[i] = summary_1

    return data


def process_files():
    summary1 = 0
    summary2 = 0
    summary3 = 0
    summary4 = 0
    arr = []
    summaries = ['summary1', 'summary2', 'summary3', 'summary4']
    for dirName, subdirList, fileList in os.walk('./combined'):
        #print(f'Found directory: {dirName}')
        for fname in fileList:
            
            if fname.endswith('.json'):  # Check if the file is a JSON file
                #print(f'\t{fname}')
                
                with open('./combined/' + fname, 'r', encoding='utf-8') as file:
                    data = json.load(file)  # Load the data from the JSON file
                #if data['biography'] == "NotAvailable":
                #transform_data(data)
                
                #for dirNameSource, subdirListSource, fileListSource in os.walk('./summary3'):
                #    for sourcename in fileListSource:
                #        if sourcename.endswith('.json'): 
                
                for i in summaries:
                    if i in data.keys():
                        
                        if len(data[i]) > 25:
                            
                            
                            if i == 'summary1':
                                summary1 += 1
                            if i == 'summary2':
                                summary2 += 1
                            if i == 'summary3':
                                summary3 += 1
                            if i == 'summary4':
                                print(data[i])
                                summary4 += 1

                '''
                with open('./combined/' + fname, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4) 
                            


                
                            if 'data_keys' in sourceData.keys():
                                sourceData['datakeys'] = sourceData['data_keys']
                            if 'data_keys' in data.keys():
                                data['datakeys'] = data['data_keys']
                            if sourceData['datakeys']['poem'] == data['datakeys']['poem']:
                                if sourceData['datakeys']['author'] == data['datakeys']['author']:
                                    if sourceData['datakeys']['day'] == data['datakeys']['day']:
                                        
                            
                            
                                        
                                        if sourceData['generate_answer'] == data['generate_answer']:
                                            
                                            if sourceData['generate_question'] == data['generate_question']:
                                                
                                                writeData = transform_data(data, sourceData)
                                                with open('./combined/' + fname, 'w') as f:
                                                    json.dump(writeData, f, indent=4) 
                            
                                                break
                '''             
    print(f'summary1:  {summary1}')
    print(f'summary2:  {summary2}')
    print(f'summary3:  {summary3}') 
    print(f'summary4:  {summary4}')              
                 
                
                #if test in poetBio.keys():
                    #data['biography'] = poetBio[test]['reflected_response']
                    #print(data['poet'])
                #transform_data(data)
                    
                    #print(data['poet'])
                #data = transform_data(data, count)  # Transform the data
                
    
     # Write the transformed data back to the JSON file
   
process_files()

#with open('poembyline', 'w') as f:
#                json.dump(poet_data, f) 


