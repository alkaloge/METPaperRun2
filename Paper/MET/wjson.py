import json

# Define the dictionary you want to write to the file
my_dict = {'name': 'John', 'age': 30, 'city': 'New York'}

# Open a file for writing (will create a new file if it doesn't exist)
with open('my_file.json', 'w') as f:
    # Write the dictionary to the file in JSON format
    json.dump(my_dict, f)

