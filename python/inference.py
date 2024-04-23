import requests
import json
import re
from openai import OpenAI
import huggingface_hub
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import time
import sys

load_dotenv()

modelId = "meta-llama/Llama-2-70b-chat-hf"
API_URL = f'https://api-inference.huggingface.co/models/{modelId}'
API_KEY = os.getenv('HUGGINGFACE_API_KEY')

headers = {"Authorization": f"Bearer {API_KEY}"}
parameters = {"return_full_text":False,"max_new_tokens":1000}
options = {"use_cache": False, "wait_for_model": True}

output_folder = "./author"

with open('poembyline.json', 'r') as f:
    poets = json.load(f)
    poets_array = list(poets.keys())

if len(sys.argv) > 1:
    count = int(sys.argv[1])

def query(payload):
    client = OpenAI(
    base_url=API_URL + "/v1/",  
    api_key=API_KEY, 
    )
    chat_completion = client.chat.completions.create(
        model="tgi",
        messages=[
            {"role": "system", "content": "You are an expert at writing biographies"},
            {"role": "user", "content": payload},
        ],
        stream=True,
        max_tokens=1000
        )

    # iterate and print stream
    for message in chat_completion:
        print(message.choices[0].delta.content, end="")

def query1(payload):
    client = InferenceClient(model="meta-llama/Llama-2-70b-chat-hf", token=API_KEY)
    print(client.text_generation(payload,  max_new_tokens=1000))

def query2(payload, attempt=1):
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs":payload, "parameters": parameters,"options": options})
        
        if response.status_code != 200:
            print(response.json().get("error_type"))
            print(response.status_code)
            time.sleep(20)
            if response.status_code == 422:
                time.sleep(300)
            return query2(payload)
        if not response.json()[0].get("generated_text"):
            print("No Text")
            time.sleep(20)
            if attempt < 3:
                return query2(payload, attempt + 1)
            else:
                return "NotAvailable"
        
        return response.json()
    except requests.exceptions.ConnectionError:
        print("Connection aborted. Retrying...")
        time.sleep(20)  # Wait for 20 seconds before retrying
        return query2(payload, attempt)

def run_inference():   
    #for index in range(count, count+2):
        poet = poets_array[count]
        info = poets[poet]
        print(poet)
        poetsorg =  "NotAvailable" if info["poets.org"] == "NotAvailable" else re.sub('<.*?>', '', info["poets.org"]["biography"])
        allpoetry = "NotAvailable" if info["all poetry"] == "NotAvailable" else re.sub('<.*?>', '', info["all poetry"]["biography"])
        poetryfoundation = "NotAvailable" if info["poetry foundation"] == "NotAvailable" else re.sub('<.*?>', '', info["poetry foundation"]["biography"])
        wikimeta = "NotAvailable" if info["wikipedia"] == "NotAvailable" else re.sub('<.*?>', '', info["wikipedia"]["poet_meta_data"]) if isinstance(info["wikipedia"]["poet_meta_data"], str) else "NotAvailable"
        wiki = "NotAvailable" if info["wikipedia"] == "NotAvailable" else re.sub('<.*?>', '', info["wikipedia"]["biography"])
        byline = info["writersalmanac"]
        
        variables = [var for var in [wikimeta, poetsorg, allpoetry, poetryfoundation, wiki] if var != "NotAvailable"]
        
        data = f'Write a 400 - 800 word biography of the poet {poet}. They wrote things like {byline}.\nInclude facts about their life and writing style use relevant information from the following: {", ".join(variables)}.' 
        def limit_query(data, variables):
            word_count = len(data.split())
            if word_count <= 2500:
                return data
            else:
                if variables:
                    # Remove the last variable
                    variables.pop()
                    # Generate the new data string
                    data = f'Write a 400 - 800 word biography of the poet {poet}. They wrote things like {byline}.\nInclude facts about their life and writing style use relevant information from the following: {", ".join(variables)}.' 
                    # Recursive call
                    return limit_query(data, variables)
        
       
        response = query2(limit_query(data, variables))

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
        print(json_log)
        
        with open('data.json', 'w') as file:
            json.dump(json_log, file, indent=4)
        
        holder = {}
        holder["poet"] = poet
        holder["photos"] = {}
        holder["poems"] = {}
        holder["biography"] = reflected_response[0]["generated_text"] if reflected_response != "NotAvailable" else "NotAvailable"
        newVariables = [poetsorg, allpoetry, poetryfoundation, wiki]
        for i in newVariables:
            if i != "NotAvailable":          
                if i == poetsorg and poets[poet]["poets.org"]["photo"] != "None" and poets[poet]["poets.org"]["photo"] != "NotAvailable":
                    holder["photos"]["poetsorg"] = poets[poet]["poets.org"]["photo"]
                if i == poetsorg and  poets[poet]["poets.org"]["poems"] != "None" and  poets[poet]["poets.org"]["poems"] != "NotAvailable":
                    holder['poems']['poetsorg'] = poets[poet]["poets.org"]["poems"]
                if i == allpoetry and poets[poet]["all poetry"]["photo"] != "None" and poets[poet]["all poetry"]["photo"] != "NotAvailable":
                    holder["photos"]["allpoetry"] = poets[poet]["all poetry"]["photo"]
                if i == allpoetry and poets[poet]["all poetry"]["poems"] != "None" and poets[poet]["all poetry"]["poems"] != "NotAvailable":
                    holder['poems']['allpoetry'] = poets[poet]["all poetry"]["poems"]
                if i == poetryfoundation and poets[poet]["poetry foundation"]["photo"] != "None" and poets[poet]["poetry foundation"]["photo"] != "NotAvailable":
                    holder["photos"]["poetryfoundation"] = poets[poet]["poetry foundation"]["photo"][3]
                if i == poetryfoundation and poets[poet]["poetry foundation"]["poems"] != "None" and poets[poet]["poetry foundation"]["poems"] != "NotAvailable":
                    holder['poems']['poetryfoundation'] = poets[poet]["poetry foundation"]["poems"]
                if i == wiki and poets[poet]["wikipedia"]["photo"] != "None" and poets[poet]["wikipedia"]["photo"] != "NotAvailable":
                    holder["photos"]["wikipedia"] = poets[poet]["wikipedia"]["photo"]

        
        with open(os.path.join(output_folder, f"{poet}.json"), 'w') as f:
                json.dump(holder, f) 
    

def reflection(payload):
    data = "Check this response for clarity, sentence structure and \
                                correctness.  Fix any spelling errors or logic problems you find \
                                and return the response in a paragraph form. \
                                Do not list any changes. \
                                If there is nothing in the \"generated_text\" field, please \
                                return \"NotAvailable\". \
                                Here is the Text to check : " + str(payload)
    
    reflected_response = query2(data)
    
    return reflected_response




run_inference()
