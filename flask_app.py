from flask import Flask, render_template, make_response, request
from linearSystem import LinearSystem
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
    print(variables)
    variableList = variables.split("-")
    constantsList = constants.split(",")
    for i in range(len(variableList)):
        variableList[i] = variableList[i].split(",")
        for j in range(len(variableList[i])):
            variableList[i][j] = float(variableList[i][j])
        constantsList[i] = float(constantsList[i])
    l = LinearSystem(variableList,constantsList)
    return list(l.solve_linear_system())
if __name__ == '__main__':
    app.run(debug=True)
