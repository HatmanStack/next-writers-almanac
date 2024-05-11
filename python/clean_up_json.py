import json

# Load the main_dictionary from the JSON file
with open('main_dictionary.json', 'r', encoding="utf-8") as f:
    main_dictionary = json.load(f)

# Get the 'day' dictionary
day_dict = main_dictionary['day']

# Sort the values and renumber the keys
sorted_values = sorted(day_dict.values())
renumbered_day_dict = {str(i+1): value for i, value in enumerate(sorted_values)}

# Update the 'day' dictionary in the main_dictionary
main_dictionary['day'] = renumbered_day_dict

# Write the updated main_dictionary back to the JSON file
with open('main_dictionary.json', 'w', encoding='utf-8') as file:
    json.dump(main_dictionary, file, indent=4)