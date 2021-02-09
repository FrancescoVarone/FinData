import cmd
import sys
import datetime as dt

class CLI(cmd.Cmd):

    def __init__(self, dataHandler):
        cmd.Cmd.__init__(self)
        self.prompt = '>>> '
        self.intro = "Type your command or write 'help' to see all available commands"
        self.__dataHandler = dataHandler


    def __intersection(self, lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3


    def do_getHistPrices(self, args):
        self.__getHistPrices(args)


    def __getHistPrices(self, args):
        try:
            ticker = args.split()[0]
            sDate = args.split()[1]
            eDate = args.split()[2]
            if len(args.split()) >= 4: currency = args.split()[3]
            else: currency = None
        except:
            sys.stdout.write('Please enter at least the required inputs: ticker, start date, end date' + '\n')
            return False
        try: sDate = dt.datetime.strptime(sDate, '%m/%d/%Y')
        except:
            sys.stdout.write('Please enter a valid start date, format must be: mm/dd/yyyy' + '\n')
            return False
        try: eDate = dt.datetime.strptime(eDate, '%m/%d/%Y')
        except:
            sys.stdout.write('Please enter a valid end date, format must be: mm/dd/yyyy' + '\n')
            return False

        try:
            if currency == None:
                res =self.__dataHandler.getHistClose(ticker, 'stock', sDate, eDate)
                for i in res.keys(): sys.stdout.write(dt.datetime.strftime(i, '%m/%d/%Y') + ' ' + str(res[i]) + '\n')
            else:
                res = {}
                stockRes = self.__dataHandler.getHistClose(ticker, 'stock', sDate, eDate)
                currRes =  self.__dataHandler.getHistClose('OANDA:'+currency+'_USD', 'fx', sDate, eDate)
                intersec = self.__intersection(list(stockRes.keys()), list(currRes.keys()))
                for i in intersec: res[i] = round(stockRes[i] / currRes[i], 2)
                for i in res.keys(): sys.stdout.write(dt.datetime.strftime(i, '%m/%d/%Y') + ' ' + str(res[i]) + '\n')
        except: return False


    def do_quit(self, arg):
        sys.exit(1)

    # shortcuts
    do_q = do_quit