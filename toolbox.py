import requests

def addQuadrature(items):
    sum = 0
    for i in range(len(items)):
        sum += items[i] ** 2
    return sum

def calculateDerivative(equation, variables, valueReplacements = {}):
    query = {"_key": "s123456", "equation": equation, "variables": ",".join(variables)}

    response = requests.get('https://www.wolframcloud.com/obj/c63c2a45-29d6-4b06-a847-d7b0174b081b', params = query)

    if response.status_code == 200:        
        derivatives = response.text.strip("{} ").split(", ")
        derivatives = [derivative.strip() for derivative in derivatives]
        
        error = "Sqrt[" + " + ".join(["Power[" + derivatives[i] + " * d" + variables[i] + ", 2]" for i in range(len(variables))]) + "]"

        if valueReplacements:
            value = calculate(error, valueReplacements)
            return (error, value)

        return error
    
    return None

def calculate(equation, values):
    query = {"_key": "s123456", "equation": equation, "values": "{" + ",".join([key + '->' + str(value) for key, value in values.items()]) + "}"}

    response = requests.get('https://www.wolframcloud.com/obj/c4b5e27d-ec4e-409a-a607-8d4779c35019', params = query)

    if response.status_code == 200:
        value = float(response.text)
        return value

    return None

