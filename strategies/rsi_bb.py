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

    def __init__(
            self,
            price_data: pd.DataFrame,
            rsi_period=14,
            bb_window=20,
            bb_std=2
    ):
        super().__init__(price_data)
        self.rsi_period = rsi_period
        self.bb_window = bb_window
        self.bb_std = bb_std

    def generate_signals(self) -> pd.DataFrame:
        """
        Generate buy/sell signals based on RSI < 30 and BB bounce.
        """
        close = self.price_data["close"]
        rsi = RSIIndicator(close=close, window=self.rsi_period).rsi()

        bb = BollingerBands(
            close=close, window=self.bb_window, window_dev=self.bb_std
        )
        bb_lower = bb.bollinger_lband()
        bb_middle = bb.bollinger_mavg()
        rsi_condition = rsi < 30
        price_below_lband = close.shift(1) < bb_lower.shift(1)
        price_cross_up = close > bb_lower
        bb_bounce = price_below_lband & price_cross_up
        buy_signal = rsi_condition & bb_bounce
        sell_signal = (
                (close.shift(1) > bb_middle.shift(1)) &
                (close < bb_middle)
        )
        signals = pd.DataFrame(0, index=close.index, columns=["signal"])
        signals.loc[buy_signal, "signal"] = 1
        signals.loc[sell_signal, "signal"] = -1
        return signals

    def run_backtest(self) -> pd.DataFrame:
        """
        Run backtest using VectorBT.
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
        Return key metrics of the strategy.
        """
        portfolio_stats = self.run_backtest()
        metrics = {
            "total_return": portfolio_stats["total_return"],
            "sharpe_ratio": portfolio_stats["sharpe_ratio"],
            "max_drawdown": portfolio_stats["max_drawdown"],
            "winrate": portfolio_stats["winrate"],
        }
        return metrics
