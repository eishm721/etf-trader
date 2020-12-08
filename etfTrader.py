"""
FILENAME: etfTrader

Implements modified knapsack search algorithm to find optimium
portfolio distribution (in polynomial time) for trading ETF option contracts
using modified straddle-based strategy
"""

import collections
import scrapePrices as sp

SHARES_PER_CONTRACT = 100


CASH = 400000
ETFS = {
    'SPY': {
        1191: {
            'strikePrice': 363,
            'premium': 1.8
        },
        941: {
            'strikePrice': 181,
            'premium': 1.13
        },

    },
    'DIA': {
        83: {
            'strikePrice': 296,
            'premium': 1.77
        }
    },
    'QQQ': {
        9: {
            'strikePrice': 300,
            'premium': 2.15
        }  
    }
}


class ETFCalculator:
    def __init__(self, cash, etfs=('SPY', 'DIA', 'QQQ', 'IWM')):
        """
        Initialize with etfs to trade and avaliable cash
        """
        self.etfs = ETFS #sp.StockExtractor().extractPutData(etfs)
        print("ETF Data extracted. Finding your assignments...\n")
        self.cash = cash

        
        # finds lowest possible strike price out of all contracts
        self.cheapestStock = float('inf')
        self.numContracts = 0
        for etf in self.etfs:
            for expiration in self.etfs[etf]:
                self.cheapestStock = min(self.cheapestStock, self.etfs[etf][expiration]['strikePrice'])
                self.numContracts += 1

    def __calcOptimalAssignment(self, dp, contracts):
        """
        Given all possible contracts and filled DP table from value assignment,
        determines optimal assignment of contracts that created that value.
        """
        bag = []
        contractIdx = self.numContracts
        cashRemaining = self.cash // SHARES_PER_CONTRACT
        while contractIdx > 0 and cashRemaining > 0:
            curr = dp[contractIdx][cashRemaining]
            if curr != dp[contractIdx - 1][cashRemaining]:
                # current contract is included - add to bag and update remainingCash
                bag.append((contracts[contractIdx - 1]['stock'], contracts[contractIdx - 1]['expiration']))
                cashRemaining -= contracts[contractIdx - 1]['strikePrice']
            else:
                # current contract is excluded
                contractIdx -= 1
        
        return bag, cashRemaining * SHARES_PER_CONTRACT

    def assignStocksDP(self):
        """
        Implements modified 0/1 knapsack search algorithm for calculating maximum possible
        premium given all valid contracts. Builds dynamic programming table that is used to 
        determine optimal assignment in polynomial time (O(cash * numContracts))
        """
        capacity = self.cash // SHARES_PER_CONTRACT
        dp = [ [0 for _ in range(capacity + 1)] for _ in range(self.numContracts + 1)]
        
        contracts = []
        for cashLimit in range(capacity + 1):
            contractIdx = 1
            for stock in self.etfs:
                for expiration in self.etfs[stock]:
                    weight = self.etfs[stock][expiration]['strikePrice']
                    premium = self.etfs[stock][expiration]['premium']

                    # build up array of all contracts for calculating optimal assignments
                    if cashLimit == 0:
                        contracts.append({'stock': stock, 'expiration': expiration, 'strikePrice': weight})

                    dp[contractIdx][cashLimit] = dp[contractIdx - 1][cashLimit]
                    if weight <= cashLimit:
                        # either include or exclude the current contract, take one with max value
                        dp[contractIdx][cashLimit] = max(dp[contractIdx][cashLimit], dp[contractIdx][cashLimit - weight] + premium)
                    contractIdx += 1

        asssignmentValue = dp[-1][-1] * SHARES_PER_CONTRACT
        assignments, cashRemaining = self.__calcOptimalAssignment(dp, contracts)
        return asssignmentValue, assignments, cashRemaining
                    
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
            # precomputed value
            return cache[(value, moneyLeft)], assignment

        maxValue = 0
        bestAssignment = None
        
        # try assigning 1 more of each ETF to current assignment and recursively pick ETF w/ highest value
        for etf in self.etfs:
            for expiration in self.etfs[etf]:
                tempVal = value + self.etfs[etf][expiration]['premium']
                tempMoney = moneyLeft - self.etfs[etf][expiration]['strikePrice']
                currVal, currAssignment = self.__assignStocksRec(tempVal, tempMoney, assignment + [(etf, expiration)], cache)

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
    calc = ETFCalculator(cash=CASH)

    print(calc.assignStocksDP())
    print(calc.assignStocks()['Value ($x100)'])

    print()
    assignments = calc.assignStocks()
    for key in assignments:
        print(key+":", assignments[key])

if __name__ == '__main__':
    tests()