import unittest
import os
import pandas as pd
from unittest.mock import MagicMock
from core.backtester import run_backtest_on_single_pair


class TestBacktester(unittest.TestCase):
    def setUp(self):
        """Preparing mock data for price_data."""
        self.price_data = pd.DataFrame(
            {
                "date": pd.date_range("2020-01-01", periods=5, freq="D"),
                "close": [100, 102, 101, 103, 104],
            }
        )
        self.price_data.set_index("date", inplace=True)
        self.mock_strategy_class = MagicMock()
        self.mock_strategy_class.return_value.generate_signals = MagicMock()
        self.mock_strategy_class.return_value.run_backtest = MagicMock()
        self.mock_strategy_class.return_value.run_backtest.return_value.plot. \
            return_value = MagicMock()

    def test_run_backtest_on_single_pair(self):
        """We test whether the function works correctly with mock data."""
        result_df = run_backtest_on_single_pair(
            self.mock_strategy_class, self.price_data, "TestStrategy"
        )
        self.assertTrue(isinstance(result_df, pd.DataFrame))
        self.mock_strategy_class.return_value.run_backtest.assert_called_once()

    def test_metrics_csv_creation(self):
        """Check whether the metrics.csv file is created."""
        metrics_file = "results/metrics.csv"
        if os.path.exists(metrics_file):
            os.remove(metrics_file)
        run_backtest_on_single_pair(
            self.mock_strategy_class, self.price_data, "TestStrategy"
        )
        self.assertTrue(os.path.exists(metrics_file))


if __name__ == "__main__":
    unittest.main()
