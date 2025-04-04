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

    def generate_signals(self) -> pd.DataFrame:
        """
        Generates trading signals for the SMA Crossover strategy.
        Buy when short SMA is above long SMA,
        and sell when short SMA is below long SMA.
        """
        short_sma = self.price_data["close"].rolling(window=self.short_window).mean()
        long_sma = self.price_data["close"].rolling(window=self.long_window).mean()

        buy_signal = short_sma > long_sma
        sell_signal = short_sma < long_sma

        signals = pd.DataFrame(0, index=self.price_data.index, columns=["signal"])
        signals.loc[buy_signal, "signal"] = 1
        signals.loc[sell_signal, "signal"] = -1

        return signals

    def run_backtest(self) -> pd.DataFrame:
        """
        Performs a backtest on the SMA Crossover strategy.
        Returns a DataFrame with the backtest results.
        """
        signals = self.generate_signals()

        portfolio = vbt.Portfolio.from_signals(
            self.price_data["close"],
            entries=signals["signal"] == 1,
            exits=signals["signal"] == -1,
            freq="1T",
            slippage=0.001,
            fees=0.001,
        )
        return portfolio.stats()

    def get_metrics(self) -> dict:
        """
        Calculates key strategy metrics.
        """
        portfolio_stats = self.run_backtest()
        metrics = {
            "total_return": portfolio_stats["total_return"],
            "sharpe_ratio": portfolio_stats["sharpe_ratio"],
            "max_drawdown": portfolio_stats["max_drawdown"],
            "winrate": portfolio_stats["winrate"],
        }
        return metrics
