# Use alpaca API
# Martingale strategy for S&P 500 ETFs (IVV, SPY)
# follow one direction until we get profit
import alpaca_trade_api as tradeapi

KEY = "PK57HCE2U6BW50JXOB2D"
SECRET = "Non7NRI0tvy1hhGDz0bnYsCXWUreba4Gtd3AWqwQ"

class TradingBot:
    def __init__(self, etf='SPY'):
        self.key = KEY
        self.secret = SECRET
        self.alpaca_endpoint = 'https://paper-api.alpaca.markets'
        self.api = tradeapi.REST(self.key, self.secret, self.alpaca_endpoint)
        self.symbol = etf
        self.current_order = None   # keeps track of open orders
        self.last_price = 1

        # limit bot to one open position - how many shares of etf we own
        try:
            self.position = int(self.api.get_position(self.symbol).qty)
        except:
            self.position = 0


class Martingale(TradingBot):
    """
    Double investment size on losing trades–expected long-term return is same
    Buying in dips when the price goes down and lowering your average entry price.
    Winning trades regain losses including initial trade amount.

    Pros: Recoup the losses & generate profits improving the net earnings
    Cons: Increasing the investment size without stop loss limits.
    """
    def submit_order(self, targetShares):
        if self.current_order is not None:
            self.api.cancel_order(self.current_order.id)

        delta = targetShares - self.position
        if delta == 0:
            return

        print("Processing the order for {} shares...".format(targetShares))

        if delta > 0:
            buy_quantity = delta
            if self.position < 0:
                buy_quantity = min(abs(self.position), buy_quantity)
            print("Buying {} shares...".format(buy_quantity))
            self.current_order = self.api.submit_order(self.symbol, buy_quantity, 'buy', 'limit', 'day', self.last_price)
        else:
            sell_quantity = abs(delta)
            if self.position > 0:
                sell_quantity = min(abs(self.position), sell_quantity)
            print("Selling {} shares...".format(sell_quantity))
            self.current_order = self.api.submit_order(self.symbol, sell_quantity, 'sell', 'limit', 'day', self.last_price)


if __name__ == '__main__':
    t = Martingale()
    t.submit_order(3)
