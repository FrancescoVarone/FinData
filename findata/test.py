# The present script runs the main tests to assess the correct behaviour of the program
# ToDo:
#   - implement this kind of tests also for the other methods
#   - implement other parser tests to check if exceptions are raised also with other input conditions

import unittest
from cli import CLI
from data_handler import DataHandler
from method_handler import MethodHandler
import datetime as dt


class TestCase(unittest.TestCase):
    def test_parser(self):
        """Tests the correct behaviour of the parser method: an args string without a required input is
        passed to the method and the test checks if an exception is raised"""
        data_handler = DataHandler('')
        method_handler = MethodHandler(data_handler, '')
        cli_app = CLI(method_handler)
        args_exp = {'Ticker': {'Type': 'String', 'Required': 1}, 'StartDate': {'Type': 'Date', 'Required': 1},
                    'EndDate': {'Type': 'Date', 'Required': 1}, 'Currency': {'Type': 'String', 'Required': 1}}
        args_obtained = 'AAPL 2021/01/01 2021/02/14'
        with self.assertRaises(Exception):
            res = cli_app.parse_args(args_obtained, args_exp)

    def test_get_hist_prices(self):
        """Given a pre-defined set of inputs the test checks if the method correctly computes the results"""
        data_handler = DataHandler('')
        method_handler = MethodHandler(data_handler, '')
        data = {dt.datetime(2021, 1, 1): 120, dt.datetime(2021, 1, 2): 122, dt.datetime(2021, 1, 3): 123,
                dt.datetime(2021, 1, 4): 122, dt.datetime(2021, 1, 5): 119, dt.datetime(2021, 1, 8): 118,
                dt.datetime(2021, 1, 9): 120, dt.datetime(2021, 1, 10): 122}
        data_handler.load_db_manually('MSFT', data)
        res_test = {dt.datetime(2021, 1, 3): 123, dt.datetime(2021, 1, 4): 122, dt.datetime(2021, 1, 5): 119,
                    dt.datetime(2021, 1, 8): 118, dt.datetime(2021, 1, 9): 120}
        res = method_handler.get_hist_prices('MSFT', dt.datetime(2021, 1, 3), dt.datetime(2021, 1, 9), '')
        self.assertEqual(res, res_test)


if __name__ == '__main__':
    unittest.main()
