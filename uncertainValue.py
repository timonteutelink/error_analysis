# digits = (amount, number to multiply with)
# voorbeeld: U = 13 ± 0.3 V = UncertainValue(13, absolute=True, error=0.3, label="U [V]")
import math
import toolbox

class UncertainValue:

    def __init__(self, value, absolute = False, error = 0, digits = (-1, -1), label = ""):
        self.value = value
        self.label = label

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
        if self.label is not None:
            return f"{self.value} ± {self.absoluteError} ({self.label})"
        else:
            return f"{self.value} ± {self.absoluteError}"
    
    def __add__(self, other):
        absoluteError = math.sqrt(toolbox.addQuadrature([self.absoluteError, other.absoluteError]))
        return UncertainValue(self.value + other.value, absolute = True, error = absoluteError, label=f"({self.label}) + ({other.label})")

    def __sub__(self, other):
        absoluteError = math.sqrt(toolbox.addQuadrature([self.absoluteError, other.absoluteError]))
        return UncertainValue(self.value - other.value, absolute = True, error = absoluteError, label=f"({self.label}) - ({other.label})")

    def __mul__(self, other): # add all possibilites for magic methods so you can create normal equations without wolfram.
        newValue = self.value * other.value
        relativeError = newValue * math.sqrt(toolbox.addQuadrature([self.relativeError, other.relativeError]))
        return UncertainValue(newValue, absolute = False, error = relativeError, label=f"({self.label}) * ({other.label})")

    def __truediv__(self, other):
        newValue = self.value / other.value
        relativeError = newValue * math.sqrt(toolbox.addQuadrature([self.relativeError, other.relativeError]))
        return UncertainValue(newValue, absolute = False, error = relativeError, label=f"({self.label}) / ({other.label})")
