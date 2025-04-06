import pandas as pd
import vectorbt as vbt
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from strategies.base import StrategyBase


class RSIBBStrategy(StrategyBase):
    """
    Strategy: RSI < 30 + Bollinger Bands bounce confirmation.
    Buy signal when RSI < 30 and price bounces from lower Bollinger Band.
    """

    def __init__(self, price_data: pd.DataFrame, rsi_period=14, bb_window=20, bb_std=2):
        super().__init__(price_data)
        self.rsi_period = rsi_period
        self.bb_window = bb_window
        self.bb_std = bb_std
        self.entries = None
        self.exits = None
        self.portfolio = None

    def generate_signals(self) -> pd.DataFrame:
        """
        Generate buy/sell signals based on RSI < 30 and BB bounce.
        """
        close = self.price_data["close"]
        rsi = RSIIndicator(close=close, window=self.rsi_period).rsi()

        bb = BollingerBands(close=close, window=self.bb_window, window_dev=self.bb_std)
        bb_lower = bb.bollinger_lband()
        bb_middle = bb.bollinger_mavg()

        rsi_condition = rsi < 30
        price_below_lband = close.shift(1) < bb_lower.shift(1)
        price_cross_up = close > bb_lower
        bb_bounce = price_below_lband & price_cross_up

        self.entries = (rsi_condition & bb_bounce).fillna(False)
        self.exits = (
            (close.shift(1) > bb_middle.shift(1)) & (close < bb_middle)
        ).fillna(False)

        return pd.DataFrame({"entries": self.entries, "exits": self.exits})

    def run_backtest(self) -> vbt.Portfolio:
        """
        Run backtest using VectorBT and return Portfolio object.
        """
        if self.entries is None or self.exits is None:
            self.generate_signals()

        close = self.price_data["close"]
        self.portfolio = vbt.Portfolio.from_signals(
            close=close,
            entries=self.entries,
            exits=self.exits,
            freq="1min",
            slippage=0.001,
            fees=0.001,
        )

        return self.portfolio

    def get_metrics(self) -> dict:
        """
        Return key metrics of the strategy using calculate_metrics.
        """
        if self.portfolio is None:
            self.run_backtest()

        from core.metrics import calculate_metrics

        return calculate_metrics(self.portfolio)
