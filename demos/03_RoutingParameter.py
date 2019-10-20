from flask import Flask
from flask import render_template

app = Flask("Hello World")
@app.route('/hello')
@app.route('/hello/<name>')
def begruessung(name=False):
    if name:
        return "Hallo " + name + " !"
    else:
        return "Not Hallo World again..."
if __name__ == "__main__":
    app.run(debug=True, port=5000)
