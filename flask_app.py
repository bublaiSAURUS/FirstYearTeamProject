from flask import Flask, render_template, make_response, request
from linearSystem import LinearSystem
import sympy as sp
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
    variableList = variables.split("&")
    constantsList = constants.split(",")
    for i in range(len(variableList)):
        variableList[i] = variableList[i].split(",")
        for j in range(len(variableList[i])):
            variableList[i][j] = float(variableList[i][j])
        constantsList[i] = float(constantsList[i])
    l = LinearSystem(variableList,constantsList)
    return list(l.solve_linear_system())
@app.route('/nonLinear',methods = ['POST','GET'])
def nonLinear():
    resp = make_response(render_template('nonLinear.html'))
    resp.set_cookie('variables', 'test')
    resp.set_cookie('constants', 'test2')
    return resp
@app.route('/nonLinearSolve',methods = ['POST', 'GET'])
def nonLinearSolve():
    resp = make_response(render_template('nonLinearSolve.html'))
    variables = request.cookies.get('variables')
    constants = request.cookies.get('constants')
    variableList = variables.split("&")
    constantsList = constants.split(",")
    for i in range(len(variableList)):
        variableList[i] = variableList[i].split(",")
        for j in range(len(variableList[i])):
            variableList[i][j] = float(variableList[i][j])
        constantsList[i] = float(constantsList[i])
    x,y,z = sp.symbols("x,y,z")
    functionList = []
    if len(variableList) == 3:
        for i in range(len(variableList)):
            functionList.append(sp.Eq(variableList[i][0]*x**2+variableList[i][1]*y**2+variableList[i][2]*z**2+variableList[i][3]*x+variableList[i][4]*y+variableList[i][5]*z,constantsList[i]))
        solution = sp.solve(functionList,(x,y,z))
    elif len(variableList) == 2:
        for i in range(len(variableList)):
            functionList.append(sp.Eq(variableList[i][0]*x**2+variableList[i][1]*y**2+variableList[i][2]*x+variableList[i][3]*y,constantsList[i]))
        solution = sp.solve(functionList,(x,y))
    else:
        for i in range(len(variableList)):
            functionList.append(sp.Eq(variableList[i][0]*x**2+variableList[i][1]*x,constantsList[i]))
        solution = sp.solve(functionList,(x))
    resp.set_cookie('solution','&'.join(str(x) for x in solution))
    resp.set_cookie('variables', variables)
    resp.set_cookie('constants', constants)
    return resp
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
@app.route('/PDE',methods = ['POST','GET'])
def PDE():
    resp = make_response(render_template('PDE.html'))
    resp.set_cookie('variables', 'test')
    return resp
@app.route('/PDESolve',methods = ['POST','GET'])
def PDESolve():
    variables = request.cookies.get('variables')
    print(variables)
    variableList = variables.split("&")
    for i in range(len(variableList)):
        variableList[i] = float(variableList[i])
    return variableList
if __name__ == '__main__':
    app.run(debug=True)
