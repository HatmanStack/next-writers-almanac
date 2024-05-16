import os
import json
import requests
from urllib.parse import urlparse

# Define the directory with the JSON files and the output directory
json_dir = '../../garrison/public/test'
output_dir = '../../garrison/public/image'


def download_image(url, output_dir, retries=1):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers, stream=True)
        
        response.raise_for_status()

        # Get the file name from the URL
        url_path = urlparse(url).path
        image_filename = os.path.basename(url_path.split('/')[-1])

        # Save the image to the output directory
        image_path = os.path.join(output_dir, f'{image_filename}')
        with open(image_path, 'wb') as image_file:
            for chunk in response.iter_content(chunk_size=8192):
                image_file.write(chunk)

        return image_path,  response.status_code

    except requests.exceptions.RequestException as e:
        print(f'Error downloading image from {url}')

        # If there was an error and we haven't retried yet, try again without the query parameters
        if retries > 0 and isinstance(e, requests.exceptions.HTTPError) and e.response.status_code != 404:
            base_url = url.split('?')[0]
            return download_image(base_url, output_dir, retries - 1)

        return None, e.response.status_code if isinstance(e, requests.exceptions.HTTPError) else None

    
    
# Iterate over the JSON files in the directory
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        filepath = os.path.join(json_dir, filename)

        # Open the JSON file and load its contents
        with open(filepath, 'r+') as file:
            print(filename)
            data = json.load(file)
            
            # Get the photo URLs
            photos = data.get('photos', {})
            keys_to_delete = []
            for key, value in photos.items():
                if isinstance(value, dict) and 'image' in value and isinstance(value['image'], str):
                    url = value['image']
                elif isinstance(value, str):
                    url = value
                else:
                    continue

                if key == 'allpoetry':
                    url_parts = url.split('//', 2)
                    if len(url_parts) > 2:
                        url = 'https://' + url_parts[2]

                image_path, status_code = download_image(url, output_dir)

                url = urlparse(url).path
                image_filename = os.path.basename(url.split('/')[-1])
                if 'media' not in data:
                    data['media'] = []
                if image_path is not None and status_code != 404:
                    # Change the URL in the original JSON to point to the new image file
                    data['media'].append(image_filename)
                

            
                    # Write the updated JSON data back to the file
            file.seek(0)
            json.dump(data, file)
            file.truncate()