from . import data_helper
def prepare_export(persons,projects,memberfee):
    export={}
    header= ["firstname","lastname","hours","salary","memberfee"]
    for key,value in persons.items():
         person_id = key
         person = {}
         for key,value in value.items():
             person[key]= value
         person['memberfee'] = memberfee
         for projectname,properties in projects.items():
            for project in properties:
                for id,values in project['members'].items():
                    if id == person_id:
                        for member in values:                            
                            person[projectname] = member['hours']
                    else:
                        person[projectname] =12
         export[person_id] = person
    for projectname,properites in projects.items():
        header.append(projectname)
    return export,header

def create_export(path,name_csv):
    data = data_helper.load_json(path)
    memberfee = data['memberfee']
    export_list = prepare_export(data['persons'],data['projects'],memberfee)
    export = export_list[0]
    headers = export_list[1]
    data_helper.save_csv(headers,export,name_csv)