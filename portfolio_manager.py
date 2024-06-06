"""Class to manage portfolio creation and update."""
import pandas as pd
import numpy as np
from datetime import datetime as dt
import matplotlib.pyplot as plt

from market_data import MarketData
from gradient_ascent.mathematical_model import Model



class Manager:
    def __init__(self, model: Model, market_data: MarketData) -> None:
        self.model = model
        self.market_data = market_data


    def create_portfolio(self) -> None:
        ticker = 'BTCUSDT'
        (x_train, x_test) = self.get_data(ticker)
        theta, sharpes = self.create_model(x_train)
        self.validate_model(theta, sharpes, x_train, x_test)


    def get_data(self, ticker: str) -> tuple[np.array, np.array]:
        raw_data = self.market_data.get_klines(ticker, self.market_data.client.KLINE_INTERVAL_15MINUTE) # TODO: check data format
        coin = pd.DataFrame(
            data=[pd.to_numeric(row[1]) for row in raw_data],
            columns=['open_price']
        )
        coin.index = [dt.fromtimestamp(row[0] / 1000) for row in raw_data]
        x_train, x_test = self.model.train_test_split(coin['open_price'].diff()[1:])

        return (x_train, x_test)


    def create_model(self, x_train) -> tuple[list, list]:
        theta, sharpes = self.model.train(x_train, epochs=2000, M=8, commission=0.0025, learning_rate=0.3)

        return theta, sharpes


    def validate_model(self, theta: list, sharpes: list, x_train: list, x_test: list) -> None:
        plt.rcParams["figure.figsize"] = (5, 3)
        plt.rcParams["figure.dpi"] = 150

        plt.plot(sharpes)
        plt.xlabel('Epoch Number')
        plt.ylabel('Sharpe Ratio');

        train_returns = self.model.returns(self.model.positions(x_train, theta), x_train, 0.0025)
        plt.plot((train_returns).cumsum(), label="Reinforcement Learning Model", linewidth=1)
        plt.plot(x_train.cumsum(), label="Buy and Hold", linewidth=1)
        plt.xlabel('Ticks')
        plt.ylabel('Cumulative Returns');
        plt.legend()
        plt.title("RL Model vs. Buy and Hold - Training Data");

        test_returns = self.model.returns(self.model.positions(x_test, theta), x_test, 0.0025)
        plt.plot((test_returns).cumsum(), label="Reinforcement Learning Model", linewidth=1)
        plt.plot(x_test.cumsum(), label="Buy and Hold", linewidth=1)
        plt.xlabel('Ticks')
        plt.ylabel('Cumulative Returns');
        plt.legend()
        plt.title("RL Model vs. Buy and Hold - Test Data");