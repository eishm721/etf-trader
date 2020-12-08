"""
FILENAME: scrapePrices

Implements class for finding options data for 
specified ETFs. To be used for running backtracking algorithm
"""
#upload 2 things to github, yahoo finance scraper + app

import datetime
from datetime import timezone
import yahooFinanceScraper

DAYS_IN_WEEK = 7
FRIDAY_INDEX = 4
STRIKE_RATIO = 0.985

class StockExtractor:
    def __init__(self):
        self.scraper = yahooFinanceScraper.YahooFinanceScraper()
   
    def __getNextFriday(self):
        """
        Helper function to get next friday in the current week.
        Used to pick option expiration dates
        """
        today = datetime.date.today()
        return today + datetime.timedelta((FRIDAY_INDEX-today.weekday()) % DAYS_IN_WEEK)

    def __getStrikePrice(self, stock):
        """
        Calculates strike price based on current stock price.
        strike = stock - (1.5% * stock)
        """
        currPrice = self.scraper.getCurrPrice(stock)
        return round(currPrice * STRIKE_RATIO)

    def extractPutData(self, stocks):
        """
        Takes an array of stocks and calculates strike price and premium for  
        a given expiration date
        """
        etfs = {}
        expirationDate = self.__getNextFriday()
        for stock in stocks:
            strikePrice = self.__getStrikePrice(stock)
            premium = self.scraper.getPutPrice(stock, expirationDate, strikePrice)
            etfs[stock] = {
                'strikePrice': strikePrice, 
                'premium': premium,
                'expiration': expirationDate.strftime("%m/%d/%Y")
            }
        return etfs

def testStockExtractor():
    s = StockExtractor()
    print(s.extractPutData(('SPY', 'DIA', 'QQQ', 'IWM')))



    

