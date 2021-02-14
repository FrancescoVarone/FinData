import cmd
import sys
import MethodHandler as mh
import datetime as dt
import plotille as plt


class CLI(cmd.Cmd):

    def __init__(self, methodHandler: mh.MethodHandler):
        cmd.Cmd.__init__(self)
        self.prompt = '>>> '
        self.intro = 'DB loaded successfully! You have at you disposal 1Y history data for the ' \
                     'largest 100 stocks of the S&P 500 index' + '\n' + \
                     "Type your command or write 'help' to see all available commands"
        self.__methodHandler = methodHandler

    def help_get_last_quotes(self):
        sys.stdout.write('\n' + "Retrieves the last quotes (close/open/high/low) for the given ticker. Currency"
                                " is an optional parameter" + '\n')
        sys.stdout.write("Syntax is: 'get_last_quotes ticker currency'" + '\n')
        sys.stdout.write("Example: 'get_last_quotes AAPL GBP'" + '\n\n')

    def help_plot_hist_rates(self):
        sys.stdout.write('\n' + "Plots the historical rates for a given currency. StartDate and EndDate are optional"
                                " parameters. Data refers to OANDA exchange" + '\n')
        sys.stdout.write("Syntax is: 'plot_hist_rates currency startDate endDate'" + '\n')
        sys.stdout.write("To get the whole rates history, just type: 'plot_hist_rates currency'" + '\n')
        sys.stdout.write("Example: 'plot_hist_rates AUD 2020/12/01 2020/12/15'" + '\n\n')

    def help_plot_hist_prices(self):
        sys.stdout.write('\n' + "Plots the historical prices for a given ticker. StartDate and EndDate are optional"
                                " parameters" + '\n')
        sys.stdout.write("Syntax is: 'plot_hist_prices ticker startDate endDate'" + '\n')
        sys.stdout.write("To get the whole prices history, just type: 'plot_hist_prices ticker'" + '\n')
        sys.stdout.write("Example: 'plot_hist_prices AAPL 2020/12/01 2020/12/15'" + '\n\n')

    def help_get_hist_prices(self):
        sys.stdout.write('\n' + "Gets the historical prices for a given ticker in a given time range. Currency is "
                         "an optional parameter." + '\n')
        sys.stdout.write("Syntax is: 'get_hist_prices ticker startDate endDate currency'" + '\n')
        sys.stdout.write("Example: 'get_hist_prices AAPL 2020/12/01 2020/12/15 GBP'" + '\n\n')

    def help_quit(self):
        sys.stdout.write('\n' + "Print 'quit' to exit the program" + '\n\n')

    def do_get_last_quotes(self, args):
        try:
            exp_args = {'Ticker': {'Type': 'String', 'Required': 1}, 'Currency': {'Type': 'String', 'Required': 0}}
            args = self.parse_args(args, exp_args)
            res = self.__methodHandler.get_last_quotes(args['Ticker'], args['Currency'])
            sys.stdout.write('Close: ' + str(res['c']) + '\n')
            sys.stdout.write('High: ' + str(res['h']) + '\n')
            sys.stdout.write('Low: ' + str(res['l']) + '\n')
            sys.stdout.write('Open: ' + str(res['o']) + '\n\n')
        except Exception as e:
            sys.stdout.write(str(e) + '\n\n')


    def do_plot_hist_rates(self, args: str) -> None:
        try:
            exp_args = {'Ticker': {'Type': 'String', 'Required': 1}, 'StartDate': {'Type': 'Date', 'Required': 0},
                        'EndDate': {'Type': 'Date', 'Required': 0}}
            args = self.parse_args(args, exp_args)
            res = self.__methodHandler.plot_hist_quotes(args['Ticker'], args['StartDate'], args['EndDate'], 'fx')
            if len(res.keys()) >= 2:
                fig = plt.Figure()
                fig.x_label = 'Time'
                fig.y_label = 'Rates'
                fig.width = 120
                fig.height = 30
                fig.set_x_limits(min_=list(res.keys())[0], max_=list(res.keys())[-1])
                fig.set_y_limits(min_=0.8 * min(list(res.values())), max_=1.1 * max(list(res.values())))
                fig.plot(res.keys(), res.values())
                sys.stdout.write('\n' + fig.show(legend=False) + '\n\n\n')
            else:
                sys.stdout.write('Error: Graph requires at least 2 values to be showed' + '\n\n')
        except Exception as e:
            sys.stdout.write(str(e) + '\n\n')

    def do_plot_hist_prices(self, args: str) -> None:
        try:
            exp_args = {'Ticker': {'Type': 'String', 'Required': 1}, 'StartDate': {'Type': 'Date', 'Required': 0},
                        'EndDate': {'Type': 'Date', 'Required': 0}}
            args = self.parse_args(args, exp_args)
            res = self.__methodHandler.plot_hist_quotes(args['Ticker'], args['StartDate'], args['EndDate'], 'stock')
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
                sys.stdout.write('Error: Graph requires at least 2 values to be showed' + '\n\n')
        except Exception as e:
            sys.stdout.write(str(e) + '\n\n')

    def do_get_hist_prices(self, args: str) -> None:
        try:
            exp_args = {'Ticker': {'Type': 'String', 'Required': 1}, 'StartDate': {'Type': 'Date', 'Required': 1},
                        'EndDate': {'Type': 'Date', 'Required': 1}, 'Currency': {'Type': 'String', 'Required': 0}}
            args = self.parse_args(args, exp_args)
            res = self.__methodHandler.get_hist_prices(args['Ticker'], args['StartDate'], args['EndDate'],
                                                       args['Currency'])
            for i in res.keys():
                sys.stdout.write(dt.datetime.strftime(i, '%m/%d/%Y') + ' ' + str(res[i]) + '\n')
            sys.stdout.write('\n')
        except Exception as e:
            sys.stdout.write(str(e) + '\n\n')

    def do_quit(self, args):
        sys.exit(1)

    def parse_args(self, args_obtained: str, args_exp: dict) -> dict:  # argsExp is {argName:{type: xxx, req: xxx}, ...}
        args_obtained = args_obtained.split()  # list of args obtained
        args_dic = {}  # dict that will be returned by the function {argName: value}
        args_names = list(args_exp.keys())  # names of the expected args

        for i in range(0, len(args_obtained)):
            if i+1 > len(list(args_exp.keys())):
                raise Exception('Too many arguments')
            args_dic[args_names[i]] = args_obtained[i]

        for name in args_names:
            if (args_exp[name]['Required'] == 1) and (not (name in list(args_dic.keys()))):
                raise Exception('Error: ' + name + ' is a required parameter')
            if (args_exp[name]['Type'] == 'Date') and (name in list(args_dic.keys())):
                try:
                    args_dic[name] = dt.datetime.strptime(args_dic[name], '%Y/%m/%d')
                except:
                    raise Exception('Error: please enter a valid date for ' + name + '. Right format is: yyyy/mm/dd')
            if not name in list(args_dic.keys()):
                args_dic[name] = ''
        return args_dic
