import json
import os 
from . import meistertask_requests as meistertask
import csv


def save_csv(headers,export,filename):
    path = 'data/csv/'+ filename
    with open(path, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for key,values in export.items():
            writer.writerow(values)

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

def get_list_of_projects(api_key):
        project_names = []
        try:
            response = meistertask.get_all_project(api_key)
            for project in response:
                project_names.append({
                "name": project['name'],
                "id": project['id']
                    })
            return project_names 
        except:
            return
def prepare_data(key,path,datatype):
    try:
        filepath = get_filepath(path,datatype)
        data = {}
        data = load_json(filepath)
        data = data[key]
        return data
    except:
        return 

def get_filepath(path,datatype):
    filepath= './data/' + datatype + "/"+ path
    return filepath