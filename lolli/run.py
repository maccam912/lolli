from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
from datetime import datetime
from pathlib import Path

import backtrader as bt
import typer

from lolli.strategy import TestStrategy

app = typer.Typer()


def datafile(path: str, fromdate: datetime, todate: datetime):
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, path)

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath, fromdate=fromdate, todate=todate, reverse=False
    )

    return data


@app.command()
def run(
    path: Path,
    fromdate: datetime = typer.Argument(None, formats=["%Y-%m-%d"]),
    todate: datetime = typer.Argument(None, formats=["%Y-%m-%d"]),
):
    cerebro = bt.Cerebro()

    # Add a strategy
    # strats = cerebro.optstrategy(TestStrategy, maperiod=range(10, 31))
    cerebro.addstrategy(TestStrategy)

    # Add the Data Feed to Cerebro
    cerebro.adddata(datafile(path, fromdate, todate))

    # Set our desired cash start
    cerebro.broker.setcash(1000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set the commission
    cerebro.broker.setcommission(commission=0.0)

    # Run over everything
    cerebro.run(maxcpus=1)

    cerebro.plot()


def main():
    app()
