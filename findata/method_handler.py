# The present class represents an intermediate level between CLI and DataHandler.
# User's commands caught from CLI call methods of this class that in turn call data_handler methods.
# The methods of this class perform all the operations that by design cannot be done by CLI and DataHandler.
# For example, if the user asks to get the historical prices for a stock in a foreign currency,
#   all the operations needed to convert the data from the original currency are performed by a method of this class
#   (see 'get_hist_prices')


import datetime as dt
import utilities as ut
import urllib.request
import json
import data_handler as dh


class MethodHandler:
    def __init__(self, data_handler: dh.DataHandler, token: str):
        self.__dataHandler = data_handler
        self.__token = token

    def get_currencies(self) -> list:
        return self.__dataHandler.get_currencies()

    def get_stocks(self) -> list:
        return self.__dataHandler.get_stocks()

    def get_last_quotes(self, ticker: str, currency) -> dict:
        """Asks to finnhub for the requested data (stock and forex), performs currency conversion (if necessary) and
        returns the results to the calling method"""
        if currency != '':
            url_currency = 'https://finnhub.io/api/v1/forex/rates?base=USD&token=' + self.__token
            res_currency = json.load(urllib.request.urlopen(url_currency))
            if currency not in list(res_currency['quote'].keys()):
                raise Exception('Error: FX rate not available for the requested currency')
            fx_rate = res_currency['quote'][currency]
        else:
            fx_rate = 1
        url_stock = 'https://finnhub.io/api/v1/quote?symbol=' + ticker + '&token=' + self.__token
        res_stock = json.load(urllib.request.urlopen(url_stock))
        for key in list(res_stock.keys()):
            res_stock[key] = round(res_stock[key] * fx_rate, 2)
        return res_stock

    def plot_hist_quotes(self, ticker: str, s_date, e_date, flag: str) -> dict:
        """Set start_date and end_date if not provided, queries the DB through data_handler and returns the results
        to the calling method """
        if s_date == '':
            s_date = self.__dataHandler.get_min_date(ticker, flag)
        if e_date == '':
            e_date = self.__dataHandler.get_max_date(ticker, flag)
        if flag == 'stock':
            res = self.__dataHandler.get_hist_close(ticker, flag, s_date, e_date)
        else:
            res = self.__dataHandler.get_hist_close('OANDA:' + ticker + '_USD', flag, s_date, e_date)
        return res

    def get_hist_prices(self, ticker: str, s_date: dt.datetime, e_date: dt.datetime, currency: str) -> dict:
        """Queries the DB through data_handler, performs currency conversion when needed and returns the results
        to the calling method"""
        if currency == '':
            res = self.__dataHandler.get_hist_close(ticker, 'stock', s_date, e_date)
        else:
            res = {}
            stock_res = self.__dataHandler.get_hist_close(ticker, 'stock', s_date, e_date)
            curr_res = self.__dataHandler.get_hist_close('OANDA:' + currency + '_USD', 'fx', s_date, e_date)
            intersection = ut.intersection(list(stock_res.keys()), list(curr_res.keys()))
            for i in intersection:
                res[i] = round(stock_res[i] / curr_res[i], 2)
        return res
