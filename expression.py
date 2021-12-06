from numpy import Infinity
from uncertainValue import UncertainValue
import toolbox

#add erro handling and checks if wolfram messages arent completed and cant get uncertainvalue

class Expression():
    """
    This class is used to perform error analysis on complex equations.
    
    """

    def __init__(self, expression, label=""):
        """
        The constructor takes an expression in as a string. This string is sent to wolframcloud so the equation has to be in wolfram format.
        """
        self.expression = expression
        self.label = label
        self.variables = {}

        self.derivatives = []
        self.errorExpression = ""
        self.resultingUncertainValue = None

    def addVariable(self, variableName):
        self.setVariable(variableName)

    def setVariable(self, variableName, uncertainValue, value = Infinity, error = 0, absolute = False, digits = (-1, -1)):
        if uncertainValue is not None:
            self.variables[variableName] = uncertainValue
        else:
            self.variables[variableName] = UncertainValue(value, absolute = absolute, error = error, digits = digits)

    def getPartialDerivatives(self):
        if len(self.derivatives) < 1:
            self.derivatives = toolbox.determinePartialDerivatives(self.expression, list(self.variables.keys()))
        
        return self.derivatives
    
    def getErrorExpression(self):
        if not self.errorExpression:
            self.errorExpression = toolbox.determineErrorExpression(self.getPartialDerivatives(), list(self.variables.keys()))
            
        return self.errorExpression

    def getUncertainValue(self):
        if not self.resultingUncertainValue:
            values = {}
            
            for variableName, uncertainValue in self.variables.items():
                values[variableName] = uncertainValue.value
                values["d" + variableName] = uncertainValue.absoluteError

            newValue = toolbox.evaluateExpression(self.expression, values)
            newError = toolbox.evaluateExpression(self.getErrorExpression(), values)

            self.resultingUncertainValue = UncertainValue(newValue, absolute=True, error=newError, label=self.label)

        return self.resultingUncertainValue

    def __str__(self):
        return self.getUncertainValue().__str__()
