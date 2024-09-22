import json
import os

def load_file(file_path):
    result = []
    # Open the file in read mode
    with open(file_path) as f:
        file = f.readlines()
        for line in file:
            # Parse each line as JSON and append it to the result list
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