
from flask import Flask, render_template, make_response, request

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/solve')
def solve():
    return render_template('solve.html')
@app.route('/docs')
def docs():
    return render_template('docs.html')
@app.route('/linear',methods = ['POST','GET'])
def linear():
    resp = make_response(render_template('linear.html'))
    resp.set_cookie('variables', 'test')
    resp.set_cookie('constants', 'test2')
    return resp
@app.route('/linearSolve',methods = ['POST', 'GET'])
def linearSolve():
    variables = request.cookies.get('variables')
    constants = request.cookies.get('constants')
    variableList = variables.split(".")
    for i in range(len(variableList)):
        variableList[i] = variableList[i].split(",")
    return "These are the variables: " + variables + ". And these are the constants: " + constants
if __name__ == '__main__':
    app.run(debug=True)
