from flask import Flask, render_template, make_response, request
from sympy.solvers import pdsolve
from sympy.abc import x, y
from sympy import Function, pprint, symbols
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
    resp = make_response(render_template('linearSolve.html'))
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
    resp = make_response(render_template('nonLinearSolve.html'))
    variables = request.cookies.get('variables').replace(",","@")
    constants = request.cookies.get('constants').replace(",","@")
    variableList = variables.split("&")
    constantsList = constants.split("@")
    for i in range(len(variableList)):
        variableList[i] = variableList[i].split("@")
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
    print('&'.join(str(x) for x in solution).replace(",","@").replace("(","").replace(")",""))
    resp.set_cookie('solution','&'.join(str(x) for x in solution).replace(",","@").replace("(","").replace(")",""))
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
    resp = make_response(render_template('ODESolve.html'))
    coefficients = request.cookies.get('coefficients').replace(",","@")
    initialConditions = request.cookies.get('initialConditions').replace(",","@")
    initialConditionsList = initialConditions.split('&')
    initialConditionsDict = {}
    for initialCondition in initialConditionsList:
        values = initialCondition.split("@")
        for i in range(len(values)):
            values[i] = float(values[i])
        initialConditionsDict[values[0]] = values[1:]
    coefficientsList = coefficients.split("@")
    for i in range(len(coefficientsList)):
        coefficientsList[i] = float(coefficientsList[i])
    x = sp.Symbol("x")
    f = sp.Function("f")(x)
    n = len(initialConditionsDict)
    diff_eq = sp.Eq(coefficientsList[0]*f.diff(x,x)+coefficientsList[1]*f.diff(x)+coefficientsList[2]*f,0)
    ics={}
    for key in initialConditionsDict:
        if key==0:
            ics.update({f.subs(x,initialConditionsDict[key][0]):initialConditionsDict[key][1]})
        if key==1:
            ics.update({f.diff().subs(x,initialConditionsDict[key][0]):initialConditionsDict[key][1]})
        if key==2:
            ics.update({f.diff(x,x).subs(x,initialConditionsDict[key][0]):initialConditionsDict[key][1]})
    ivp = sp.dsolve(diff_eq,ics = ics).rhs
    ans = str(ivp)
    s = ""
    if("**" in ans):
        s = ans.replace("**","^")
    elif("exp"in ans):
        s = ans.replace("exp","e^")
    else:
        s = ans
    solution = "f(x)=" + s
    resp.set_cookie('coefficients', coefficients)
    resp.set_cookie('initialConditions', initialConditions)
    resp.set_cookie('solution',solution)
    print(solution)
    return resp

@app.route('/PDE',methods = ['POST','GET'])
def PDE():
    resp = make_response(render_template('PDE.html'))
    resp.set_cookie('variables', 'test')
    return resp
@app.route('/PDESolve',methods = ['POST','GET'])
def PDESolve():
    resp = make_response(render_template('PDESolve.html'))
    variables = request.cookies.get('variables')
    variableList = variables.split("&")
    for i in range(len(variableList)):
        variableList[i] = float(variableList[i])
    #return variableList
    x,y = symbols("x,y")
    f = Function('f')
    u = f(x,y)
    ux = u.diff(x)
    uy = u.diff(y)
    a = variableList[0]
    b = variableList[1]
    c = variableList[2]
    genform = a*u + b*ux + c*uy
    pprint(genform)
    x = str(pdsolve(genform))
    y = x[3:len(x)-1]
    t = y.replace('exp','e^')
    w = ""
    if('**' in t):
        w = t.replace("**","^")
    else:
        w = t
    s = w[:7] + "=" + w[9:]
    resp.set_cookie('variables', variables)
    resp.set_cookie('solution',s.replace(",","|"))
    print(s.replace(",",";"))
    return resp
if __name__ == '__main__':
    app.run(debug=True)

