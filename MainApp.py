import CLI
import DataHandler as dh
import MethodHandler as mh
import datetime as dt
import sys

sys.stdout.write('Welcome to FinData: a simple CLI for retrieving financial data from finnhub ' + '(v. 1.0 - 7 feb 2021)' + '\n')
token = input('Please enter your API key to get data from Finnhub: ')
token = 'c0f7i1748v6snrib4ca0'
dataHandler = dh.DataHandler(token)
methodHandler = mh.MethodHandler(dataHandler, token)
cli = CLI.CLI(methodHandler)
cli.cmdloop()


