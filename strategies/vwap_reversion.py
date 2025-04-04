import pandas as pd
import vectorbt as vbt
from strategies.base import StrategyBase


class VWAPReversionStrategy(StrategyBase):
    """
    VWAP Reversion Intraday Strategy.
    """

    def __init__(self, price_data: pd.DataFrame, threshold: float = 0.01):
        super().__init__(price_data)
        self.threshold = threshold
        self.vwap = None

    def generate_signals(self) -> pd.DataFrame:
        """
        Signal generation: long entry when there is a significant drop
        below VWAP, short entry when there is a rise above VWAP.
        """
        close = self.price_data["close"]
        high = self.price_data["high"]
        low = self.price_data["low"]
        volume = self.price_data["volume"]
        typical_price = (high + low + close) / 3
        cum_vwap = (typical_price * volume).cumsum() / volume.cumsum()
        self.vwap = cum_vwap

        vwap_diff = (close - cum_vwap) / cum_vwap

        entries_long = vwap_diff < -self.threshold
        entries_short = vwap_diff > self.threshold
        exits = vwap_diff.abs() < 0.001

        self.signals = pd.DataFrame(
            {"entry_long": entries_long,
             "entry_short": entries_short,
             "exit": exits}
        )
        return self.signals

    def run_backtest(self) -> pd.DataFrame:
        """
        Running a backtest via vectorbt.
        """
        if self.signals is None:
            self.generate_signals()
        close = self.price_data["close"]
        entries = self.signals["entry_long"]
        short_entries = self.signals["entry_short"]
        exits = self.signals["exit"]
        pf = vbt.Portfolio.from_signals(
            close,
            entries=entries,
            short_entries=short_entries,
            exits=exits,
            short_exits=exits,
            fees=0.001,
            slippage=0.001,
        )

        self.results = pf
        return pf.stats()

    def get_metrics(self) -> dict:
        """
        Obtaining key backtest metrics.
        """
        if self.results is None:
            self.run_backtest()
        stats = self.results.stats()
        metrics = {
            "Total Return": stats["Total Return [%]"],
            "Sharpe Ratio": stats["Sharpe Ratio"],
            "Max Drawdown": stats["Max Drawdown [%]"],
            "Win Rate": stats["Win Rate [%]"],
            "Expectancy": stats["Expectancy"],
            "Exposure Time": stats["Exposure Time [%]"],
        }
        return metrics
