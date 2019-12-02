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
def get_filepath(path,datatype):
    filepath= './data/' + datatype + "/"+ path
    return filepath

#route functions

@app.route('/',methods=['GET','POST'])
def index():
    files = data_helper.get_all_files(json_path)
    data = data_helper.load_json(auth_path + '/auth.json')
    client_id = data['client_id']
    client_secret = data['client_secret']
    if request.method == 'POST' :
        if request.form['submit'] == 'Submit':
          api_key = request.form['apikey']
          try: 
                selected_projects =  request.form.getlist('mycheckbox')
                salary = request.form['salary']
                memberfee = request.form['memberfee']
                path = report.report(selected_projects,int(salary),api_key,memberfee)
                redirect_path = 'projects/' + path
                return redirect(redirect_path)   
          except:
                return render_template("index.html",error= 'true')

        elif request.form['submit'] == 'Report':
            path = 'projects/' + request.form['file']
            return redirect(path)       
    return render_template("index.html",files= files,client_id=client_id, client_secret=client_secret)

@app.route('/projects/<path>')
def projects(path):
    if path is not None:
        data = data_helper.prepare_data("projects",path,"json")
        if data is None:
            return abort(404)
        return render_template("projects.html",projects=data,path=path)

@app.route('/persons/<path>')
def persons(path):
    if path is not None:
        data = data_helper.prepare_data("persons",path,"json")
        if data is None:
            return abort(404)
        return render_template("persons.html",persons=data, path=path)

@app.route('/tasks/<path>')
def tasks(path):
    if path is not None:
        data = data_helper.prepare_data("projects",path,"json")
        if data is None:
            return abort(404)
        return render_template("tasks.html",tasks=data, path=path) 
   

@app.route('/person/<path>/<id>')
def person(path,id):
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
    filepath=  get_filepath(path,"json")
    csv_filename = 'timereport_staysmart.csv'
    export.create_export(filepath,csv_filename)
    try:
        return send_from_directory(app.config["CLIENT_CSV"], filename=csv_filename, as_attachment=True)
    except FileNotFoundError:
       return abort(404)

@app.route('/returnpath',methods=['GET','POST'])
def auth():
    if request.method == 'GET':
        code = request.args.get('code')
        access_token = login(code)
        access_token = access_token['access_token']
        api_key= "Bearer " + access_token
        project_names= data_helper.get_list_of_projects(api_key)
        if project_names is None:
            return render_template("index.html",error= 'true')
        else:
            return render_template("index.html",projects= project_names, api_key=api_key)
        

def login(code):
    data = data_helper.load_json(json_path+"/auth.json")
    client_id = data['client_id']
    client_secret = data['client_secret']
    url= 'https://www.mindmeister.com/oauth2/token?grant_type=authorization_code&code='+code+'&client_id='+client_id+'&client_secret='+client_secret+'&redirect_uri=https://127.0.0.1:5000/returnpath&scopes=mindmeister'
    response = requests.post(url)
    response = response.json()
    return response

#errorhandler
@app.errorhandler(404)
def page_not_found(e):
    return redirect('https://127.0.0.1:5000/')  
if __name__ == "__main__":
    app.run(ssl_context='adhoc',debug=True, port=5000)
 