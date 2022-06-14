#!/bin/python3
import json
import argparse
from genson import SchemaBuilder
import os

parser = argparse.ArgumentParser(description='Attempt to detect schema by scanning all files \
        in the given folder')
parser.add_argument('--folder', required=True, type=str, help='the folder to scan')
#parser.add_argument('--max', default=100000, type=int, help='Max number of files to go through')
args = parser.parse_args()

builder = SchemaBuilder()

folder = args.folder
total_scanned = 0
json_errors = []

print(f"looping through {folder}")

def loop_dir(dirname: str):
    _files = []
    for subdir, dirs, files in os.walk(dirname):
        for d in dirs:
            _files.extend(loop_dir(d))
        for file in files:
            #print(f"Scanning: {subdir}/{file}")
            _files.append(f"{subdir}/{file}")
    return _files

file_list = []
file_list.extend(loop_dir(folder))

total_scanned = len(file_list)
print(f"Saw {total_scanned} number of files")

for f in file_list:
    with open(f, 'r') as file:
        try:
            json_obj = json.loads(file.read())
            builder.add_object(json_obj)
        except Exception as e:
            #print(f"bad: {e}")
            json_errors.append((f, f"{e}"))

total_json_errors = len(json_errors)
print(f"Total json errors: {total_json_errors}")
print(builder.to_json(indent=2))

with open("schema.json", "w") as f:
    f.write(builder.to_json(indent=2))

with open("json_errors.txt", "w") as f:
    output = "filename,error\n"
    for item in json_errors:
        #print(f" {item[0]} --> {item[1]} ")
        output += f"\"{item[0]}\",\"{item[1]}\"\n"
    f.write(output)
