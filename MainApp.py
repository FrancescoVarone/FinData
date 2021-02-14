import CLI
import DataHandler as dh
import MethodHandler as mh
import sys

sys.stdout.write('Welcome to FinData: a simple CLI for retrieving financial data from finnhub ' + '(v. 1.0 - 14 feb 2021)' + '\n')
token = 'c0f7i1748v6snrib4ca0'
dataHandler = dh.DataHandler(token)
dataHandler.load_db()
methodHandler = mh.MethodHandler(dataHandler, token)
cli = CLI.CLI(methodHandler)
cli.cmdloop()


