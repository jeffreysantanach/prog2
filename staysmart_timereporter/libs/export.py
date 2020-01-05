"""
Summary:
Libary of functions to create an CSV export of the report. 

"""

from . import data_helper
def prepare_export(persons,projects,memberfee):
    """
    Summary:
    Goes through all projects and get the hours made in the project, if available,
    and add it to the dictionary. This is repeated for each person.
    Args:
        persons (dict): persons of the report
        projects (dict): projects of the report
        memberfee (int): memberfee of the association 
    Return:
        0   list: header information for CSV
        1   dict: content of the csv-file
    """
    export={}
    header= ["firstname","lastname","hours","salary","memberfee"]
    for key,value in persons.items():
         person_id = key
         person = {}
         for key,value in value.items():
             person[key]= value
         person['memberfee'] = memberfee   
         for projectname,properties in projects.items():
            person[projectname] = 0 
            for project in properties:
                for id,values in project['members'].items():
                    if id == person_id:                         
                        person[projectname]= values[0]['hours']
         export[person_id] = person
         
    for projectname,properites in projects.items():
        header.append(projectname)
    return export,header

def create_export(path,name_csv):
    """
    Summary:
    Creates the CSV file out of the report
    Args:
        path (string): file path of the JSON-File
        name_csv (string): name of the CSV which has to be created
       

    """
    data = data_helper.load_json(path)
    memberfee = data['memberfee']
    export_list = prepare_export(data['persons'],data['projects'],memberfee)
    export = export_list[0]
    headers = export_list[1]
    data_helper.save_csv(headers,export,name_csv)