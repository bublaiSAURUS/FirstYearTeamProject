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
    resp = make_response(render_template('ResultsPage.html'))
    variables = request.cookies.get('variables').replace(",","@")
    constants = request.cookies.get('constants').replace(",","@")
    variableList = variables.split("&")
    constantsList = constants.split("@")
    for i in range(len(variableList)):
        variableList[i] = variableList[i].split("@")
        for j in range(len(variableList[i])):
            variableList[i][j] = float(variableList[i][j])
        constantsList[i] = float(constantsList[i])
    l = LinearSystem(variableList,constantsList)
    resp.set_cookie('variables', variables)
    resp.set_cookie('constants', constants)
    solutions = ','.join(str(x) for x in list(l.solve_linear_system()))
    resp.set_cookie('solution',solutions.replace(",","@"))
    return resp
@app.route('/nonLinear',methods = ['POST','GET'])
def nonLinear():
    resp = make_response(render_template('nonLinear.html'))
    resp.set_cookie('variables', 'test')
    resp.set_cookie('constants', 'test2')
    return resp
@app.route('/nonLinearSolve',methods = ['POST', 'GET'])
def nonLinearSolve():
    variables = request.cookies.get('variables')
    constants = request.cookies.get('constants')
    print(variables)
    variableList = variables.split("&")
    constantsList = constants.split(",")
    for i in range(len(variableList)):
        variableList[i] = variableList[i].split(",")
        for j in range(len(variableList[i])):
            variableList[i][j] = float(variableList[i][j])
        constantsList[i] = float(constantsList[i])
    return variableList
@app.route('/ODE',methods = ['POST','GET'])
def ODE():
    resp = make_response(render_template('ODE.html'))
    resp.set_cookie('variables', 'test')
    resp.set_cookie('constants', 'test2')
    return resp
@app.route('/ODESolve',methods = ['POST', 'GET'])
def ODESolve():
    coefficients = request.cookies.get('coefficients')
    initialConditions = request.cookies.get('initialConditions')
    initialConditionsList = initialConditions.split('&')
    initialConditionsDict = {}
    for initialCondition in initialConditionsList:
        values = initialCondition.split(",")
        for i in range(len(values)):
            values[i] = float(values[i])
        initialConditionsDict[values[0]] = values[1:]
    coefficientsList = coefficients.split(",")
    for i in range(len(coefficientsList)):
        coefficientsList[i] = float(coefficientsList[i])
    return initialConditionsDict
if __name__ == '__main__':
    app.run(debug=True)
