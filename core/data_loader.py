import ccxt
import pandas as pd
import time
from pathlib import Path
from datetime import datetime
from typing import Optional


root = Path(__file__).resolve().parent.parent
DATA_PATH = root / "data" / "btc_1m_feb25.parquet"

start_date = datetime(2025, 2, 1)
end_date = datetime(2025, 2, 28)

since = int(time.mktime(start_date.timetuple()) * 1000)
until = int(time.mktime(end_date.timetuple()) * 1000)
limit = 1000


def get_spot_pairs(quote_asset="BTC", top_n=100) -> list:
    """
    Returns a list of the most liquid spot trading pairs
    with the specified base currency (quote_asset).
    """
    exchange = ccxt.binance()
    markets = exchange.load_markets()
    return [
        symbol
        for symbol, info in markets.items()
        if symbol.endswith(f"/{quote_asset}") and info.get("spot", False)
    ][:top_n]


def fetch_data() -> Optional[pd.DataFrame]:
    """
    Loads 1-minute OHLCV data for top BTC pairs from Binance or from cache.
    Returns: A DataFrame with market data, or None if loading fails.
    """
    if DATA_PATH.exists():
        df = pd.read_parquet(DATA_PATH)
        if not df.isnull().values.any():
            return df

    exchange = ccxt.binance()
    all_data = []
    for pair in get_spot_pairs():
        ohlcv = exchange.fetch_ohlcv(pair, timeframe="1m", since=since, limit=limit)
        df = pd.DataFrame(
            ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        df["pair"] = pair
        all_data.append(df)

    if all_data:
        data = pd.concat(all_data, ignore_index=True)
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        data.to_parquet(DATA_PATH, compression="brotli")
        return data
    return None


data = fetch_data()
