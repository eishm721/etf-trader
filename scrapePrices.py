"""
FILENAME: scrapePrices

Implements class for finding options data for 
specified ETFs. To be used for running backtracking algorithm
"""
#upload 2 things to github, yahoo finance scraper + app

import time, datetime
from datetime import timezone
import yahooFinanceScraper

DAYS_IN_WEEK = 7
FRIDAY_INDEX = 4
STRIKE_RATIO = 0.985
SECONDS_IN_WEEK = 604800


class StockExtractor:
    def __init__(self, numWeeks=1):
        self.scraper = yahooFinanceScraper.YahooFinanceScraper()
        self.numWeeks = numWeeks
   
    def __getStrikePrice(self, stock):
        """
        Calculates strike price based on current stock price.
        strike = stock - (1.5% * stock)
        """
        currPrice = self.scraper.getCurrPrice(stock)
        return round(currPrice * STRIKE_RATIO)

    def __inRangeExpirations(self, stock):
        possibleDates = self.scraper.getExpirationDates(stock)
        lastDate = time.time() + (SECONDS_IN_WEEK * self.numWeeks)
        return [date for date in possibleDates if date < int(lastDate) ]

    def extractPutData(self, stocks):
        """
        Takes an array of stocks and calculates strike price and premium for  
        a given expiration date
        """
        etfs = {}
        # expirationDate = getNextFriday()
        for stock in stocks:
            for expiration in self.__inRangeExpirations(stock):
                strikePrice = self.__getStrikePrice(stock)
                premium = self.scraper.getPutPrice(stock, expiration, strikePrice)

                # convert expiration date to readable form
                value = datetime.datetime.utcfromtimestamp(expiration)
                utc_time = f"{value:%m-%d-%Y}"

                if stock not in etfs:
                    etfs[stock] = {}
                etfs[stock][utc_time] = {
                    'strikePrice': strikePrice, 
                    'premium': premium,
                }

        return etfs

def testStockExtractor():
    print()
    s = StockExtractor()
    print(s.extractPutData(('SPY', 'DIA', 'QQQ', 'IWM')))


if __name__ == '__main__':
    testStockExtractor()
    

