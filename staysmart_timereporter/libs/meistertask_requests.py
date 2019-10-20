import requests 
from libs import auth_meistertask as authentication
def get_tasks(projectid):
    url = 'http://www.meistertask.com/api/projects/' + projectid +'/tasks'
    response = requests.get( url,
               headers={'Authorization': authentication.key},
    )
    response = response.json()
    return response 

def get_projects(projectid):
    url = 'http://www.meistertask.com/api/projects/' + projectid
    response = requests.get( url,
               headers={'Authorization': authentication.key},
    )
    response = response.json()
    return response 

def get_workintervals_project(projectid):
    url = 'http://www.meistertask.com/api/projects/'+ projectid +'/work_intervals?'
    response = requests.get( url,
               headers={'Authorization': authentication.key},
    )
    response = response.json()
    return response
def get_persons_project(projectid):
    url = 'http://www.meistertask.com/api/projects/'+ projectid +'/members?include_persons=true'
    response = requests.get( url,
               headers={'Authorization': authentication.key},
    )
    response = response.json()
    return response
def get_all_project():
    url = 'http://www.meistertask.com/api/projects/'
    response = requests.get( url,
               headers={'Authorization': authentication.key},
    )
    response = response.json()

    return response
