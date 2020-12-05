from lxml import html
import requests

etfPriceURLs = {
    'SPY': 'https://finance.yahoo.com/quote/SPY?p=SPY&.tsrc=fin-srch',
    'QQQ': 'https://finance.yahoo.com/quote/QQQ?p=QQQ&.tsrc=fin-srch',
    'IWM': 'https://finance.yahoo.com/quote/IWM?p=IWM&.tsrc=fin-srch',
    'DIA': 'https://finance.yahoo.com/quote/DIA?p=DIA&.tsrc=fin-srch'
}

def getCurrPrice(stock):
    if stock not in etfPriceURLs:
        return None
    page = requests.get(etfPriceURLs[stock])
    tree = html.fromstring(page.content)
    return float(tree.xpath('//span[@class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"]/text()')[0])




#print(getCurrPrice('SPY'))
