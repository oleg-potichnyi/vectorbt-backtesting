from abc import ABC, abstractmethod
import pandas as pd


class StrategyBase(ABC):
    """
    Abstract base class for all trading strategies.
    """

    def __init__(self, price_data: pd.DataFrame):
        """
        Initializing the strategy with input price data.
        """
        self.price_data = price_data
        self.signals = None
        self.results = None

    @abstractmethod
    def generate_signals(self) -> pd.DataFrame:
        """
        Generates trading signals based on price_data.
        """
        pass

    @abstractmethod
    def run_backtest(self) -> pd.DataFrame:
        """
        Performs backtesting based on signals.
        """
        pass

    @abstractmethod
    def get_metrics(self) -> dict:
        """
        Calculates and returns key performance metrics.
        """
        pass
