# The present script is used to run properly the program.
# It creates the objects for the three main classes (CLI, DataHandler and MethodHandler) and initializes
# the cmdloop in which user's commands are processed.


import cli
import data_handler as dh
import method_handler as mh
import sys

sys.stdout.write(
    'Welcome to FinData: a simple CLI for retrieving financial data from finnhub ' + '(v. 1.0 - 14 feb 2021)' + '\n')
token = 'c0f7i1748v6snrib4ca0'
dataHandler = dh.DataHandler(token)
dataHandler.load_db()
methodHandler = mh.MethodHandler(dataHandler, token)
cli_app = cli.CLI(methodHandler)
cli_app.cmdloop()
