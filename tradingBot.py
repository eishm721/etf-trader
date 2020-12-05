

# alpaca API
# Martingale strategy for S&P ETFs (IVV, SPY,
# follow one direction until we get profit

import alpaca_trade_api as tradeapi

class Martingale:
    def __init__(self, etf):
        self.key = ## key
        self.secret = ## secret
        self.alpaca_endpoint = 'https://paper-api.alpaca.markets'
        self.api = tradeapi.RESTT(self.key, self.secret, self.alpaca_endpoint)
        self.symbol = etf
        self.current_order = None   # keeps track of open orders
        self.last_price = 1

        # limit bot to one open position
        try:
            self.position = int(self.api.get_position(self.symbol).qty)
        except:
            self.position = 0

    def submit_order(self, target):
        if self.current_order is not None:
            self.api.cancel_order(self.current_order.id)

        delta = target - self.position
        if delta == 0:
            return

        print("Processing the order for {} shares".format(target)...)

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
    t = Martingale('SPY')
    t.submit_order(3)
