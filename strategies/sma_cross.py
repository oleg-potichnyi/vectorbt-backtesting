import pandas as pd
import vectorbt as vbt
from strategies.base import StrategyBase


class SMACrossover(StrategyBase):
    """
    Strategy of crossing two moving averages (SMA).
    """

    def __init__(self, price_data: pd.DataFrame, short_window=50, long_window=200):
        """
        Initializing the strategy with input data.
        """
        super().__init__(price_data)
        self.short_window = short_window
        self.long_window = long_window
        self.entries = None
        self.exits = None
        self.portfolio = None

    def generate_signals(self) -> pd.DataFrame:
        """
        Generate buy/sell signals.
        """
        close = self.price_data['close']
        short_sma = close.rolling(window=self.short_window).mean()
        long_sma = close.rolling(window=self.long_window).mean()

        self.entries = (short_sma > long_sma).fillna(False)
        self.exits = (short_sma < long_sma).fillna(False)

        return pd.DataFrame({'entries': self.entries, 'exits': self.exits})

    def run_backtest(self) -> vbt.Portfolio:
        """
        Run backtest using VectorBT.
        """

        if self.entries is None or self.exits is None:
            self.generate_signals()

        close = self.price_data['close']
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
        Return calculated metrics using core.metrics.
        """
        if self.portfolio is None:
            self.run_backtest()

        from core.metrics import calculate_metrics
        return calculate_metrics(self.portfolio)

