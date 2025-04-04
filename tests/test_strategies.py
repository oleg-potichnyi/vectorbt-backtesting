import unittest
import pandas as pd
from strategies.sma_cross import SMACrossover
from strategies.rsi_bb import RSIBBStrategy
from strategies.vwap_reversion import VWAPReversionStrategy


class TestSMACrossover(unittest.TestCase):
    def setUp(self):
        date_range = pd.date_range(
            start="2025-02-01", end="2025-02-10", freq="T"
        )
        price_data = pd.DataFrame(
            {"close": [100 + i for i in range(len(date_range))]},
            index=date_range
        )

        self.price_data = price_data
        self.strategy = SMACrossover(self.price_data)

    def test_generate_signals(self):
        """Testing signal generation for the SMA crossover strategy."""
        signals = self.strategy.generate_signals()
        self.assertIn("signal", signals.columns)
        self.assertTrue(signals["signal"].isin([1, 0, -1]).all())
        self.assertEqual(signals.iloc[0]["signal"], 0)
        self.assertIn(signals.iloc[10]["signal"], [0, 1, -1])

    def test_run_backtest(self):
        """We are testing the launch of the strategy backtest."""
        result = self.strategy.run_backtest()

        self.assertIsInstance(result, pd.Series)
        required_metrics = [
            "Total Return [%]",
            "Benchmark Return [%]",
            "Max Drawdown [%]",
            "Omega Ratio",
            "Sortino Ratio",
        ]
        for metric in required_metrics:
            self.assertIn(metric, result.index)


class TestRSIBBStrategy(unittest.TestCase):
    def setUp(self):
        data = {
            "close": [
                100, 98, 96, 94, 92, 91, 90, 89, 88, 87, 86,
                85, 84, 83, 82, 81, 80, 81, 82, 83, 84
            ]
        }
        index = pd.date_range(
            start="2022-01-01",
            periods=len(data["close"]),
            freq="1T"
        )
        self.price_data = pd.DataFrame(data, index=index)

    def test_generate_signals_structure(self):
        strategy = RSIBBStrategy(price_data=self.price_data)
        signals = strategy.generate_signals()

        self.assertIsInstance(signals, pd.DataFrame)
        self.assertIn("signal", signals.columns)
        self.assertEqual(len(signals), len(self.price_data))


class TestVWAPReversionStrategy(unittest.TestCase):
    def setUp(self):
        self.data = {
            'close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [
                1000, 1200, 1100, 1150, 1180, 1200, 1300, 1250, 1270, 1300
            ]
        }
        self.price_data = pd.DataFrame(self.data)
        self.strategy = VWAPReversionStrategy(self.price_data, threshold=0.01)

    def test_generate_signals(self):
        signals = self.strategy.generate_signals()
        self.assertIsNotNone(signals)
        self.assertTrue('entry_long' in signals.columns)
        self.assertTrue('entry_short' in signals.columns)
        self.assertTrue('exit' in signals.columns)


if __name__ == "__main__":
    unittest.main()
