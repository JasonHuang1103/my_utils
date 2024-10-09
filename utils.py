import json
import os
import re
from load_write import load_file, write_list_of_dicts_to_file

#--------------------------------------------------#

# given a data entry, cast the value of the key "question" with a list
def cast_list(data):
    if "question" in data:
        data["question"] = [data["question"]]

# given a data entry, remost a layer of list of the value with key "question"
def remove_list(data):
    if "question" in data and isinstance(data["question"], list) and len(data["question"]) == 1:
        data["question"] = data["question"][0]

# given the file path to a json file, sort the file by the values with key "id"
def sort_json(input_file_path, output_file_name, output_loc=""):
    data = load_file(input_file_path)
    data.sort(key=lambda x: int(re.search(r'\d+$', x["id"]).group()))
    write_list_of_dicts_to_file(output_file_name, data, subdir=output_loc)

# given the file path to a json file, reindex the file by the values with key "id"
def reindex_json(input_file_path, output_file_name, output_loc=""):
    data = load_file(input_file_path)
    for i, entry in enumerate(data):
        entry["id"] = re.sub(r'\d+', str(i), entry["id"])
    write_list_of_dicts_to_file(output_file_name, data, subdir=output_loc)

#--------------------------------------------------#

# verify enum format: entries and type must be string
def recursive_find_enum(entry, results, preceding_type=None):
    """Recursively searches for 'enum' in nested dictionaries."""
    if isinstance(entry, dict):
        for key, value in entry.items():
            if key == "type":
                preceding_type = value  # Update the last 'type' encountered

            elif key == "enum":
                # Check the two conditions for adding the entry's 'id'
                if preceding_type != "string" or not all(isinstance(item, str) for item in value):
                    if "id" in entry:
                        results.append(entry.get("id"))

            # Recurse if the value is another dictionary
            if isinstance(value, dict):
                recursive_find_enum(value, results, preceding_type)

def find_invalid_enums(data_entries, output_filename):
    results = []

    # Create 'output' directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the full path for the output file
    output_file_path = os.path.join(output_dir, output_filename)

    # Loop through each entry (each entry is a dictionary) in data_entries (which is a list)
    for entry in data_entries:
        recursive_find_enum(entry, results)  # Recursively find invalid enums

    # Write results (invalid ids) to a text file
    with open(output_file_path, 'w') as file:
        for result in results:
            file.write(str(result) + "\n")
    
    print(f"Invalid enum results have been saved to {output_file_path}")

# Directory containing JSON files
directory_path = "./berkeley-function-call-leaderboard/data"

count = 0
for file_name in os.listdir(directory_path):
    # Check if the file is a JSON file
    if file_name.endswith(".json"):
        count += 1
        print(f"Processing {count}: {file_name}")
        # Construct the full file path
        file_path = os.path.join(directory_path, file_name)
        # Call the load_file function with the file path
        data = load_file(file_path)
        if data:  # Proceed only if data was loaded successfully
            output_filename = f"{file_name}_output.txt"
            find_invalid_enums(data, output_filename)

print(f"Total processed files: {count}")