# digits = (amount, number to multiply with), valueUnit=(waarde, eenheid)
# voorbeeld: U = 13 ± 0.3 V UncertainValue(13, absolute=True, error=0.3, valueUnit=("U","V"))

import toolbox

class UncertainValue:

    def __init__(self, value, absolute = False, error = 0, digits = (-1, -1), valueUnit = ("", "")):
        self.value = value
        self.valueUnit = valueUnit

        self.absoluteError = 0
        self.relativeError = 0

        if absolute:
            self.absoluteError = error
            self.calculateRelativeError()
        else:
            self.relativeError = error
            self.calculateAbsoluteError()
        
        if digits[0] > -1:
            self.absoluteError += digits[0] * digits[1]
            self.calculateRelativeError()

    def setRelativeError(self, relativeError):
        self.relativeError = relativeError
        self.calculateAbsoluteError()

    def calculateRelativeError(self):
        self.relativeError = self.absoluteError / self.value
    
    def setAbsoluteError(self, absoluteError):
        self.absoluteError = absoluteError
        self.calculateRelativeError()
    
    def calculateAbsoluteError(self):
        self.absoluteError = self.relativeError * self.value

    def __str__(self):
        if not self.valueUnit[0]:
            return str(self.value) + " ± " + str(self.absoluteError)
        else:
            return self.valueUnit[0] + " = " + str(self.value) + " ± " + str(self.absoluteError) + " " + self.valueUnit[1]
    
    def __add__(self, other):
        #if self.valueUnit[0] != other
        error = toolbox.addQuadrature([self.absoluteError, other.absoluteError])
        return UncertainValue(self.value + other.value, absolute=True, error = error, valueUnit=self.valueUnit)
