import requests 

def get_tasks(projectid,api_key):
    url = 'http://www.meistertask.com/api/projects/' + projectid +'/tasks'
    response = requests.get( url,
               headers={'Authorization': api_key},
    )
    response = response.json()
    return response 

def get_projects(projectid,api_key):
    url = 'http://www.meistertask.com/api/projects/' + projectid
    response = requests.get( url,
               headers={'Authorization': api_key},
    )
    response = response.json()
    return response 

def get_workintervals_project(projectid,api_key):
    url = 'http://www.meistertask.com/api/projects/'+ projectid +'/work_intervals?'
    response = requests.get( url,
               headers={'Authorization': api_key},
    )
    response = response.json()
    return response
def get_persons_project(projectid,api_key):
    url = 'http://www.meistertask.com/api/projects/'+ projectid +'/members?include_persons=true'
    response = requests.get( url,
               headers={'Authorization': api_key},
    )
    response = response.json()
    return response
def get_all_project(api_key):
    url = 'http://www.meistertask.com/api/projects/'
    response = requests.get( url,
               headers={'Authorization': api_key},
    )
    response = response.json()

    return response
