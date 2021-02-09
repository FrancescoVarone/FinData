#This class represents the DB in which stocks data are stored
#To do:
    #Insert a timeout when loading DB
    #Better error handling (if wrong token? if no connection?)
    #Load stockTickers from csv
    #Get full time interval data


import json
import datetime as dt
import math as mt
import urllib.request
import time as tm
import sys


class DataHandler():
    def __init__(self, token: str):
        self.__stockTickers = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'FB', 'GOOGL']
        self.__fxTickers = ['OANDA:AUD_USD', 'OANDA:EUR_USD', 'OANDA:GBP_USD']
        self.__token = token
        self.__data = {'stock':{}, 'fx': {}}
        for ticker in self.__stockTickers: self.__data['stock'][ticker] = {}
        for ticker in self.__fxTickers: self.__data['fx'][ticker] = {}
        self.__eDate = dt.datetime.today() - dt.timedelta(days=1)
        self.__sDate = dt.datetime(year=self.__eDate.year-1, month=self.__eDate.month, day=self.__eDate.day)
        self.__eDateUnix = str(mt.trunc(self.__eDate.timestamp()))
        self.__sDateUnix = str(mt.trunc(self.__sDate.timestamp()))
        self.__loadStockData()
        self.__loadFxData()


    def __loadStockData(self):
        for i in range(0, len(self.__stockTickers)):
            ticker = self.__stockTickers[i]
            res = None
            url = 'https://finnhub.io/api/v1/stock/profile2?symbol=' + ticker + '&token=' + self.__token
            while res == None:
                try: res = urllib.request.urlopen(url)
                except: tm.sleep(1)
            self.__data['stock'][ticker]['anag'] = json.load(res)
            tm.sleep(0.5)
            sys.stdout.write('\r')
            sys.stdout.write('Loading DB with stock anagraphic data. Please wait... ' + str(mt.trunc((i+1)/len(self.__stockTickers)*100)) + '%')
        sys.stdout.write('\n')

        for i in range(0, len(self.__stockTickers)):
            ticker = self.__stockTickers[i]
            res = None
            url = 'https://finnhub.io/api/v1/stock/candle?symbol=' + ticker + '&resolution=D&from=' + self.__sDateUnix + \
                   '&to=' + self.__eDateUnix + '&token=' + self.__token
            while res == None:
                try: res = urllib.request.urlopen(url)
                except: tm.sleep(1)
            self.__data['stock'][ticker]['quotes'] = json.load(res)
            tm.sleep(0.5)
            sys.stdout.write('\r')
            sys.stdout.write('Loading DB with stock price data. Please wait... ' + str(mt.trunc((i+1)/len(self.__stockTickers)*100)) + '%')
        sys.stdout.write('\n')

        #Convert unix time stamps to dates
        for ticker in self.__stockTickers:
            for i in range(0, len(self.__data['stock'][ticker]['quotes']['t'])):
                date = dt.datetime.utcfromtimestamp(self.__data['stock'][ticker]['quotes']['t'][i])
                self.__data['stock'][ticker]['quotes']['t'][i] = dt.datetime(date.year, date.month, date.day)


    def __loadFxData(self):
        for i in range(0, len(self.__fxTickers)):
            ticker = self.__fxTickers[i]
            res = None
            url = 'https://finnhub.io/api/v1/forex/symbol?exchange=oanda&token=' + self.__token
            while res == None:
                try: res = urllib.request.urlopen(url)
                except: tm.sleep(1)
            for j in json.load(res):
                if j['symbol'] == ticker: self.__data['fx'][ticker]['anag'] = j
            tm.sleep(0.5)
            sys.stdout.write('\r')
            sys.stdout.write('Loading DB with forex anagraphic data. Please wait... ' + str(mt.trunc((i+1)/len(self.__fxTickers)*100)) + '%')
        sys.stdout.write('\n')

        for i in range(0, len(self.__fxTickers)):
            ticker = self.__fxTickers[i]
            res = None
            url = 'https://finnhub.io/api/v1/forex/candle?symbol=' + ticker + '&resolution=D&from=' + self.__sDateUnix \
                  + '&to=' +self.__eDateUnix + '&token=' + self.__token
            while res == None:
                try: res = urllib.request.urlopen(url)
                except: tm.sleep(1)
            self.__data['fx'][ticker]['quotes'] = json.load(res)
            tm.sleep(0.5)
            sys.stdout.write('\r')
            sys.stdout.write('Loading DB with forex rates. Please wait... ' + str(mt.trunc((i+1)/len(self.__fxTickers)*100)) + '%')
        sys.stdout.write('\n')

        #Convert unix time stamps to dates
        for ticker in self.__fxTickers:
            for i in range(0, len(self.__data['fx'][ticker]['quotes']['t'])):
                date = dt.datetime.utcfromtimestamp(self.__data['fx'][ticker]['quotes']['t'][i])
                self.__data['fx'][ticker]['quotes']['t'][i] = dt.datetime(date.year, date.month, date.day)


    def getHistClose(self, ticker: str, flag: str, sDate: dt.datetime, eDate: dt.datetime):
        if sDate > eDate : return 'Error: start date cannot be greater than end date'
        try: dummy = self.__data[flag][ticker]
        except:
            if flag == 'stock': sys.stdout.write('Ticker not included in the Database' + '\n')
            else: sys.stdout.write('Currency not included in the Database' + '\n')

        # Setting eIndex
        resDic = {}
        if eDate >= self.__data[flag][ticker]['quotes']['t'][-1]:
            eIndex = len(self.__data[flag][ticker]['quotes']['t']) - 1
        else:
            i = 0
            while self.__data[flag][ticker]['quotes']['t'][i] <= eDate: i = i + 1
            eIndex = i - 1

        #Setting sIndex
        if sDate <= self.__data[flag][ticker]['quotes']['t'][0]: sIndex = 0
        else:
            i = 0
            while self.__data[flag][ticker]['quotes']['t'][i] < sDate: i = i + 1
            sIndex = i

        for i in range(sIndex, eIndex+1):
            resDic[self.__data[flag][ticker]['quotes']['t'][i]] = self.__data[flag][ticker]['quotes']['c'][i]
        return resDic


    def getHistCloseMaxInt(self, ticker: str, flag: str):
        maxSdate = self.__data[flag][ticker]['quotes']['t'][0]
        maxEdate = self.__data[flag][ticker]['quotes']['t'][-1]
        return self.getHistClose(ticker, flag, maxSdate, maxEdate)