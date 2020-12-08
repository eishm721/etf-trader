"""
FILENAME: scrapePrices

Implements class for finding all possible options data for 
specified ETFs. To be used for running backtracking algorithm.
"""

import time, datetime, yahooFinanceScraper
from datetime import timezone

DAYS_IN_WEEK = 7
SECONDS_IN_WEEK = 604800
FRIDAY_INDEX = 4
STRIKE_RATIO = 0.985


class StockExtractor:
    def __init__(self, numWeeks=1):
        self.scraper = yahooFinanceScraper.YahooFinanceScraper()
        self.numWeeks = numWeeks  # number of weeks in the future to consider expirations
   
    def __getStrikePrice(self, stock):
        """
        Calculates strike price based on current stock price.
        strike = stock - (1.5% * stock)
        """
        currPrice = self.scraper.getCurrPrice(stock)
        return round(currPrice * STRIKE_RATIO)

    def __inRangeExpirations(self, stock):
        """
        Calculates all possible expiration dates for a option for
        a specific ticket within self.numWeeks from today 
        """
        possibleDates = self.scraper.getExpirationDates(stock)
        lastPossibleDate = time.time() + (SECONDS_IN_WEEK * self.numWeeks)
        return [date for date in possibleDates if date < lastPossibleDate ]

    def extractPutData(self, stocks):
        """
        Takes an array of stocks and calculates strike price and premium for all 
        valid expiration dates.
        Example output format:
        {
            'SPY': {
                1607644800: {
                    strikePrice: 369.02,
                    premium: 1.92
                }
            }
        }
        """
        etfs = {}
        for stock in stocks:
            validExpirations = self.__inRangeExpirations(stock)
            strikePrice = self.__getStrikePrice(stock)
            for expiration in validExpirations:
                premium = self.scraper.getPutPrice(stock, expiration, strikePrice)

                # convert expiration date to readable form
                expDt = datetime.datetime.utcfromtimestamp(expiration)
                utc_expiration = f"{expDt:%m-%d-%Y}"

                if stock not in etfs:
                    etfs[stock] = {}
                etfs[stock][utc_expiration] = { 'strikePrice': strikePrice, 'premium': premium }
        return etfs


def testStockExtractor():
    print()
    s = StockExtractor()
    print(s.extractPutData(('SPY', 'DIA', 'QQQ', 'IWM')))


if __name__ == '__main__':
    testStockExtractor()
    

