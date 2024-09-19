import json
import os
import re

def load_file(file_path):
    result = []
    with open(file_path) as f:
        file = f.readlines()
        for line in file:
            result.append(json.loads(line))
    return result

def write_list_of_dicts_to_file(filename, data, subdir=None):
    if subdir:
        # Ensure the subdirectory exists
        os.makedirs(subdir, exist_ok=True)

        # Construct the full path to the file
        filename = os.path.join(subdir, filename)

    # Write the list of dictionaries to the file in JSON format
    with open(filename, "w") as f:
        for i, entry in enumerate(data):
            json_str = json.dumps(entry)
            f.write(json_str)
            if i < len(data) - 1:
                f.write("\n")

# given the file path to a file, sort the file by the value in the key "id"
def sort_json(file_path):
    data = load_file(file_path)
    data.sort(key=lambda x: int(re.search(r'\d+', x['id']).group()))
    write_list_of_dicts_to_file(file_path, data, subdir="")

#--------------------------------------------------#

# Main logic
for file in os.listdir("."):
    if file.endswith(".json"):
        sort_json(file)