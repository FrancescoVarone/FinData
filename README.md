# Getting started
To get started just launch in python the file **'main.py'**.  
As soon as the program is launched, it will need to load the internal DB with stock and fx data.  
The DB loadng can take a few minutes to complete depending on your connection.  
For what concerns stocks, the internal DB contains the anagraphic and quotes data of **1Y history** for the **100 largest stocks** in the **S&P 500 index**.  
For what concerns fx rates, the internal DB contains the anagraphic and quotes data of **1Y history** for the following fx rates: **AUD/USD**, **GBP/USD** and **EUR/USD**.  

# Commands
Once the DB is successfully loaded, you can start typing commands from the command line.  
To get the full list of available commands, just type `help`.  
To get help for the specific command, type `help <command>`.  

## get_stocks
**Description**: retrieves the list of available tickers in the DB  
**Sintax**: `get_stocks`  

## get_currencies
**Description**: retrieves the list of available fx rates in the DB  
**Sintax**: `get_currencies`

## get_last_quotes
**Description**: retrieves the last quotes (close/open/high/low) for the given ticker. Currency is an optional parameter.  
**Sintax**: `get_last_quotes ticker currency`  
**Example**: `get_last_quotes AAPL AUD`  

## get_hist_prices
**Description**: retrieves the historical prices for a given ticker in a given time range. Currency is an optional parameter  
**Sintax**: `get_hist_prices ticker startDate endDate currency`  
**Example**: `get_hist_prices AAPL 2020/12/01 2020/12/15 GBP`

## plot_hist_prices
**Description**: plots the historical prices for a given ticker. StartDate and EndDate are optional parameters.  
**Sintax**: `plot_hist_prices ticker startDate endDate`. To get the whole prices history, just type: `plot_hist_prices ticker`  
**Example**: `plot_hist_prices AAPL 2020/12/01 2020/12/15`  

## plot_hist_rates
**Description**: plots the historical fx rates (vs USD) for a given currency (from OANDA exchange). StartDate and EndDate are optional parameters.  
**Sintax**: `plot_hist_rates currency startDate endDate`. To get the whole rates history, just type: `plot_hist_rates currency`  
**Example**: `plot_hist_rates GBP 2020/12/01 2020/12/15`  

# Technical notes
The program relies on three main classes to work: **CLI**, **MethodHandler** and **DataHandler**.  
The main.py creates an instance of these three classes and runs the cmd loop that constantly catchs the user's commands. 

## CLI
CLI is the Command Line Interface class which inherits from the built-in Cmd class.  
The duties of this class are:
  - to catch user's commands (by inheriting from Cmd class)  
  - to identify the inputs contained in the command string (by using the parse_args method)  
  - to run the appropriate method associated with the user's command (by calling method_handler methods)  
  - to print the results of the command (by using stdout or plotille module)  
  
## MethodHandler
The MethodHandler class represents an **intermediate level** between CLI and DataHandler.  
User's commands caught from CLI call methods of this class that in turn call data_handler methods.  
The methods of this class perform all the operations that by design cannot be done by CLI and DataHandler.  
For example, if the user asks to get the historical prices for a stock in a foreign currency, all the operations needed to convert the data from the original currency are performed by a method of this class (see 'get_hist_prices')

## DataHandler
The DataHandler class **contains** the **DB** of the program and the methods to **query** the DB.  
The DB is the attribute 'data' of this class. As a private attribute it can be modified only by the methods of this class. This avoids other parts of the code to harm the integrity of the data.  

The attribute 'data' is a dict and it is organised in the following manner:
  - the first key level is used to separate stock data from fx data. Keys are: 'stock' and 'fx'
  - the second key level refers to the tickers (a stock or fx ticker). Keys are: ticker1, ticker2, ...
  - the third key level is used to separate angraphic data from quotes data. Keys are: 'anag', 'quotes'
  - the fourth key level is the one inherited from finnhub. For exmple, for stock and fx rates quotes we have: 'c', 'h', 'l', 'o', 't'...

The duties of the class are:  
  - to load data from finnhub (by using 'load_db' method)  
  - to perform simple queries to get the data (mainly by using 'get_hist_close' method)  
