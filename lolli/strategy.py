import backtrader as bt
from backtrader.indicators.crossover import CrossDown, CrossUp


class TestStrategy(bt.Strategy):
    params = (
        ("maperiod", 13),
        ("printlog", False),
    )

    def log(self, txt, dt=None, doprint=False):
        """Logging function fot this strategy"""
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.started = False

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma1 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
        )

        self.sma2 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=(self.params.maperiod) * 2
        )

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm))

    def next(self):
        if not self.started:
            if self.sma1[0] > self.sma2[0]:
                self.buy()
            else:
                self.sell()
            self.buy()
            self.started = True
        if self.sma1[-1] <= self.sma2[-1] and self.sma1[0] > self.sma2[0]:
            self.buy(size=2)
        if self.sma1[-1] > self.sma2[-1] and self.sma1[0] <= self.sma2[0]:
            self.sell(size=2)

    def stop(self):
        self.close()

        self.log(
            "(MA Period %2d) Ending Value %.2f"
            % (self.params.maperiod, self.broker.getvalue()),
            doprint=True,
        )
