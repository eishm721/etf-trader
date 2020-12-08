"""
FILENAME: etfTrader

Implements modified knapsack search algorithm to find optimium
portfolio distribution (in polynomial time) for trading ETF option contracts
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
        print("ETF Data extracted. Finding your assignments...\n")
        self.cash = cash

        # finds lowest possible strike price out of all contracts
        self.cheapestStock = float('inf')
        self.numContracts = 0

        self.contracts = []
        for etf in self.etfs:
            for expiration in self.etfs[etf]:
                self.cheapestStock = min(self.cheapestStock, self.etfs[etf][expiration]['strikePrice'])
                self.numContracts += 1
                
    def __calcOptimalAssignment(self, dp, contracts):
        """
        Given all possible contracts and filled DP table from value assignment,
        determines optimal assignment of contracts that created that value.
        Also determined cash remaining after purchasing all contracts.
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

    def assignStocksDP(self):
        """
        Calculates optimal portfolio distribution given current cash and 
        current options trading prices.

        Implements modified 0/1 knapsack search algorithm for calculating maximum possible
        premium given all valid contracts. Builds dynamic programming table that is used to 
        determine optimal assignment in polynomial time (O(cash * numContracts))
        """
        # cannot afford any stocks, exit early
        if self.cash < self.cheapestStock:
            return self.__formatOutput([], 0, self.cash)

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

        assignment, cashRemaining = self.__calcOptimalAssignment(dp, contracts)
        return self.__formatOutput(assignment, dp[-1][-1], cashRemaining)


def tests():
    calc = ETFCalculator(cash=76000)
    print()
    assignments = calc.assignStocksDP()
    for key in assignments:
        print(key+":", assignments[key])


if __name__ == '__main__':
    tests()