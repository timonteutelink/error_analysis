from uncertainValue import UncertainValue
import toolbox

class Formula():

    def __init__(self, formula):
        self.formula = formula
        self.values = []

    def addValue(self, value, absolute = False, error = 0, digits = (-1, -1), valueUnit = ("", "")):
        self.values.append(UncertainValue(value, absolute = absolute, error = error, digits = digits, valueUnit = valueUnit))

    def getPartialDerivatives(self):
        return toolbox.calculateDerivative(self.formula, [value.valueUnit[0] for value in self.values])
    
    


def calculateFormula(formula, uncertainValues, valueUnit = ("", ""), error = False):
    values = {}
    variables = []
    for uncertainValue in uncertainValues:
        values[uncertainValue.valueUnit[0]] = uncertainValue.value
        values["d" + uncertainValue.valueUnit[0]] = uncertainValue.absoluteError
        variables.append(uncertainValue.valueUnit[0])
    print(values)

    newValue = toolbox.calculate(formula, values)
    errorFormula, newError = toolbox.calculateDerivative(formula, variables, values)
    
    returnValue = UncertainValue(newValue, absolute=True, error=newError, valueUnit=valueUnit)

    if error:
        return (returnValue, errorFormula)
    else:
        return returnValue