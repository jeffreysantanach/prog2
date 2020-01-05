"""
Summary:
Libary of functions to edit, read and save data in files. 

"""

import json
import os 
from . import meistertask_requests as meistertask
import csv

def save_csv(headers,export,filename):
    """
    Summary: 
    Creates a CSV file in the CSV folder
    
    Args:
        headers (dict): header of csv-file
        export (dict): content of csv-file (without header)
        filename (string): the name of the csv-file
        
    """
    path = 'data/csv/'+ filename
    with open(path, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for key,values in export.items():
            writer.writerow(values)

def load_json(json_path):
    """
    Summary: 
    Fetches the contents of a JSON file.
    
    Args:
        json_path (string): path of the JSON file
        
    Returns:
        dict : Content of JSON file
    """
    data = {}
    try:
        with open(json_path, "r") as open_file:
            data = json.load(open_file)
    except:
        print("Error with file at", json_path, "!")
    finally:
        return data

def save_json(json_path, data):
    """
    Summary: 
    Creates a JSON file in the JSON folder
    
    Args:
        json_path (dictionary): path and filename of the JSON file. 
        data (dict): content of json-file 
   
        
    """
    with open(json_path, "w", encoding="utf-8") as open_file:
        json.dump(data, open_file, indent=4)


def get_all_files(basepath):
    """
    Summary: 
    Creates a list of the files in the specific folder
    
    Args:
        basepath (dictionary): Path of the folder where the files should be searched
    Returns:
        list : list of files in specific folder
        
    """
    files = []
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            files.append(entry)
    return files

def get_list_of_projects(api_key):
    """
    Summary: 
    Creates a list of the projects in meistertask, in which the user is a member of.
    
    Args:
        api_key (string): API key of the user for accessing the data in meistertask.
    Returns:
        list : List of projects the user is a member of
        
    """
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
    """
    Summary: 
    Gets data from JSON file and returns the values specified in the key.
    
    Args:
        key (string): name of the key from which the data should be taken.
        path (string): name of the file
        datatype (string): Datatype of the file
    Returns:
        string: full path of the file
    """
    try:
        filepath = get_filepath(path,datatype)
        data = {}
        data = load_json(filepath)
        data = data[key]
        return data
    except:
        return 

def get_filepath(path,datatype):
    """
    Summary: 
    Creates the file path, based on the file type
    
    Args:
        path (string): name of the file
        datatype (string): Datatype of the file
    Returns:
        string: full path of the file
    """
    filepath= './data/' + datatype + "/"+ path
    return filepath