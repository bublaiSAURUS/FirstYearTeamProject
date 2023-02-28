from sympy.polys.euclidtools import NotInvertible
import numpy as np

class LinearSystem:
  '''
  Class that stores the data for the linear system along with the functionality.
  '''

  def __init__(self, coefficients, constants):
    '''
    'coefficients': coefficient matrix for the system of equations
    'constants': constant vector for the system of equations
    '''
    self.coefficients = np.array(coefficients)
    self.constants = np.array(constants)
  
  def display(self):
    sln = self.solve_linear_system()
    num_var = len(sln)
    # displaying the system of equations
    variable_strings = []
    system_string = ''
    for i in range(num_var):
      variable_strings.append('x_'+str(i))
    for i in range(num_var):
      for j in range(num_var):
        if j > 0 and self.coefficients[i][j] >= 0:
          system_string += '+'+str(self.coefficients[i][j])+str(variable_strings[j])+' '
        else:
          system_string += str(self.coefficients[i][j])+str(variable_strings[j])+' '
      system_string += '= '+str(self.constants[i])+',\n'

    print('Equation:')
    print(system_string)

    if not self.solution_exists():
      print("The linear system does not have a solution.")
    # displaying the solution if it exists
    
    sln_string = '['
    for i in range(len(sln)):
      sln_string += 'x_'+str(i)+', '
    sln_string = sln_string[:len(sln_string)-2]
    sln_string += '] = '+str(sln)
    print('Solution:')
    print(sln_string)

  def inv(self):
    '''
    Returns the inverse of the coefficient matrix
    '''
    return list(np.linalg.inv(self.coefficients))
  
  def det(self):
    '''
    Returns the determinant of the coefficient matrix
    '''
    return np.linalg.det(self.coefficients)
  
  def rank(self):
    '''
    Returns the rank of the coefficient matrix
    '''
    return np.linalg.matrix_rank(self.coefficients)
  
  def dim(self):
    '''
    Returns the dimension coefficient matrix
    '''
    return self.coefficients.shape[0]
  
  def solution_exists(self):
    '''
    Returns a boolean to state if the solution exists
    '''
    return (self.rank() == self.dim()) and (self.det() != 0)

  def solve_linear_system(self):
    '''
    Returns the solution to the linear system under the assummption the solution exists
    '''
    if not self.solution_exists():
      return self.dim()*[None]

    return np.linalg.solve(self.coefficients, self.constants)