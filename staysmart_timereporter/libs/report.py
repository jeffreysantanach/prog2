
import meistertask_requests as meistertask
from datetime import datetime
from datetime import timedelta
import json

def calctime(starttime,endtime):
    time = 0.0
    time = endtime - starttime
    time = time.seconds
    return time
def sec_to_hours(seconds):
    hours = seconds/3600
    hours = round(hours,2)
    return hours
def report(selected_projects,apikey):
    projects = {}
    #projects['projects'].append({'PR&Marketing2019'}) 
    for selected_project in selected_projects:
        name = meistertask.get_projects(selected_project,apikey)
        name = name['name']
        projecttime = 0.0
        times = meistertask.get_workintervals_project(selected_project,apikey)
        persons = meistertask.get_persons_project(selected_project,apikey)
        project_tasks = meistertask.get_tasks(selected_project,apikey)
        persons = persons['persons']
        projects[name] = []
        members = {}
        tasks={}
        for person in persons:
            worktime = 0.0
            for time in times:
                if time['person_id'] == person['id']:
                    result= float(calctime(datetime.strptime(time['started_at'],'%Y-%m-%dT%H:%M:%S.%fZ'),datetime.strptime(time['finished_at'],'%Y-%m-%dT%H:%M:%S.%fZ')))
                    result = sec_to_hours(result)
                    worktime = worktime + result     
            key = person['id']  
            members[key] = []
            members[key].append({
                'firstname' : person['firstname'],
                'lastname' : person['lastname'],
                'hours' : worktime,
                'salary' : worktime *25
                    
                }) 
        for task in project_tasks:
            worktime = 0.0
            
            worktime= sec_to_hours(task['tracked_time'])
            projecttime = projecttime + worktime
            key= task['id']
            tasks[key] =[]
            tasks[key].append({
                'name' : task['name'],
                'time' : worktime
            })

        projects[name].append({
                    'members': members,
                    'tasks' : tasks,
                    'time' : projecttime
                    }   )
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    path = 'data/report' + dt_string + '.json'
    with open(path,'w') as outfile:
        json.dump(projects,outfile)
    return path