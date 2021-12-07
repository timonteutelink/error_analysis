import curvefitgui
import matplotlib.pyplot as plt
from uncertainvaluelist import UncertainValueList
import curvefitgui
#thinnk about this because maybe possibility to add multiple arrays and extract uncertainvalue from that if needed so taht its stored in most used format
#create UncertainValueList class to handle all the going from arrays of values and uncertainties to single object that can be used in plotting
# alse add possibilit of having the entire array have same uncertainty and the possibility to multiply these arrays (multiplies all underlying uncertain values) so that sets of data can be processed before being plotted
#add possibility for fits ass wel


def plotData(x, y, title=None):
    """
    inputs x and y are expected to be uncertainvaluelists
    """

    if not isinstance(x, UncertainValueList) or not isinstance(y, UncertainValueList):
        raise ValueError("inputs are not of instance UncertainValueList")
    
    xArray = x.values
    xerrArray = x.absoluteErrors
    yArray = y.values
    yerrArray = y.absoluteErrors

    plt.figure()

    plt.scatter(xArray, yArray)
    plt.errorbar(xArray, yArray, xerr=xerrArray, yerr=yerrArray, fmt="none", elinewidth=0.6)
    
    if x.label is not None:
        plt.xlabel(x.label)
    if y.label is not None:
        plt.ylabel(x.label)
    if title is not None:
        plt.title(title)
    
    plt.minorticks_on()
    plt.grid(which='major', color='#DDDDDD', linewidth=0.8)
    plt.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
    plt.show()

def fitLinearData(x, y):
    """
    inputs x and y are expected to be uncertainvaluelists
    returns output of linearfitgui
    """

    if not isinstance(x, UncertainValueList) or not isinstance(y, UncertainValueList):
        raise ValueError("inputs are not of instance UncertainValueList")
    
    return curvefitgui.linear_fit_gui(x.values, y.values, xerr=x.absoluteErrors, yerr=y.absoluteErrors, xlabel=x.label, ylabel=y.label)

def fitData(fitFunction, x, y):
    """
    inputs x and y are expected to be uncertainvaluelists
    returns output of curvefitgui
    """

    if not isinstance(x, UncertainValueList) or not isinstance(y, UncertainValueList):
        raise ValueError("inputs are not of instance UncertainValueList")
    
    return curvefitgui.linear_fit_gui(fitFunction, x.values, y.values, xerr=x.absoluteErrors, yerr=y.absoluteErrors, xlabel=x.label, ylabel=y.label)
