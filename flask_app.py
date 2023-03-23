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
    resp = make_response(render_template('ODESolve.html'))
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
    resp.set_cookie('solution',s)
    print(s)
    return resp
if __name__ == '__main__':
    app.run(debug=True)


