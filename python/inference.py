import requests
import json
import re
from openai import OpenAI
import huggingface_hub
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()



modelId = "meta-llama/Llama-2-70b-chat-hf/v1/"

API_URL = f'https://api-inference.huggingface.co/models/{modelId}'

#headers = {"Authorization": f"Bearer {token}"}

'''
def query(payload):
    data = {"inputs":payload, "parameters":{"return_full_text": False}, "options":{"wait_for_model": True, "use_cache": True}}
    print(data)
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()
'''
def query(payload):
    client = OpenAI(
    base_url=API_URL,
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    )
    chat_completion = client.chat.completions.create(
        model="tgi",
        messages=[
            {"role": "system", "content": "You write essays for magazines about people's lives"},
            {"role": "user", "content":"Tell me a story"},
        ],
        stream=True,
        max_tokens=6000
    )

    # iterate and print stream
    for message in chat_completion:
        print(message.choices[0].delta.content, end="")



def query1(payload):
    client = InferenceClient(model="meta-llama/Llama-2-70b-chat-hf", token="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")

    output = client.text_generation(payload)
    print(output)

# Load the data from poets.json
with open('poembyline.json', 'r') as f:
    poets = json.load(f)

# Iterate through each entry in poets
def run_inference():
    for poet in poets:
        info = poets[poet]
        
        poetsorg =  "NotAvailable" if info["poets.org"] == "NotAvailable" else re.sub('<.*?>', '', info["poets.org"]["biography"])
        allpoetry = "NotAvailable" if info["all poetry"] == "NotAvailable" else re.sub('<.*?>', '', info["all poetry"]["biography"])
        poetryfoundation = "NotAvailable" if info["poetry foundation"] == "NotAvailable" else re.sub('<.*?>', '', info["poetry foundation"]["biography"])
        wikimeta = "NotAvailable" if info["wikipedia"] == "NotAvailable" else re.sub('<.*?>', '', info["wikipedia"]["poet_meta_data"]) if isinstance(info["wikipedia"]["poet_meta_data"], str) else "NotAvailable"
        wiki = "NotAvailable" if info["wikipedia"] == "NotAvailable" else re.sub('<.*?>', '', info["wikipedia"]["biography"])
        byline = info["writersalmanac"]
        
        variables = [wikimeta, poetsorg, allpoetry, poetryfoundation, wiki]
        data = f'Write a 400 - 800 biography of the poet {poet}. They wrote things like {byline}.\nInclude facts about their life and writing style use relevant information from here {", ".join(variables)}.' 
        def limit_query(data, variables):
            if len(data) <= 15000:
                return data
            else:
                if variables:
                    # Remove the last variable
                    variables.pop()
                    # Generate the new data string
                    data = f'Write a 400 - 800 biography of the poet {poet}. They wrote things like {byline}.\nInclude facts about their life and writing style use relevant information from here {", ".join(variables)}.' 
                    # Recursive call
                    return limit_query(data, variables)
        
        query(limit_query(data, variables))
        return

run_inference()
