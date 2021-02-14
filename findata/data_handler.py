# The present class contains the DB of the program and the methods to query the DB.
# The DB is the attribute 'data' of this class. As a private attribute it can be modified only by the methods
#   of this class. This avoids other parts of the code to harm the integrity of the data.

# The attribute 'data' is a dict. It contains two main keys to separate stock data from fx data:
#   data.keys() = ['stock', 'fx']

# The stock data are stored in the following manner:
#       data['stock'].keys() = [ticker1, ticker2, ...]
#           data['stock'][ticker].keys() = ['anag', 'quotes']
#               data['stock'][ticker]['anag'].keys() = ['country', 'currency', ...]
#               data['stock'][ticker]['quotes'].keys() = ['c', 'h', 't', ...]

# The fx data are organized in the following manner:
#       data['fx'].keys() = [ticker1, ticker2, ...]
#           data['fx'][ticker].keys() = ['anag', 'quotes']
#               data['fx'][ticker]['anag'].keys() = ['description', 'displaySymbol', ...]
#               data['fx'][ticker]['quotes'].keys() = ['c', 'h', 't', ...]

# The duties of the class are:
#   - to load data from finnhub (by using 'load_db' method)
#   - to perform simple queries to get the data (mainly by using 'get_hist_close' method)

# ToDo:
#   - check if data can be retrieved faster from finnhub by using the appropriate library
#   - catch the absence of connection with an appropriate Exception

import json
import datetime as dt
import math as mt
import urllib.request
import urllib.error
import time as tm
import sys


class DataHandler:
    def __init__(self, token: str):
        self.__stock_tickers = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'FB', 'GOOGL', 'GOOG', 'BRK.B', 'JNJ', 'JPM', 'V',
                                'NVDA', 'DIS', 'PG', 'PYPL', 'UNH', 'HD', 'MA', 'BAC', 'NFLX', 'INTC', 'CMCSA', 'ADBE',
                                'VZ', 'CRM', 'ABT', 'T', 'XOM', 'CSCO', 'WMT', 'PFE', 'TMO', 'PEP', 'MRK', 'ABBV',
                                'AVGO', 'KO', 'NKE', 'CVX', 'QCOM', 'NEE', 'ACN', 'LLY', 'TXN', 'MDT', 'MCD', 'COST',
                                'DHR', 'HON', 'BMY', 'AMGN', 'UNP', 'WFC', 'LIN', 'PM', 'C', 'LOW', 'SBUX', 'ORCL',
                                'UPS', 'NOW', 'BA', 'RTX', 'IBM', 'AMD', 'CAT', 'BLK', 'MS', 'INTU', 'AMT', 'MMM', 'GS',
                                'GE', 'DE', 'CVS', 'TGT', 'AMAT', 'MU', 'CHTR', 'ISRG', 'BKNG', 'LMT', 'GILD', 'FIS',
                                'SCHW', 'TJX', 'AXP', 'MDLZ', 'MO', 'SPGI', 'PLD', 'SYK', 'TMUS', 'LRCX', 'ZTS', 'CI',
                                'BDX', 'CB', 'ANTM', 'ADP']
        self.__fx_tickers = ['OANDA:AUD_USD', 'OANDA:EUR_USD', 'OANDA:GBP_USD']
        self.__token = token
        self.__data = {'stock': {}, 'fx': {}}
        for ticker in self.__stock_tickers:
            self.__data['stock'][ticker] = {}
        for ticker in self.__fx_tickers:
            self.__data['fx'][ticker] = {}
        self.__e_date = dt.datetime.today() - dt.timedelta(days=1)
        self.__s_date = dt.datetime(year=self.__e_date.year - 1, month=self.__e_date.month, day=self.__e_date.day)
        self.__e_date_unix = str(mt.trunc(self.__e_date.timestamp()))
        self.__s_date_unix = str(mt.trunc(self.__s_date.timestamp()))

    def get_currencies(self) -> list:
        ls = []
        for i in list(self.__data['fx'].keys()):
            ls.append(self.__data['fx'][i]['anag']['displaySymbol'])
        return ls

    def get_stocks(self) -> list:
        return list(self.__data['stock'].keys())

    def load_db_manually(self, ticker: str, data: dict) -> None:
        self.__data['stock'][ticker]['quotes'] = {}
        self.__data['stock'][ticker]['quotes']['t'] = list(data.keys())
        self.__data['stock'][ticker]['quotes']['c'] = list(data.values())

    def load_db(self) -> None:
        self.__load_stock_data()
        self.__load_fx_data()

    def __load_stock_data(self) -> None:
        """"Gets from finnhub anagraphic data and quotes data for the stocks in self.__stock_tickers and uploads
         them into the DB"""
        # loading anag data
        for i in range(0, len(self.__stock_tickers)):
            ticker = self.__stock_tickers[i]
            url = 'https://finnhub.io/api/v1/stock/profile2?symbol=' + ticker + '&token=' + self.__token
            res = None
            while res is None:
                try:
                    res = urllib.request.urlopen(url)
                except urllib.error.HTTPError:
                    tm.sleep(1)
            self.__data['stock'][ticker]['anag'] = json.load(res)
            tm.sleep(0.5)
            sys.stdout.write('\r')
            sys.stdout.write('Loading DB with stock anagraphic data. Please wait... ' +
                             str(mt.trunc((i + 1) / len(self.__stock_tickers) * 100)) + '%')
        sys.stdout.write('\n')

        # loading price data
        for i in range(0, len(self.__stock_tickers)):
            ticker = self.__stock_tickers[i]
            res = None
            url = 'https://finnhub.io/api/v1/stock/candle?symbol=' + ticker + '&resolution=D&from=' + \
                  self.__s_date_unix + '&to=' + self.__e_date_unix + '&token=' + self.__token
            while res is None:
                try:
                    res = urllib.request.urlopen(url)
                except urllib.error.HTTPError:
                    tm.sleep(1)
            self.__data['stock'][ticker]['quotes'] = json.load(res)
            tm.sleep(0.5)
            sys.stdout.write('\r')
            sys.stdout.write('Loading DB with stock price data. Please wait... ' +
                             str(mt.trunc((i + 1) / len(self.__stock_tickers) * 100)) + '%')
        sys.stdout.write('\n')

        # Convert unix time stamps to dates
        for ticker in self.__stock_tickers:
            for i in range(0, len(self.__data['stock'][ticker]['quotes']['t'])):
                date = dt.datetime.utcfromtimestamp(self.__data['stock'][ticker]['quotes']['t'][i])
                self.__data['stock'][ticker]['quotes']['t'][i] = dt.datetime(date.year, date.month, date.day)

    def __load_fx_data(self) -> None:
        """"Gets from finnhub anagraphic data and quotes data for the fx rates in self.__fx_tickers and uploads
         them into the DB"""
        # loading anag data
        for i in range(0, len(self.__fx_tickers)):
            ticker = self.__fx_tickers[i]
            res = None
            url = 'https://finnhub.io/api/v1/forex/symbol?exchange=oanda&token=' + self.__token
            while res is None:
                try:
                    res = urllib.request.urlopen(url)
                except urllib.error.HTTPError:
                    tm.sleep(1)
            for j in json.load(res):
                if j['symbol'] == ticker:
                    self.__data['fx'][ticker]['anag'] = j
            tm.sleep(0.5)
            sys.stdout.write('\r')
            sys.stdout.write('Loading DB with forex anagraphic data. Please wait... ' +
                             str(mt.trunc((i + 1) / len(self.__fx_tickers) * 100)) + '%')
        sys.stdout.write('\n')

        # loading rates data
        for i in range(0, len(self.__fx_tickers)):
            ticker = self.__fx_tickers[i]
            res = None
            url = 'https://finnhub.io/api/v1/forex/candle?symbol=' + ticker + '&resolution=D&from=' + \
                  self.__s_date_unix + '&to=' + self.__e_date_unix + '&token=' + self.__token
            while res is None:
                try:
                    res = urllib.request.urlopen(url)
                except urllib.error.HTTPError:
                    tm.sleep(1)
            self.__data['fx'][ticker]['quotes'] = json.load(res)
            tm.sleep(0.5)
            sys.stdout.write('\r')
            sys.stdout.write('Loading DB with forex rates. Please wait... ' +
                             str(mt.trunc((i + 1) / len(self.__fx_tickers) * 100)) + '%')
        sys.stdout.write('\n')

        # Convert unix time stamps to dates
        for ticker in self.__fx_tickers:
            for i in range(0, len(self.__data['fx'][ticker]['quotes']['t'])):
                date = dt.datetime.utcfromtimestamp(self.__data['fx'][ticker]['quotes']['t'][i])
                self.__data['fx'][ticker]['quotes']['t'][i] = dt.datetime(date.year, date.month, date.day)

    def get_hist_close(self, ticker: str, flag: str, s_date: dt.datetime, e_date: dt.datetime) -> dict:
        """Retrieves the close prices or rates for the given ticker in the given time range"""
        if not (ticker in list(self.__data[flag].keys())):
            if flag == 'stock':
                msg = 'Error: ticker not included in the Database'
            else:
                msg = 'Error: currency not included in the Database'
            raise Exception(msg)
        if s_date > e_date:
            raise Exception('Error: start date cannot be greater than end date')
        if s_date > self.__data[flag][ticker]['quotes']['t'][-1]:
            raise Exception('Error: start date cannot be greater than max DB date: ' +
                            self.__data[flag][ticker]['quotes']['t'][-1].strftime('%Y/%m/%d'))
        if e_date < self.__data[flag][ticker]['quotes']['t'][0]:
            raise Exception('Error: end date cannot be less than min DB date: ' +
                            self.__data[flag][ticker]['quotes']['t'][0].strftime('%Y/%m/%d'))
        # Setting eIndex
        res_dic = {}
        if e_date >= self.__data[flag][ticker]['quotes']['t'][-1]:
            e_index = len(self.__data[flag][ticker]['quotes']['t']) - 1
        else:
            i = 0
            while self.__data[flag][ticker]['quotes']['t'][i] <= e_date:
                i = i + 1
            e_index = i - 1

        # Setting sIndex
        if s_date <= self.__data[flag][ticker]['quotes']['t'][0]:
            s_index = 0
        else:
            i = 0
            while self.__data[flag][ticker]['quotes']['t'][i] < s_date:
                i = i + 1
            s_index = i
        for i in range(s_index, e_index + 1):
            res_dic[self.__data[flag][ticker]['quotes']['t'][i]] = self.__data[flag][ticker]['quotes']['c'][i]
        return res_dic

    def get_max_date(self, ticker: str, flag: str) -> dt.datetime:
        if flag == 'stock':
            if not (ticker in list(self.__data[flag].keys())):
                raise Exception('Error: ticker not included in the Database')
            else:
                return self.__data[flag][ticker]['quotes']['t'][-1]
        else:
            if not ('OANDA:' + ticker + '_USD' in list(self.__data[flag].keys())):
                raise Exception('Error: currency not included in the Database')
            else:
                return self.__data[flag]['OANDA:' + ticker + '_USD']['quotes']['t'][-1]

    def get_min_date(self, ticker: str, flag: str):
        if flag == 'stock':
            if not (ticker in list(self.__data[flag].keys())):
                raise Exception('Error: ticker not included in the Database')
            else:
                return self.__data[flag][ticker]['quotes']['t'][0]
        else:
            if not ('OANDA:' + ticker + '_USD' in list(self.__data[flag].keys())):
                raise Exception('Error: currency not included in the Database')
            else:
                return self.__data[flag]['OANDA:' + ticker + '_USD']['quotes']['t'][0]
