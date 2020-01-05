""" 
Summary: 
    Main python file to run the webapp. It routes the webrequest to the correct functions. 
Args:
    app: defines the name of the web app
    csv_path: path of the CSV-Files
    app.config["CLIENT_CSV"]: Config for downloading files
    json_path: path of the JSON files
    auth_path: path of the authorization file for the api access to meistertask.
"""
# import modules
import os
import json
import requests
from flask import Flask
from flask import render_template, request, redirect, url_for,send_file
from flask import send_file, send_from_directory, abort

from libs import meistertask_requests as meistertask
from libs import data_helper 
from libs import export
from libs import report
 
#global varibales
app = Flask("staysmart_timereporter")
csv_path ="data/csv"
app.config["CLIENT_CSV"] = csv_path
json_path = "./data/json"
auth_path = "./data/auth"

#functions

def get_access_token(code):
    """
    Summary: 
    Gets the Access Token from MeisterTask
    
    Args:
        code (String): the authorization code received from the Meistertask authorization server
    Returns:
        string: the access token of respective user
    """
    data = data_helper.load_json(auth_path+"/auth.json")
    client_id = data['client_id']
    client_secret = data['client_secret']
    url= 'https://www.mindmeister.com/oauth2/token?grant_type=authorization_code&code='+code+'&client_id='+client_id+'&client_secret='+client_secret+'&redirect_uri=https://127.0.0.1:5000/returnpath&scopes=mindmeister'
    response = requests.post(url)
    response = response.json()
    access_token = response['access_token']
    return access_token

#route functions

@app.route('/',methods=['GET','POST'])
def index():
    """
    Summary: 
    Start page of the tool. 
    When https://127.0.0.1:5000 is called for the first time, index.html is called. 
    If the button "View projects" is pressed, an already existing report is opened.
    If the button "Evaluate projects" is pressed, the projects are analysed.
   
        
    Returns:
        Renders templates or call functions with the path.
    """
    files = data_helper.get_all_files(json_path)
    data = data_helper.load_json(auth_path + '/auth.json')
    client_id = data['client_id']
    client_secret = data['client_secret']
    if request.method == 'POST' :
        if request.form['submit'] == 'Submit':
            api_key = request.form['apikey']
            try:
                selected_projects =  request.form.getlist('mycheckbox')
                hsalary = request.form['salary']
                memberfee = request.form['memberfee']
                path = report.report(selected_projects,float(hsalary),api_key,float(memberfee))
                redirect_path = 'projects/' + path
                # Forwarding to the report just created
                return redirect(redirect_path)  
            # forwarding to the error page
            except:
                return render_template("index.html",error= 'true')

        elif request.form['submit'] == 'Report':
            path = 'projects/' + request.form['file']
            # Forwarding to the selected report 
            return redirect(path)
    # shows startpage       
    return render_template("index.html",files= files,client_id=client_id, client_secret=client_secret)

@app.route('/projects/<path>')
def projects(path):
    """
    Summary: 
    Shows the report for all projects
    
    Args:
        path (string): name of the json file
        
    Returns:
        report of projects
    """
    if path is not None:
        data = data_helper.prepare_data("projects",path,"json")
        if data is None:
            return abort(404)
        return render_template("projects.html",projects=data,path=path)

@app.route('/persons/<path>')
def persons(path):
    """
    Summary: 
    Shows the report for all persons
    
    Args:
        path (string): name of the json file
        
    Returns:
        report of persons
    """
    if path is not None:
        data = data_helper.prepare_data("persons",path,"json")
        if data is None:
            return abort(404)
        return render_template("persons.html",persons=data, path=path)

@app.route('/tasks/<path>')
def tasks(path):
    """
    Summary: 
    Shows the report for all tasks
    
    Args:
        path (string): name of the json file
        
    Returns:
        report of tasks
    """
    if path is not None:
        data = data_helper.prepare_data("projects",path,"json")
        if data is None:
            return abort(404)
        return render_template("tasks.html",tasks=data, path=path) 
   

@app.route('/person/<path>/<id>')
def person(path,id):
    """
    Summary: 
    Shows the time report for the individual person
    
    Args:
        path (string): name of the json file
        id (integer): Meistertask ID of person 
        
    Returns:
       time report of the individual person
    """
    if path is not None:
        memberfee = data_helper.prepare_data("memberfee",path,"json")
        data = data_helper.prepare_data("projects",path,"json")
        person = data_helper.prepare_data("persons",path,"json")
        try: 
            person = person[id]
            return render_template("person.html",projects=data, path=path, id= id, person= person,memberfee=memberfee)
        except:
            return abort(404)
    return redirect(url_for('main.py'))

@app.route("/download/<path>")
def csv_export(path):
    """
    Summary: 
    Creates a CSV file and makes it available for download
    
    Args:
        path (string): name of the json file
        id (integer): Meistertask ID of person 
        
    Returns:
       CSV file to download
    """
    filepath=  data_helper.get_filepath(path,"json")
    csv_filename = path[:-5] + ".csv"
    export.create_export(filepath,csv_filename)
    try:
        return send_from_directory(app.config["CLIENT_CSV"], filename=csv_filename, as_attachment=True)
    except FileNotFoundError:
       return abort(404)

@app.route('/returnpath',methods=['GET','POST'])
def auth():
    """
    Summary: 
    Returns path of OAuth2 authorization, get the secret code of the meistertask server 
    and get out the access_token of the user
        
    Returns:
       Form for selection of the projects, which should be analysed
    """
    if request.method == 'GET':
        code = request.args.get('code')
        access_token = get_access_token(code)
        
        api_key= "Bearer " + access_token
        project_names= data_helper.get_list_of_projects(api_key)
        if project_names is None:
            return render_template("index.html",error= 'true')
        else:
            return render_template("index.html",projects= project_names, api_key=api_key)
        

#errorhandler
@app.errorhandler(404)
def page_not_found(e):
    """
    Summary: 
    error handler for error 404. It brings the user back to the startpage
    
    Args:
        e (string): id of error
    
    Returns:
       Startpage
    """
    return redirect('https://127.0.0.1:5000/')  
if __name__ == "__main__":
    app.run(ssl_context='adhoc',debug=True, port=5000)
 