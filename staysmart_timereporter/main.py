from flask import Flask
from flask import render_template, request, redirect, url_for
from libs import report
import json
from libs import meistertask_requests as meistertask
from libs import data_helper 
app = Flask("staysmart_timereporter")

@app.route('/',methods=['GET','POST'])
def auth():
    project_names = []
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
                path = report.report(selected_projects,int(salary),api_key)
                redirect_path = 'projects/' + path
                return redirect(redirect_path)
            except:
                return render_template("index.html",error= 'true')
    return render_template("index.html")

@app.route('/projects/<path>')
def projects(path):
    if path is not None:
        path= 'data/' + path
        data = {}
        data = data_helper.load_json(path)
        data = data['projects']
        return render_template("projects.html",projects=data)
    return data
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
