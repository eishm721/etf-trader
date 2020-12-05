# backtracking algorithm

import collections

SHARES_PER_CONTRACT = 100

CASH = 82000
ETFS = {
    'SPY': {
        'strikePrice': 363,
        'premium': 1.8
    },
    'IWM': {
        'strikePrice': 181,
        'premium': 1.13
    },
    'DIA': {
        'strikePrice': 296,
        'premium': 1.77
    },
    'QQQ': {
        'strikePrice': 300,
        'premium': 2.15
    }
}



def extractStockData(stocks):
    pass

class ETFCalculator:
    def __init__(self, etfs, cash):
        self.etfs = ETFS #extractStockData(etfs)
        self.cash = cash
        self.cheapestStock = min([self.etfs[etf]['strikePrice'] for etf in self.etfs])

    def __calcRemainingCash(self, assignment):
        balance = self.cash
        for etf in assignment:
            balance -= (self.etfs[etf]['strikePrice'] * SHARES_PER_CONTRACT)
        return balance

    def __assignStocksRec(self, value, moneyLeft, assignment, cache):
        if moneyLeft < 0:
            return moneyLeft, assignment
        if moneyLeft < self.cheapestStock:
            return value, assignment
        if (value, moneyLeft) in cache:
            return cache[(value, moneyLeft)], assignment
        maxValue = 0
        bestAssignment = None
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
        return {
            'Optimal Assignment': dict(collections.Counter(assignment)),
            'Value ($x100)': float(str(round(value * SHARES_PER_CONTRACT, 2))),
            'Cash Remaining ($)': cashRemaining
        }

    def assignStocks(self):
        if self.cash < self.cheapestStock:
            # cannot afford any stocks, exit early
            return self.__formatOutput([], 0, self.cash)
        assignmentValue, assignment = self.__assignStocksRec(0, self.cash // SHARES_PER_CONTRACT, [], {})
        return self.__formatOutput(assignment, assignmentValue, self.__calcRemainingCash(assignment))


calc = ETFCalculator([], CASH)
print(calc.assignStocks())
