"""
Server-side code for Anvil UI.
Handles HTTP requests
"""

import anvil.server
import requests, datetime

@anvil.server.callable
def getCurrPrice(stock):
  """
  Extract real-time market price for given stock ticker.
  Parses HTML code for Yahoo Finance website
  """
  url = 'https://query1.finance.yahoo.com/v8/finance/chart/{}?interval=1m'
  request = anvil.http.request(url.format(stock), json=True)
  return request['chart']['result'][0]['meta']['regularMarketPrice']
   
@anvil.server.callable
def getExpirationDates(stock):
  """
  Extract expiration dates for all avaliable options for a given stock
  """
  url = 'https://query2.finance.yahoo.com/v7/finance/options/{}'.format(stock)
  data = anvil.http.request(url, json=True)
  return data['optionChain']['result'][0]['expirationDates']

@anvil.server.callable
def getContracts(stock, expiration, optionType):
  """
  Returns an array of all contracts of a specified ticker with 
  a specific expirationDate (datetime.datetime object), of a specific
  type (call or put).
  """
  url = 'https://query2.finance.yahoo.com/v7/finance/options/{}?date={}'.format(stock, expiration)
  request = anvil.http.request(url, json=True)
  data = request['optionChain']['result']
  if not data:
      raise ValueError("Ticker/expiration combo does not exist")
  return data[0]['options'][0][optionType]  