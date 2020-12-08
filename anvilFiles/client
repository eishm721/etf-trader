"""
Back-end code for client side interactions in Anvil UI
"""
from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import collections
import time, datetime, collections
import anvil.http

DAYS_IN_WEEK = 7
SECONDS_IN_WEEK = 604800
FRIDAY_INDEX = 4
STRIKE_RATIO = 0.985
SHARES_PER_CONTRACT = 100

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
    return anvil.server.call('getCurrPrice', stock)
  
  def getExpirationDates(self, stock):
    """
    Extract expiration dates for all avaliable options for a given stock
    """
    return anvil.server.call('getExpirationDates', stock)

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
    return anvil.server.call('getContracts', stock, expiration, optionType)

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

      
class StockExtractor:
  def __init__(self, numWeeks):
    self.scraper = YahooFinanceScraper()
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

      
class ETFCalculator:
  def __init__(self, cash, etfs, weeks):
    """
    Initialize with etfs to trade and avaliable cash
    """
    self.etfs = StockExtractor(weeks).extractPutData(etfs)
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
      cashRemaining = int(self.cash // SHARES_PER_CONTRACT)
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

  def assignStocks(self):
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

    capacity = int(self.cash // SHARES_PER_CONTRACT)
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

      
class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
      
  def calcAssignments_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    # get assignments
    weeks = 1
    if self.weeksInFuture.text != "":
      weeks = int(self.weeksInFuture.text)
    calculator = ETFCalculator(float(self.cashInput.text), ('SPY', 'DIA', 'QQQ', 'IWM'), weeks)
    output = calculator.assignStocks()
    assignment = output['Optimal Assignment']
    
    # build array of all assignments
    res = []
    for contract in assignment:
      res.append(contract[0] + " " + contract[1] + ": " + str(assignment[contract]))
    
    # build array of all possible contracts
    possible = []
    for stock in calculator.etfs:
      for expiration in calculator.etfs[stock]:
        strike = calculator.etfs[stock][expiration]['strikePrice']
        premium = calculator.etfs[stock][expiration]['premium']
        possible.append("  ".join([stock, expiration, str(strike), str(premium)]))
        
    # format output
    self.numSPY.text = '\n'.join(res)
    self.totalValue.text = output['Value ($x100)']
    self.remainingCash.text = output['Cash Remaining ($)']
    self.possibleContracts.text = '\n'.join(possible)
        
    
      
    
  