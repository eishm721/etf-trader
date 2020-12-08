"""
FILENAME: yahooFinanceScraper

Class for scraping stock and options data from Yahoo Finance API
Uses lxml to parse HTML for stock prices and scrapes YF API for options data
"""
from lxml import html
import requests, datetime


class YahooFinanceScraper:
    def __init__(self):
        """
        Initialize stock data class with Yahoo Finance stock URLs
        """
        self.price = 'https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch'
        self.options = 'https://query2.finance.yahoo.com/v7/finance/options/{}?date={}'
        self.allOptions = 'https://query2.finance.yahoo.com/v7/finance/options/{}'
    
    def getCurrPrice(self, stock):
        """
        Extract real-time market price for given stock ticker.
        Parses HTML code for Yahoo Finance website
        """
        page = requests.get(self.price.format(stock, stock))
        tree = html.fromstring(page.content)
        return float(tree.xpath('//span[@class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"]/text()')[0])

    def getExpirationDates(self, stock):
        """
        Extract expiration dates for all avaliable options for a given stock
        """
        data = requests.get('https://query2.finance.yahoo.com/v7/finance/options/{}'.format(stock)).json()
        return data['optionChain']['result'][0]['expirationDates']

    def __findStrikeIndex(self, contracts, strikePrice):
        """
        Given an array of contracts and a desired strike price,
        finds index of contract with that strike price using binary search.
        """
        start = 0
        end = len(contracts) - 1
        while start <= end:
            mid = (start + end) // 2
            midPrice = int(contracts[mid]['strike'])  # price of current contract
            if midPrice == strikePrice:
                return mid
            elif midPrice < strikePrice:
                start = mid + 1
            else:
                end = mid - 1
        return -1

    def getContracts(self, stock, expiration, optionType):
        """
        Returns an array of all contracts of a specified ticker with 
        a specific expirationDate (datetime.datetime object), of a specific
        type (call or put).
        """
        request = requests.get(self.options.format(stock, expiration)).json()
        data = request['optionChain']['result']
        if not data:
            raise ValueError("Invalid ticker")
        return data[0]['options'][0][optionType]  

    def __getOptionsPrice(self, stock, expiration, strike, optionType):
        """
        Takes a stock ticker, expiration date, strikePrice, type of option.
        Returns bid price
        """
        contracts = self.getContracts(stock, expiration, optionType)
        contract = contracts[self.__findStrikeIndex(contracts, strike)]
        return contract['bid']

    def getPutPrice(self, stock, expiration, strike):
        """
        Returns bid price of a PUT option for specific stock and specific expiration date
        """
        return self.__getOptionsPrice(stock, expiration, strike, 'puts')

    def getCallPrice(self, stock, expiration, strike):
        """
        Returns bid price of a CALL option for specific stock and specific expiration date
        """
        return self.__getOptionsPrice(stock, expiration, strike, 'calls')


def testScraper():
    print()
    s = YahooFinanceScraper()

    dec11th = 1607644800
    print(s.getPutPrice('SPY', dec11th, 369))


if __name__ == '__main__':
    testScraper()