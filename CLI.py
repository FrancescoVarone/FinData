import cmd
import sys
import MethodHandler as mh

class CLI(cmd.Cmd):

    def __init__(self, methodHandler: mh.MethodHandler):
        cmd.Cmd.__init__(self)
        self.prompt = '>>> '
        self.intro = "Type your command or write 'help' to see all available commands"
        self.__methodHandler = methodHandler


    def help_getLastQuotes(self):
        sys.stdout.write('\n' + "Retrieves the last quotes (close/open/high/low) for the given ticker. Currency"
                                " is an optional parameter" + '\n')
        sys.stdout.write("Syntax is: 'getLastQuotes ticker currency'" + '\n')
        sys.stdout.write("Example: 'getLastQuotes AAPL GBP'" + '\n\n')


    def help_plotHistRates(self):
        sys.stdout.write('\n' + "Plots the historical rates for a given currency. StartDate and EndDate are optional"
                                " parameters" + '\n')
        sys.stdout.write("Syntax is: 'plotHistRates currency startDate endDate'" + '\n')
        sys.stdout.write("To get the whole rates history, just type: 'plotHistRates currency'" + '\n')
        sys.stdout.write("Example: 'plotHistRates AUD 12/01/2020 12/15/2020'" + '\n\n')


    def help_plotHistPrices(self):
        sys.stdout.write('\n' + "Plots the historical prices for a given ticker. StartDate and EndDate are optional"
                                " parameters" + '\n')
        sys.stdout.write("Syntax is: 'plotHistPrices ticker startDate endDate'" + '\n')
        sys.stdout.write("To get the whole prices history, just type: 'plotHistPrices ticker'" + '\n')
        sys.stdout.write("Example: 'plotHistPrices AAPL 12/01/2020 12/15/2020'" + '\n\n')


    def help_getHistPrices(self):
        sys.stdout.write("Gets the historical prices for a given ticker in a given time range. Currency is "
                         "an optianal parameter." + '\n')
        sys.stdout.write("Syntax is: getHistPrices ticker startDate endDate currency" + '\n')
        sys.stdout.write("Example: getHistPrices AAPL 12/01/2020 12/15/2020 GBP" + '\n')


    def help_quit(self):
        sys.stdout.write("Print 'quit' to exit the program" + '\n')


    def do_getLastQuotes(self, args):
        self.__methodHandler.getLastQuotes(args)


    def do_plotHistRates(self, args):
        self.__methodHandler.plotHistRates(args)


    def do_plotHistPrices(self, args):
        self.__methodHandler.plotHistPrices(args)


    def do_getHistPrices(self, args):
        self.__methodHandler.getHistPrices(args)


    def do_quit(self, arg):
        sys.exit(1)