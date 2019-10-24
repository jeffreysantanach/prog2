import json
import data_helper
import meistertask_requests
def get_all_persons(data):
    persons = set()
    for project in data:
        for projectdata in data[project]:
            for member in projectdata['members']:
                persons.add(member)
    return persons

def sum_per_person(data,persons):
    for person in persons:
         for project in data:
            for projectdata in data[project]:
                for member in projectdata['members']:
                
with open("test.json", "r") as open_file:
            data = json.load(open_file)
persons = get_all_persons(data)
