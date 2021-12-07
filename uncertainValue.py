# digits = (amount, number to multiply with)
# voorbeeld: U = 13 ± 0.3 V = UncertainValue(13, absolute=True, error=0.3, label="U [V]")
import numpy as np
from toolbox import addQuadrature, isNumber

class UncertainValue:

    def __init__(self, value, error, absolute = True, digits = (-1, -1), label = None):
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
        if isNumber(other):
            return UncertainValue(self.value + other, self.absoluteError, label=self.label)
        elif isinstance(other, UncertainValue):
            absoluteError = np.sqrt(addQuadrature([self.absoluteError, other.absoluteError]))
            return UncertainValue(self.value + other.value, absoluteError, label=f"({self.label}) + ({other.label})")
        raise ValueError("Operation not supported yet")

    def __sub__(self, other):
        if isNumber(other):
            return UncertainValue(self.value - other, self.absoluteError, label=self.label)
        elif isinstance(other, UncertainValue):
            absoluteError = np.sqrt(addQuadrature([self.absoluteError, other.absoluteError]))
            return UncertainValue(self.value - other.value, absoluteError, label=f"({self.label}) - ({other.label})")
        raise ValueError("Operation not supported yet")

    def __mul__(self, other): # add all possibilites for magic methods so you can create normal equations without wolfram.
        if isNumber(other):
            return UncertainValue(self.value * other, self.absoluteError * other, label=self.label)
        elif isinstance(other, UncertainValue):
            newValue = self.value * other.value
            relativeError = newValue * np.sqrt(addQuadrature([self.relativeError, other.relativeError]))
            return UncertainValue(newValue, relativeError, absolute = False, label=f"({self.label}) * ({other.label})")
        raise ValueError("Operation not supported yet")

    def __truediv__(self, other):
        if isNumber(other):
            return UncertainValue(self.value / other, self.absoluteError / other, label=self.label)
        elif isinstance(other, UncertainValue):
            newValue = self.value / other.value
            relativeError = newValue * np.sqrt(addQuadrature([self.relativeError, other.relativeError]))
            return UncertainValue(newValue, relativeError, absolute = False, label=f"({self.label}) / ({other.label})")
        raise ValueError("Operation not supported yet")

    def __pow__(self, exponent):
        if isNumber(exponent):
            return UncertainValue(self.value ** exponent, np.abs(exponent * self.value ** (exponent - 1)) * self.absoluteError, label=self.label)
        raise ValueError("Operation not supported yet")