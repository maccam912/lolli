import os

import pandas as pd
import tda
import typer
from backtesting import Backtest
from tda.auth import easy_client
from tda.client import Client

from lolli.strategy import SmaCross

app = typer.Typer()

token_path = os.path.join(os.getenv("HOME"), ".config", "tdtoken")


@app.command()
def login():
    tda.auth.client_from_manual_flow(
        api_key=os.getenv("TDA_API_KEY"),
        redirect_url="https://127.0.0.1:4000",
        token_path=token_path,
    )


@app.command()
def run(symbol: str):
    c = easy_client(
        api_key=os.getenv("TDA_API_KEY"),
        redirect_uri="https://127.0.0.1:4000",
        token_path=token_path,
    )
    hist = c.get_price_history(
        symbol,
        period_type=Client.PriceHistory.PeriodType.DAY,
        period=Client.PriceHistory.Period.FIVE_YEARS,
        frequency_type=Client.PriceHistory.FrequencyType.MINUTE,
        frequency=Client.PriceHistory.Frequency.EVERY_MINUTE,
    )
    pd_hist = pd.DataFrame(hist.json()["candles"])
    print(pd_hist)

    bt = Backtest(
        pd_hist, SmaCross, cash=10000, commission=0.002, exclusive_orders=True
    )
    output = bt.run()
    bt.plot()


def main():
    app()
