#Utility functions used by classes

import datetime as dt
import sys

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def parseArgs(argsObtained: str, argsExp: dict): #argsExp is {argName:{type: xxx, req: xxx}, ...}
    argsObtained = argsObtained.split() #list of args obtained
    argsDic = {} #dict that will be returned by the function {argName: value}
    argsNames = list(argsExp.keys()) #names of the expected args

    for i in range(0, len(argsObtained)):
        argsDic[argsNames[i]] = argsObtained[i]

    for name in argsNames:
        if (argsExp[name]['req'] == 1) and (not(name in list(argsDic.keys()))):
            sys.stdout.write('Error: ' + name + ' is a required parameter' + '\n')
            raise Exception()
        if (argsExp[name]['type'] == 'Date') and (name in list(argsDic.keys())):
            try:
                argsDic[name] = dt.datetime.strptime(argsDic[name], '%m/%d/%Y')
            except:
                sys.stdout.write('Error: please enter a valid date for ' + name +'\n')
                raise Exception()

    return argsDic