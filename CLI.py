import cmd
import sys
import datetime as dt
import Utilities as ut
import plotille as plt

class CLI(cmd.Cmd):

    def __init__(self, dataHandler):
        cmd.Cmd.__init__(self)
        self.prompt = '>>> '
        self.intro = "Type your command or write 'help' to see all available commands"
        self.__dataHandler = dataHandler


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


    def do_plotHistRates(self, args):
        self.__plotHistRates(args)


    def do_plotHistPrices(self, args):
        self.__plotHistPrices(args)


    def do_getHistPrices(self, args):
        self.__getHistPrices(args)


    def do_quit(self, arg):
        sys.exit(1)


    def __plotHistRates(self, args):
        self.__plotHistQuotes(args, 'fx')


    def __plotHistPrices(self, args):
        self.__plotHistQuotes(args, 'stock')


    def __plotHistQuotes(self, args, flag):
        try:
            ticker = args.split()[0]
        except:
            sys.stdout.write('Error: please enter at least the required inputs: ticker' + '\n')
            return
        try:
            if len(args.split()) == 1:
                sDate = self.__dataHandler.getMinDate(ticker, flag).strftime('%m/%d/%Y')
                eDate = self.__dataHandler.getMaxDate(ticker, flag).strftime('%m/%d/%Y')
            if len(args.split()) == 2:
                sDate = args.split()[1]
                eDate = self.__dataHandler.getMaxDate(ticker, flag).strftime('%m/%d/%Y')
            if len(args.split()) > 2:
                sDate = args.split()[1]
                eDate = args.split()[2]
        except: return

        try: sDate = dt.datetime.strptime(sDate, '%m/%d/%Y')
        except:
            sys.stdout.write('Error: please enter a valid start date, format must be: mm/dd/yyyy' + '\n')
            return
        try: eDate = dt.datetime.strptime(eDate, '%m/%d/%Y')
        except:
            sys.stdout.write('Error: please enter a valid end date, format must be: mm/dd/yyyy' + '\n')
            return
        try:
            if flag == 'stock': res = self.__dataHandler.getHistClose(ticker, flag, sDate, eDate)
            else: res = self.__dataHandler.getHistClose('OANDA:'+ticker+'_USD', flag, sDate, eDate)
        except: return

        if len(res.keys()) >= 2:
            fig = plt.Figure()
            fig.x_label = 'Time'
            fig.y_label = 'Prices'
            fig.width = 120
            fig.height = 30
            fig.set_x_limits(min_=list(res.keys())[0], max_=list(res.keys())[-1])
            fig.set_y_limits(min_=0.8*min(list(res.values())), max_=1.1*max(list(res.values())))
            fig.plot(res.keys(), res.values())
            sys.stdout.write('\n' + fig.show(legend=False) + '\n\n\n')
        else:
            sys.stdout.write('Error: Graph requires at least 2 values to be showed' + '\n')


    def __getHistPrices(self, args):
        try:
            ticker = args.split()[0]
            sDate = args.split()[1]
            eDate = args.split()[2]
            if len(args.split()) >= 4: currency = args.split()[3]
            else: currency = None
        except:
            sys.stdout.write('Error: please enter at least the required inputs: ticker, start date, end date' + '\n')
            return
        try: sDate = dt.datetime.strptime(sDate, '%m/%d/%Y')
        except:
            sys.stdout.write('Error: please enter a valid start date, format must be: mm/dd/yyyy' + '\n')
            return
        try: eDate = dt.datetime.strptime(eDate, '%m/%d/%Y')
        except:
            sys.stdout.write('Error: please enter a valid end date, format must be: mm/dd/yyyy' + '\n')
            return

        if currency == None:
            try:
                res =self.__dataHandler.getHistClose(ticker, 'stock', sDate, eDate)
                for i in res.keys(): sys.stdout.write(dt.datetime.strftime(i, '%m/%d/%Y') + ' ' + str(res[i]) + '\n')
            except: return
        else:
            res = {}
            try:
                stockRes = self.__dataHandler.getHistClose(ticker, 'stock', sDate, eDate)
            except: return
            try:
                currRes =  self.__dataHandler.getHistClose('OANDA:'+currency+'_USD', 'fx', sDate, eDate)
            except: return
            intersec = ut.intersection(list(stockRes.keys()), list(currRes.keys()))
            for i in intersec: res[i] = round(stockRes[i] / currRes[i], 2)
            for i in res.keys(): sys.stdout.write(dt.datetime.strftime(i, '%m/%d/%Y') + ' ' + str(res[i]) + '\n')