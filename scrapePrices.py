from lxml import html
import requests

def getCurrPrice(stock):
    url = 'https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch'.format(stock, stock)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return float(tree.xpath('//span[@class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"]/text()')[0])

print(getCurrPrice('AAPL'))
