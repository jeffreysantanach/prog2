from . import meistertask_requests as meistertask
from datetime import datetime
from datetime import timedelta
from . import data_helper
import json

def calctime(starttime,endtime):
    time = 0.0
    time = endtime - starttime
    time = time.seconds
    return time

def export_report_json(data):
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    path = 'report' + dt_string + '.json'
    path_json = 'data/' +path
    data_helper.save_json(path_json,data)
    return path

def append_members_json(members,key,firstname,lastname,hours,salary):
    members[key] = []
    members[key].append({
       'firstname' : firstname,
       'lastname' : lastname,
       'hours' : round(hours,2),
       'salary' : round(hours*salary,2)
        }   )
    return members

def append_project_json(projects,name,members,tasks,projecttime,salary):
    projects[name] = []
    projects[name].append({
                    'members': members,
                    'tasks' : tasks,
                    'time' : projecttime,
                    'costs' : round(projecttime *salary,2)
                    }   )
    return projects

def append_task_json(tasks,key,name,time):
    tasks[key] =[]
    tasks[key].append({
            'name' : name,
            'time' : time
        })
    return tasks

def sec_to_hours(seconds):
    hours = seconds/3600
    hours = round(hours,2)
    return hours

def get_report_data(selected_projects,apikey):
    return

def report(selected_projects,salary,apikey):
    projects = {}
    
    for selected_project in selected_projects:
        name = meistertask.get_projects(selected_project,apikey)
        name = name['name']
        projecttime = 0.0
        times = meistertask.get_workintervals_project(selected_project,apikey)
        persons = meistertask.get_persons_project(selected_project,apikey)
        project_tasks = meistertask.get_tasks(selected_project,apikey)
        persons = persons['persons'] 
        members = {}
        tasks={}
        for person in persons:
            worktime = 0.0
            for time in times:
                if time['person_id'] == person['id']:
                    result= float(calctime(datetime.strptime(time['started_at'],'%Y-%m-%dT%H:%M:%S.%fZ'),datetime.strptime(time['finished_at'],'%Y-%m-%dT%H:%M:%S.%fZ')))
                    result = sec_to_hours(result)
                    worktime = worktime + result  
            members = append_members_json(members,person['id'],person['firstname'],person['lastname'],worktime,salary)
        for task in project_tasks:
            worktime = 0.0
            worktime= sec_to_hours(task['tracked_time'])
            projecttime = projecttime + worktime
            tasks = append_task_json(tasks,task['id'],task['name'],worktime)
        projects = append_project_json(projects,name,members,tasks,projecttime,salary)
     
        
  
    path = export_report_json(projects)
    return path