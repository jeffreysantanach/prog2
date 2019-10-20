from flask import Flask
from flask import render_template, request

app = Flask("Hello World")

@app.route('/hello/',methods=['GET','POST'])
def hallo():
    if request.method == 'POST':
        number1 = request.form['number1']
        number2 = request.form['number2']
        number3 = request.form['number3']
        result = int(number1) +int(number2) +int(number3)
        return str(result)
    return render_template("calculator.html")
if __name__ == "__main__":
    app.run(debug=True, port=5000)
