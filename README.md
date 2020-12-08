# ETFTrader

This is a python bot to trade SPY/DIA/QQQ/IWM ETF contracts using straddle-based options strategy. I have developed a knapsack-based search algorithm to optimize portfolio distribution & automate trades w/ HTTP requests. Additionally, I have built a custom web-scraper to fetch live stock prices/indicators by parsing HTML code and interfacing with Yahoo Finance public API. So far, we have seen an annualized 14% return, nearly double the performance of the S&P 500 on historical data. Minimum investment must be ~$20,000 for trading ETF options.

Framework is developed in Python. Initial steps were designing a custom Yahoo Finance web-scraper due to limitations in free, real-time stock data (lxml, HTTP). Next, I developed a knapsack-based search algorithm for determining optimal porfolio allocation based on option contract details (strike price, premium, expiration) and various indicators (implied volatility, delta, theta). I built a simple UI for visualizing this algorithm using Anvil python client (both server/client side). Lastly, we interfaced the Alpaca API for placing paper trades.


### Features:
- Custom web-scraper to extract real-time stock data
  - current stock price
  - option premiums/expirations
- Knapsack algorithm for determining optimal portfolio allocation
  - considers contract strike price, premium, expiration, IV, delta, theta decay
- Simple UI (built w/ python client for Anvil) for visualizing allocation algorithm: https://etf-auto.anvil.app

### Usage

    python3 etfTrader.py [tickers,] cash
    
    - tickers: space separated list of all stock tickers
    - avaliable cash in account
   
    ex: python3 etfTrade.py SPY QQQ DIA IWM 94500
    
      
### Libraries Used:
- lxml - HTML web-scraper for real-time stock prices
- requests - HTTP requests on APIs
- Yahoo Finance API - scraping options data
- Alpaca API - placing paper trades
- Anvil - building simple UI for portfolio
- time/datetime - custom timer for determing option contract expiration dates
- NumPy/SciPy - mathematical analysis with large data sets, building classification models

    
### Most Recent Changes (12/08/20):
- Improved portfolio allocation algorithm runtime from O(2^n) to O(n^2) using dynamic program

