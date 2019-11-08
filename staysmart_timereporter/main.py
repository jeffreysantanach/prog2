from flask import Flask
from flask import render_template, request, redirect, url_for,send_file
from libs import report

import os
import json
from libs import meistertask_requests as meistertask
from libs import data_helper 
from libs import export
from flask import send_file, send_from_directory, abort

app = Flask("staysmart_timereporter")
csv_path ="data/csv"
app.config["CLIENT_CSV"] = csv_path

json_path = "./data/json"
def get_filepath(path,datatype):
    filepath= './data/' + datatype + "/"+ path
    return filepath

@app.route('/',methods=['GET','POST'])
def auth():
    project_names = []
    
    files = data_helper.get_all_files(json_path)
    if request.method == 'POST' :
        if request.form['submit'] == 'Search':
            api_key = request.form['apikey']
            try:
                response = meistertask.get_all_project(api_key)
                for project in response:
                    project_names.append({
                    "name": project['name'],
                    "id": project['id']
                        })
                return render_template("index.html",projects= project_names, api_key=api_key)
                
            except:
                return render_template("index.html",error= 'true')
        elif request.form['submit'] == 'Submit':
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
            
    return render_template("index.html",files= files)

@app.route('/projects/<path>')
def projects(path):
    if path is not None:
        filepath=  get_filepath(path,"json")
        data = {}
        data = data_helper.load_json(filepath)
        data = data['projects']
        return render_template("projects.html",projects=data,path=path)

@app.route('/persons/<path>')
def persons(path):
    if path is not None:
        filepath=  get_filepath(path,"json")
        data = {}
        data = data_helper.load_json(filepath)
        data = data['persons']
        return render_template("persons.html",persons=data, path=path)

@app.route('/tasks/<path>')
def tasks(path):
    if path is not None:
        filepath=  get_filepath(path,"json")
        data = {}
        data = data_helper.load_json(filepath)
        data = data['projects']
        return render_template("tasks.html",tasks=data, path=path)
        #return data
       
    return redirect(url_for('main.py'))

@app.route('/person/<path>/<id>')
def person(path,id):
    if path is not None:
        filepath=  get_filepath(path,"json")
        data = {}
        data = data_helper.load_json(filepath)
        memberfee = data['memberfee']
        person = data['persons'][id]
        data = data['projects']
        return render_template("person.html",projects=data, path=path, id= id, person= person,memberfee=memberfee)
        #return data
       
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



@app.errorhandler(404)
def page_not_found(e):
    return redirect('http://127.0.0.1:5000/')  
if __name__ == "__main__":
    app.run(debug=True, port=5000)
