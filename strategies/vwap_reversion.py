import pandas as pd
import vectorbt as vbt
from strategies.base import StrategyBase


class VWAPReversionStrategy(StrategyBase):
    """
    VWAP Reversion Intraday Strategy.
    """

    def __init__(self, price_data: pd.DataFrame, threshold: float = 0.01):
        """
        Ініціалізація стратегії з вхідними даними.
        """
        super().__init__(price_data)
        self.threshold = threshold
        self.vwap = None
        self.entries_long = None
        self.entries_short = None
        self.exits = None
        self.portfolio = None

    def generate_signals(self) -> pd.DataFrame:
        """
        Генерація сигналів: довга позиція, коли ціна значно падає
        нижче VWAP, коротка позиція, коли ціна піднімається вище VWAP.
        """
        close = self.price_data["close"]
        high = self.price_data["high"]
        low = self.price_data["low"]
        volume = self.price_data["volume"]
        typical_price = (high + low + close) / 3
        cum_vwap = (typical_price * volume).cumsum() / volume.cumsum()
        self.vwap = cum_vwap

        vwap_diff = (close - cum_vwap) / cum_vwap

        self.entries_long = vwap_diff < -self.threshold
        self.entries_short = vwap_diff > self.threshold
        self.exits = vwap_diff.abs() < 0.001

        return pd.DataFrame(
            {
                "entries_long": self.entries_long,
                "entries_short": self.entries_short,
                "exits": self.exits,
            }
        )

    def run_backtest(self) -> vbt.Portfolio:
        """
        Запуск бектесту через VectorBT.
        """
        if (
            self.entries_long is None
            or self.entries_short is None
            or self.exits is None
        ):
            self.generate_signals()

        close = self.price_data["close"]
        self.portfolio = vbt.Portfolio.from_signals(
            close,
            entries=self.entries_long,
            short_entries=self.entries_short,
            exits=self.exits,
            short_exits=self.exits,
            slippage=0.001,
            fees=0.001,
            freq="1min",  # <-- Set the frequency here (adjust accordingly)
        )
        return self.portfolio

    def get_metrics(self) -> dict:
        """
        Отримання ключових метрик бектесту.
        """
        if self.portfolio is None:
            self.run_backtest()

        from core.metrics import calculate_metrics

        return calculate_metrics(self.portfolio)
