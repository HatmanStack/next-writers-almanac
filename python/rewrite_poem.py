import json
import os


# Load the main JSON file
with open('poem_inference_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Iterate over each entry in the JSON file
for key, value in data.items():
    # Prefer the 'response' if it contains '++++' or '||||', otherwise use 'reflected_response'
    preferred = value['response'] if '++++' in value['response'] or '||||' in value['response'] else value['reflected_response']

    # If the preferred string contains '||||', use it as is
    if '||||' in preferred:
        transformed = preferred
    else:
        # If the preferred string contains ':' in the first 100 characters, split at ':' and use the second part
        if ':' in preferred[:100]:
            split = preferred[:100].split(':')
            #get the last element of the split list
            holder = split[1]
            
            transformed = ''.join(holder) + preferred[100:]
        # If the preferred string contains '<|CHATBOT_TOKEN|>', split at it and use the second part
        elif '<|CHATBOT_TOKEN|>' in preferred:
            transformed = preferred.split('<|CHATBOT_TOKEN|>')[1]
        else:
            transformed = preferred

    # Load the corresponding JSON file
    with open(os.path.join('../../garrison/public/poem', f'{key}.json'), 'r', encoding='utf-8') as f:
        file_data = json.load(f)

    # Update the "analysis" key with the transformed string
    file_data['analysis'] = transformed
    # After the transformation logic
    transformed = transformed.replace('++++', '').replace('||||', '')
    transformed = transformed[:10].replace('\n', '') + transformed[10:].replace('\n\n', '<br><br>').replace('\n', ' ')
    
    # Write the updated data back to the file
    with open(os.path.join('../../garrison/public/poem', f'{key}.json'), 'w', encoding='utf-8') as f:
        json.dump(file_data, f, indent=4)

