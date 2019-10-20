from flask import Flask

app = Flask("Hello World")


@app.route('/hello')
def hello_world():
    return '<h1> Hello, World!</h1>'


if __name__ == "__main__":
    app.run(debug=True, port=5000)
