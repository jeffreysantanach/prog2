from flask import Flask
from flask import render_template

app = Flask("Hello World")

@app.route('/')
def hallo(name="Jeffrey"):
    return "hello " + name + " !"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
