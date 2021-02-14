import datetime as dt
import Utilities as ut
import urllib.request
import json
import DataHandler as Dh


class MethodHandler:
    def __init__(self, data_handler: Dh.DataHandler, token: str):
        self.__dataHandler = data_handler
        self.__token = token

    def get_currencies(self) -> list:
        return self.__dataHandler.get_currencies()

    def get_stocks(self) -> list:
        return self.__dataHandler.get_stocks()

    def get_last_quotes(self, ticker: str, currency) -> dict:
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
