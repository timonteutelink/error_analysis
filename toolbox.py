import requests

def addQuadrature(items):
    sum = 0
    for i in range(len(items)):
        sum += items[i] ** 2
    return sum

def determinePartialDerivatives(expression, variables):
    query = {"_key": "s123456", "equation": expression, "variables": ",".join(variables)}

    response = requests.get('https://www.wolframcloud.com/obj/9fded9fa-60fa-44eb-a981-a5e6e4ced725', params = query)

    if response.status_code == 200:        
        derivatives = response.text.strip("{} ").split(", ")
        derivatives = [derivative.strip() for derivative in derivatives]
        
        return derivatives

    return None

def determineErrorExpression(derivatives, variables):
    return "Sqrt[" + " + ".join(["Power[" + derivatives[i] + " * d" + variables[i] + ", 2]" for i in range(len(variables))]) + "]"

def evaluateExpression(expression, values):
    query = {"_key": "s123456", "equation": expression, "values": "{" + ",".join([key + '->' + str(value) for key, value in values.items()]) + "}"}

    response = requests.get('https://www.wolframcloud.com/obj/2ae6436e-7168-46b8-822a-8a85a3f906b4', params = query)

    if response.status_code == 200:
        value = float(response.text)
        return value

    return None

