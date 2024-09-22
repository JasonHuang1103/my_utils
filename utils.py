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