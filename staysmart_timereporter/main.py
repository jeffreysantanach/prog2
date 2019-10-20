from flask import Flask
from flask import render_template, request

import json
from libs import meistertask_requests as meistertask

app = Flask("staysmart_timereporter")

@app.route('/',methods=['GET','POST'])
def auth():
    project_names = []
    if request.method == 'POST' and project_names == []:
        response = meistertask.get_all_project()
        for project in response:
            project_names.append({
             "name": project['name'],
             "id": project['id']
                })
        
        with open('data/projects.json','w') as outfile:
            json.dump(project_names,outfile)
        return render_template("index.html",projects= project_names)
    
    return render_template("index.html")

    

if __name__ == "__main__":
    app.run(debug=True, port=5000)
