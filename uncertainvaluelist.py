import numpy as np
from toolbox import addQuadrature, isNumpyArray, isNumber
from uncertainValue import UncertainValue

class UncertainValueList():

    def __init__(self, values, error, absolute = True, digits = (-1, -1), label=None):
        self.label = label

        if isNumpyArray(values):
            self.values = values
        else:
            raise TypeError("Values parameter is a numpy array.")

        uncertainties = None

        if isNumpyArray(error):
            if len(error) != len(values):
                raise ValueError("Values array and uncertainties array are not the same size.")
            uncertainties = error
        elif isNumber(error):
            uncertainties = np.ones(len(values)) * error
        else:
            raise TypeError("Uncertainty is not a number or a numpy array.")

        self.absoluteErrors = 0
        self.relativeErrors = 0

        if absolute:
            self.absoluteErrors = uncertainties
            self.calculateRelativeError()
        else:
            self.relativeErrors = uncertainties
            self.calculateAbsoluteError()
        
        if digits[0] > -1:
            self.absoluteErrors += digits[0] * digits[1]
            self.calculateRelativeError()

    def calculateRelativeError(self):
        self.relativeErrors = self.absoluteErrors / self.values
        
    def calculateAbsoluteError(self):
        self.absoluteErrors = self.relativeErrors * self.values

    def getValueAtIndex(self, index):
        return UncertainValue(self.values[index], self.absoluteErrors[index], label=self.label)

    def __str__(self):
        values = np.array2string(self.values, separator=',', threshold=6)
        absoluteErrors = np.array2string(self.absoluteErrors, separator=',', threshold=6)

        if self.label is not None:
            return f"{values} ± {absoluteErrors} ({self.label})"
        else:
            return f"{values} ± {absoluteErrors}"

    def __add__(self, other):
        if isNumber(other):
            return UncertainValueList(self.values + other, self.absoluteErrors, label=self.label)

        if isinstance(other, UncertainValueList):
            newLabel = None
            if self.label is not None and other.label is None:
                newLabel = self.label
            elif self.label is None and other.label is not None:
                newLabel = other.label
            elif self.label is not None and other.label is not None:
                newLabel = f"({self.label}) + ({other.label})"

            absoluteErrors = np.sqrt(addQuadrature([self.absoluteErrors, other.absoluteErrors]))
            return UncertainValueList(self.values + other.values, absoluteErrors, label=newLabel)
        
        if isinstance(other, UncertainValue):
            newLabel = None
            if self.label is not None and other.label is None:
                newLabel = self.label
            elif self.label is None and other.label is not None:
                newLabel = other.label
            elif self.label is not None and other.label is not None:
                newLabel = f"({self.label}) + ({other.label})"

            absoluteErrors = np.sqrt(addQuadrature([self.absoluteErrors, other.absoluteError]))
            return UncertainValueList(self.values + other.value, absoluteErrors, label=newLabel)

        raise ValueError("Operation not supported yet")

    __radd__ = __add__

    def __sub__(self, other):
        if isNumber(other):
            return UncertainValueList(self.values + other, self.absoluteErrors, label=self.label)
        
        if isinstance(other, UncertainValueList):
            newLabel = None
            if self.label is not None and other.label is None:
                newLabel = self.label
            elif self.label is None and other.label is not None:
                newLabel = other.label
            elif self.label is not None and other.label is not None:
                newLabel = f"({self.label}) - ({other.label})"

            absoluteErrors = np.sqrt(addQuadrature([self.absoluteErrors, other.absoluteErrors]))
            return UncertainValueList(self.values - other.values, absoluteErrors, label=newLabel)
        
        if isinstance(other, UncertainValue):
            newLabel = None
            if self.label is not None and other.label is None:
                newLabel = self.label
            elif self.label is None and other.label is not None:
                newLabel = other.label
            elif self.label is not None and other.label is not None:
                newLabel = f"({self.label}) - ({other.label})"

            absoluteErrors = np.sqrt(addQuadrature([self.absoluteErrors, other.absoluteError]))
            return UncertainValueList(self.values - other.value, absoluteErrors, label=newLabel)

        raise ValueError("Operation not supported yet")

    def __rsub__(self, other):
        return other - self

    def __mul__(self, other): # add all possibilites for magic methods so you can create normal equations without wolfram.
        if isNumber(other):
            return UncertainValueList(self.values * other, self.absoluteErrors * other, label=self.label)
        
        if isinstance(other, UncertainValueList):
            newLabel = None
            if self.label is not None and other.label is None:
                newLabel = self.label
            elif self.label is None and other.label is not None:
                newLabel = other.label
            elif self.label is not None and other.label is not None:
                newLabel = f"({self.label}) * ({other.label})"
            
            newValues = self.values * other.values
            relativeErrors = newValues * np.sqrt(addQuadrature([self.relativeErrors, other.relativeErrors]))
            return UncertainValueList(newValues, relativeErrors, absolute = False, label=newLabel)
        
        if isinstance(other, UncertainValue):
            newLabel = None
            if self.label is not None and other.label is None:
                newLabel = self.label
            elif self.label is None and other.label is not None:
                newLabel = other.label
            elif self.label is not None and other.label is not None:
                newLabel = f"({self.label}) + ({other.label})"

            newValues = self.values * other.value
            relativeErrors = newValues * np.sqrt(addQuadrature([self.relativeErrors, other.relativeError]))
            return UncertainValueList(newValues, relativeErrors, absolute = False, label=newLabel)

        raise ValueError("Operation not supported yet")

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isNumber(other):
            return UncertainValueList(self.values / other, self.absoluteErrors / other, label=self.label)
        
        if isinstance(other, UncertainValueList):
            newLabel = None
            if self.label is not None and other.label is None:
                newLabel = self.label
            elif self.label is None and other.label is not None:
                newLabel = other.label
            elif self.label is not None and other.label is not None:
                newLabel = f"({self.label}) / ({other.label})"

            newValue = self.values / other.values
            relativeError = newValue * np.sqrt(addQuadrature([self.relativeErrors, other.relativeErrors]))
            return UncertainValueList(newValue, relativeError, absolute = False, label=newLabel)
        
        if isinstance(other, UncertainValue):
            newLabel = None
            if self.label is not None and other.label is None:
                newLabel = self.label
            elif self.label is None and other.label is not None:
                newLabel = other.label
            elif self.label is not None and other.label is not None:
                newLabel = f"({self.label}) + ({other.label})"

            newValues = self.values / other.value
            relativeErrors = newValues * np.sqrt(addQuadrature([self.relativeErrors, other.relativeError]))
            return UncertainValueList(newValues, relativeErrors, absolute = False, label=newLabel)

        raise ValueError("Operation not supported yet")

    def __rtruediv__(self, other):
        return other * self ** -1

    def __pow__(self, exponent):
        if isNumber(exponent):
            return UncertainValueList(self.values ** exponent, np.abs(exponent * self.values ** (exponent - 1)) * self.absoluteErrors, label=self.label)
        
        raise ValueError("Operation not supported yet")