
"""
Summary:
Libary of functions to create an the report. 

"""
from . import meistertask_requests as meistertask
from datetime import datetime
from datetime import timedelta
from . import data_helper
import json

def calctime(starttime,endtime):
    """
    Summary: 
    Calculates the difference between start time and end time in seconds.
    
    Args:
        starttime (datetime): start time in the format %Y-%m-%dT%H:%M:%S.%fZ
        endtime (datetime): end time in the format %Y-%m-%dT%H:%M:%S.%fZ
    Returns:
        integer: time difference in seconds
    """
    time = 0.0
    time = endtime - starttime
    time = time.seconds
    return time

def export_report_json(data):
    """
    Summary: 
    Exports the report into a JSON file.
    
    Args:
        data (dictionary): the report data
    Returns:
        string: name of JSON file
    """
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    path = 'report' + dt_string + '.json'
    path_json = 'data/json/' +path
    data_helper.save_json(path_json,data)
    return path

def append_members_json(members,key,firstname,lastname,hours,hsalary,report,memberfee):
    """
    Summary: 
    Appends an new member to the project with the hours he/she spended in at this project. 
    It also adds the hours to the summary of each person in the report.
    
    Args:
        members (dictionary): dict of the members in the project
        key (integer): identifier (key) of the person
        firstname (string): firstname of the person
        lastname (string): lastname of the person
        hours (floating): hours of the person he or she has worked on the project
        hsalary (floating): salary per hour
        report (dictionary): the report 
        memberfee (floating): memberfee of the association
    """
    # Adds an new member to the project overview.
    members[key] = []
    members[key].append({
       'firstname' : firstname,
       'lastname' : lastname,
       'hours' : round(hours,2),
       'salary' : round(hours*hsalary,2)
        }   )
    
    # Adds or update the person in the summary of the report. 

    salary = round(hours*hsalary,2) - float(memberfee) # The salary is calculated as shown here: (Hours * Hourly salary) - Memberfee 
    if key in report['persons']: 
        # If person already has an entry, it must be updated. This mainly affects the hours and the salary
        hours = hours + float(report['persons'][key]['hours'])
        salary = round(hours*hsalary,2) - float(memberfee)
        report['persons'][key]['hours'] = round(hours,2)
        if salary > 0:
            report['persons'][key]['salary'] = str(salary) + ' CHF'
        else:
            report['persons'][key]['salary'] = '0 CHF'
    else: 
        if salary < 0:
            report['persons'][key] = {
                    "firstname": firstname,
                    "lastname" : lastname,
                    "hours": round(hours,2),
                    "salary" : str(0) + ' CHF'
                } 
        else:
            report['persons'][key] = {
                "firstname": firstname,
                "lastname" : lastname,
                "hours": round(hours,2),
                "salary" : str(round(salary,2)) + ' CHF'
            }
   

def append_project_json(projects,name,members,tasks,projecttime,hsalary):
    """
    Summary: 
    Appends a new project to the report. 
    
    Args:
        projects (dictonary): including all project data
        name(string): name of the project
        members (dictionary): dict of the members in the project
        projecttime (floating): hours which has been spended at the project
        hsalary (floating): salary per hour
    """
    projects[name] = []
    projects[name].append({
                    'members': members,
                    'tasks' : tasks,
                    'time' : round(projecttime,2),
                    'costs' : round(projecttime *hsalary,2) 
                    }   )
    

def append_task_json(tasks,key,name,time,hsalary):
    """
    Summary: 
    Appends a new task to the report. 
    
    Args:
        tasks (dictonary): including all tasks data
        key (integer): idenifier of the task
        name(string): name of the task
        time (dictionary): hours which has been spended at this task
        hsalary (floating): salary per hour
    """
    tasks[key] =[]
    tasks[key].append({
            'name' : name,
            'time' : round(time,2),
            'costs' : round(time*hsalary,2)
        })
    
    
def sec_to_hours(seconds):
    """
    Summary: 
    Converts seconds into hours
    
    Args:
        seconds (floating): seconds
    Returns: 
        floating : hours which has been calculated
    """
    hours = seconds/3600
    hours = round(hours,2)
    return hours

def add_time_to_worktime(starttime,endtime,worktime):
    """
    Summary: 
    Add a timespan to the worktime
    
    Args:
        starttime (datetime): start time in the format %Y-%m-%dT%H:%M:%S.%fZ
        endtime (datetime): end time in the format %Y-%m-%dT%H:%M:%S.%fZ

    Returns:
        floating: working after adding an new timespan
    """
    result= float(calctime(starttime,endtime))
    result = sec_to_hours(result)
    worktime = worktime + result
    return worktime

def report(selected_projects,hsalary,apikey,memberfee):
    """
    Summary: 
    Get information from Meistertask API and creates an report from the selected projects
    
    Args:
        selected_projects (list): project ids of projects which should be 
        hsalary (floating): salary per hour
        apikey (string): 
        memberfee (floating): 
    Returns:
        floating: working after adding an new timespan
    """
    report = {}
    projects = {}
    report['persons'] = {}
    report['memberfee'] = memberfee
    
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
                    worktime = add_time_to_worktime(datetime.strptime(time['started_at'],'%Y-%m-%dT%H:%M:%S.%fZ'),datetime.strptime(time['finished_at'],'%Y-%m-%dT%H:%M:%S.%fZ'),worktime)  
            append_members_json(members,person['id'],person['firstname'],person['lastname'],worktime,hsalary,report,memberfee)
            
        for task in project_tasks:
            worktime = 0.0
            worktime= sec_to_hours(task['tracked_time'])
            projecttime = projecttime + worktime
            append_task_json(tasks,task['id'],task['name'],worktime,hsalary)
        append_project_json(projects,name,members,tasks,projecttime,hsalary)
    report['projects'] = projects
    path = export_report_json(report)
    return path
 