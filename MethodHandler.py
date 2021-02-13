import sys
import datetime as dt
import Utilities as ut
import plotille as plt
import urllib.request
import json
import DataHandler as dh


class MethodHandler():
    def __init__(self, dataHandler: dh.DataHandler, token: str):
        self.__dataHandler = dataHandler
        self.__token = token

    def getLastQuotes(self, args):
        try:
            ticker = args.split()[0]
        except:
            sys.stdout.write('Error: please enter at least the required inputs: ticker' + '\n')
            return
        if len(args.split()) >= 2:
            currency = args.split()[1]
            urlCurrency = 'https://finnhub.io/api/v1/forex/rates?base=USD&token=' + self.__token
            resCurrency = urllib.request.urlopen(urlCurrency)
            try:
                fxRate = json.load(resCurrency)['quote'][currency]
            except:
                sys.stdout.write('Error: currency not available' +'\n')
                return
        else:
            fxRate = 1

        urlStock = 'https://finnhub.io/api/v1/quote?symbol=' + ticker + '&token=' + self.__token
        resStock = urllib.request.urlopen(urlStock)
        stockDic = json.load(resStock)
        sys.stdout.write('Close: ' + str(round(stockDic['c'] * fxRate, 2)) + '\n')
        sys.stdout.write('High: ' + str(round(stockDic['h'] * fxRate, 2)) + '\n')
        sys.stdout.write('Low: ' + str(round(stockDic['l'] * fxRate, 2)) + '\n')
        sys.stdout.write('Open: ' + str(round(stockDic['o'] * fxRate, 2)) + '\n')


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
        except:
            return

        try:
            sDate = dt.datetime.strptime(sDate, '%m/%d/%Y')
        except:
            sys.stdout.write('Error: please enter a valid start date, format must be: mm/dd/yyyy' + '\n')
            return
        try:
            eDate = dt.datetime.strptime(eDate, '%m/%d/%Y')
        except:
            sys.stdout.write('Error: please enter a valid end date, format must be: mm/dd/yyyy' + '\n')
            return
        try:
            if flag == 'stock':
                res = self.__dataHandler.getHistClose(ticker, flag, sDate, eDate)
            else:
                res = self.__dataHandler.getHistClose('OANDA:' + ticker + '_USD', flag, sDate, eDate)
        except:
            return

        if len(res.keys()) >= 2:
            fig = plt.Figure()
            fig.x_label = 'Time'
            fig.y_label = 'Prices'
            fig.width = 120
            fig.height = 30
            fig.set_x_limits(min_=list(res.keys())[0], max_=list(res.keys())[-1])
            fig.set_y_limits(min_=0.8 * min(list(res.values())), max_=1.1 * max(list(res.values())))
            fig.plot(res.keys(), res.values())
            sys.stdout.write('\n' + fig.show(legend=False) + '\n\n\n')
        else:
            sys.stdout.write('Error: Graph requires at least 2 values to be showed' + '\n')


    def getHistPrices(self, args):
        try:
            ticker = args.split()[0]
            sDate = args.split()[1]
            eDate = args.split()[2]
            if len(args.split()) >= 4:
                currency = args.split()[3]
            else:
                currency = None
        except:
            sys.stdout.write('Error: please enter at least the required inputs: ticker, start date, end date' + '\n')
            return
        try:
            sDate = dt.datetime.strptime(sDate, '%m/%d/%Y')
        except:
            sys.stdout.write('Error: please enter a valid start date, format must be: mm/dd/yyyy' + '\n')
            return
        try:
            eDate = dt.datetime.strptime(eDate, '%m/%d/%Y')
        except:
            sys.stdout.write('Error: please enter a valid end date, format must be: mm/dd/yyyy' + '\n')
            return

        if currency == None:
            try:
                res = self.__dataHandler.getHistClose(ticker, 'stock', sDate, eDate)
                for i in res.keys(): sys.stdout.write(dt.datetime.strftime(i, '%m/%d/%Y') + ' ' + str(res[i]) + '\n')
            except:
                return
        else:
            res = {}
            try:
                stockRes = self.__dataHandler.getHistClose(ticker, 'stock', sDate, eDate)
            except:
                return
            try:
                currRes = self.__dataHandler.getHistClose('OANDA:' + currency + '_USD', 'fx', sDate, eDate)
            except:
                return
            intersec = ut.intersection(list(stockRes.keys()), list(currRes.keys()))
            for i in intersec: res[i] = round(stockRes[i] / currRes[i], 2)
            for i in res.keys(): sys.stdout.write(dt.datetime.strftime(i, '%m/%d/%Y') + ' ' + str(res[i]) + '\n')


    def plotHistRates(self, args):
        self.__plotHistQuotes(args, 'fx')


    def plotHistPrices(self, args):
        self.__plotHistQuotes(args, 'stock')