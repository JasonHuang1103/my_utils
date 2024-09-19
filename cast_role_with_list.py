import json
import os

def load_file(file_path):
    result = []
    with open(file_path) as f:
        file = f.readlines()
        for line in file:
            result.append(json.loads(line))
    return result  # Return the list of parsed JSON objects


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


def cast_role_with_list(data):
    if "question" in data:
        data["question"] = [data["question"]]  # Ensure that the 'question' key exists before modifying

def remove_list_layer(data):
    if "question" in data and isinstance(data["question"], list) and len(data["question"]) == 1:
        # If 'question' is a list and contains one item, extract the first item
        data["question"] = data["question"][0]

# load all json files in a directory
def load_all_json_files(directory):
    result = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            result.append(load_file(os.path.join(directory, file)))
    return result

#--------------------------------------------------#

extra = ["BFCL_v3_multi_turn_miss_param.json"]

# Main logic
for file in os.listdir("."):
    if file in extra:
        list_of_dicts = load_file(file)
        if list_of_dicts:  # Make sure list_of_dicts is not empty or None
            for entry in list_of_dicts:
                remove_list_layer(entry)
            # change name to the original name + "_processed"
            write_list_of_dicts_to_file(file, list_of_dicts)

