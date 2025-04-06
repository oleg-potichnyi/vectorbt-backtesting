import pandas as pd
from core.backtester import run_backtest_on_single_pair
from strategies.sma_cross import SMACrossover
from strategies.rsi_bb import RSIBBStrategy
from strategies.vwap_reversion import VWAPReversionStrategy


price_data = pd.read_parquet("data/btc_1m_feb25.parquet")

run_backtest_on_single_pair(
    strategy_class=SMACrossover,
    price_data=price_data,
    strategy_name="SMA_Cross"
)

run_backtest_on_single_pair(
    strategy_class=RSIBBStrategy, price_data=price_data, strategy_name="RSI_BB"
)

run_backtest_on_single_pair(
    strategy_class=VWAPReversionStrategy,
    price_data=price_data,
    strategy_name="VWAP_Reversion",
)
