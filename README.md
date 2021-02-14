# Getting started
To get started just launch in python the file **'main.py'**.  
As soon as the program is launched, it will need to load the internal DB with stock and fx data.  
For what concerns stocks, the internal DB contains the anagraphic and quotes data of **1Y history** for the **100 largest stocks** in the **S&P 500 index**.  
For what concerns fx rates, the internal DB contains the anagraphic and quotes data of **1Y history** for the following fx rates: **AUD/USD**, **GBP/USD** and **EUR/USD**.  

# Commands
Once the DB are successfully loaded, you can start typing commands from the command line.  
To get the full list of available commands, just type `help`.  
To get help for the specific command, type `help <command>`.  

## get_stocks
**Description**: retrieves the list of available tickers in the DB  
**Sintax**: `get_stocks`  

## get_currencies
**Description**: retrieves the list of available fx rates in the DB  
**Sintax**: `get_stocks`

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
**Description**: plots the historical fx rates (vs USD) for a given currency. StartDate and EndDate are optional parameters.  
**Sintax**: `plot_hist_rates currency startDate endDate`. To get the whole rates history, just type: `plot_hist_rates currency`  
**Example**: `plot_hist_rates GBP 2020/12/01 2020/12/15`  
