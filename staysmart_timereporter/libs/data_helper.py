import json
import os 

def load_json(json_path):
    data = {}
    try:
        with open(json_path, "r") as open_file:
            data = json.load(open_file)
    except:
        print("Error with file at", json_path, "!")
    finally:
        return data

def save_json(json_path, data):
    with open(json_path, "w", encoding="utf-8") as open_file:
        json.dump(data, open_file, indent=4)
def get_all_files(basepath):
    files = []
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            files.append(entry)
    return files