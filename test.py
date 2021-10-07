from uncertainValue import UncertainValue
from formula import calculateFormula, UncertainValue

def main():
    L = UncertainValue(20, absolute = True, error = 0.1, valueUnit=("L", "m"))
    W = UncertainValue(40, absolute = True, error = 0.2, valueUnit=("W", "m"))

    C = calculateFormula("2 * W + 2 * L", [L, W], valueUnit=("C", "m"))
    print(C)
    

if __name__ == "__main__":
    main()