"""
FILENAME: etfTrader

Implements modified backtracking algorithm to find optimium
portfolio distribution for trading ETF option contracts
using modified straddle-based strategy
"""

import collections
import scrapePrices as sp

SHARES_PER_CONTRACT = 100

class ETFCalculator:
    def __init__(self, cash, etfs=('SPY', 'DIA', 'QQQ', 'IWM')):
        """
        Initialize with etfs to trade and avaliable cash
        """
        self.etfs = sp.StockExtractor().extractPutData(etfs)
        self.cash = cash
        self.cheapestStock = min([self.etfs[etf]['strikePrice'] for etf in self.etfs])

    def __calcRemainingCash(self, assignment):
        """
        Calculates cash remaining after a particular assignment is taken 
        """
        balance = self.cash
        for etf in assignment:
            balance -= (self.etfs[etf]['strikePrice'] * SHARES_PER_CONTRACT)
        return balance

    def __assignStocksRec(self, value, moneyLeft, assignment, cache):
        """
        Modified backtracking algorithm wrapper that finds the optimal assignment of stocks
        Implements dynamic programming for efficiency
        """
        if moneyLeft < 0:
            # assignment is not valid
            return moneyLeft, assignment
        if moneyLeft < self.cheapestStock:
            # can't assign more stocks, return current value/premium
            return value, assignment
        if (value, moneyLeft) in cache:
            # precomputed calue
            return cache[(value, moneyLeft)], assignment

        maxValue = 0
        bestAssignment = None
        
        # try assigning each ETF to current assignment and recursively pick ETF w/ highest value
        for etf in self.etfs:
            tempVal = value + self.etfs[etf]['premium']
            tempMoney = moneyLeft - self.etfs[etf]['strikePrice']
            currVal, currAssignment = self.__assignStocksRec(tempVal, tempMoney, assignment + [etf], cache)

            if currVal > maxValue:
                maxValue = currVal
                bestAssignment = currAssignment

        cache[(value, moneyLeft)] = maxValue
        return maxValue, bestAssignment

    def __formatOutput(self, assignment, value, cashRemaining):
        """
        Formats all return values from backtracking in useable form 
        """
        return {
            'Put Options': self.etfs,
            'Optimal Assignment': dict(collections.Counter(assignment)),
            'Value ($x100)': float(str(round(value * SHARES_PER_CONTRACT, 2))),
            'Cash Remaining ($)': cashRemaining
        }

    def assignStocks(self):
        """
        Calculates optimal portfolio distribution given current cash and 
        current options trading prices
        """
        if self.cash < self.cheapestStock:
            # cannot afford any stocks, exit early
            return self.__formatOutput([], 0, self.cash)
        assignmentValue, assignment = self.__assignStocksRec(0, self.cash // SHARES_PER_CONTRACT, [], {})
        return self.__formatOutput(assignment, assignmentValue, self.__calcRemainingCash(assignment))


def tests():
    calc = ETFCalculator(cash=82000)
    print(calc.assignStocks())
