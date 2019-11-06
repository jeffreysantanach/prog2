from flask import Flask
from flask import render_template, request, redirect, url_for
from libs import report
import json
from libs import meistertask_requests as meistertask
from libs import data_helper 
app = Flask("staysmart_timereporter")
basepath = ".//data"
@app.route('/',methods=['GET','POST'])
def auth():
    project_names = []
    
    files = data_helper.get_all_files(basepath)
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
    return render_template("index.html",files= files)

@app.route('/projects/<path>')
def projects(path):
    if path is not None:
        filepath= 'data/' + path
        data = {}
        data = data_helper.load_json(filepath)
        data = data['projects']
        return render_template("projects.html",projects=data,path=path)

@app.route('/persons/<path>')
def persons(path):
    if path is not None:
        filepath= 'data/' + path
        data = {}
        data = data_helper.load_json(filepath)
        data = data['persons']
        return render_template("persons.html",persons=data, path=path)

@app.route('/tasks/<path>')
def tasks(path):
    if path is not None:
        filepath= 'data/' + path
        data = {}
        data = data_helper.load_json(filepath)
        data = data['projects']
        return render_template("tasks.html",tasks=data, path=path)
        #return data
       
    return redirect(url_for('main.py'))
if __name__ == "__main__":
    app.run(debug=True, port=5000)
