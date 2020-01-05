"""
Summary:  libary of functions with API Requests
"""
import requests 

def get_tasks(projectid,api_key):
    """
    Summary: 
    Gets all tasks of a specific project in Meistertask
    
    Args:
        projectid (integer): ID of the project
        api_key (string): API key of the user for accessing the data in meistertask
    Returns:
        dictionary: tasks in the projects
    """
    url = 'http://www.meistertask.com/api/projects/' + projectid +'/tasks'
    response = requests.get( url,
               headers={'Authorization': api_key},
    )
    response = response.json()
    return response 

def get_projects(projectid,api_key):
    """
    Summary: 
    Gets informations of a specific project in Meistertask. 
    
    Args:
        projectid (integer): ID of the project
        api_key (string): API key of the user for accessing the data in meistertask
    Returns:
        dictionary: properties of the project
    """
    url = 'http://www.meistertask.com/api/projects/' + projectid
    response = requests.get( url,
               headers={'Authorization': api_key},
    )
    response = response.json()
    return response 

def get_workintervals_project(projectid,api_key):
    """
    Summary: 
    Gets all work intervalls of a specific project in Meistertask. 
    
    Args:
        projectid (integer): ID of the project
        api_key (string): API key of the user for accessing the data in meistertask
    Returns:
        dictionary: work intervalls of the project
    """
    url = 'http://www.meistertask.com/api/projects/'+ projectid +'/work_intervals?finished=true'
    response = requests.get( url,
               headers={'Authorization': api_key},
    )
    response = response.json()
    return response
def get_persons_project(projectid,api_key):
    """
    Summary: 
    Gets all members of a specific project in Meistertask. 
    
    Args:
        projectid (integer): ID of the project
        api_key (string): API key of the user for accessing the data in meistertask
    Returns:
        dictionary: member of the project
    """
    url = 'http://www.meistertask.com/api/projects/'+ projectid +'/members?include_persons=true'
    response = requests.get( url,
               headers={'Authorization': api_key},
    )
    response = response.json()
    return response
def get_all_project(api_key):
    """
    Summary: 
    Gets all projects the user is a member of.
    
    Args:
        api_key (string): API key of the user for accessing the data in meistertask
    Returns:
        dictionary: properties of the projects
    """
    url = 'http://www.meistertask.com/api/projects/'
    response = requests.get( url,
               headers={'Authorization': api_key},
    )
    response = response.json()

    return response
