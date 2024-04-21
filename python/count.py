import json

def count_not_available(json_data):
    count = 0
    
    for poet in json_data:
        holder = 0
        for key, value in json_data[poet].items():
            if value == "NotAvailable":
                holder += 1
        if holder == 4:
            count += 1
    return count

# Load JSON data
with open('poets.json') as f:
    data = json.load(f)
    

# Count "NotAvailable" values
count = count_not_available(data)
print(f'Number of "NotAvailable" values: {count}')