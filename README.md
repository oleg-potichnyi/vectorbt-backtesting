# Trading Strategies Backtesting

This project implements a backtesting system for three trading strategies on 1-minute OHLCV data for 100 trading pairs against BTC from Binance, using the VectorBT framework. The system includes data loading, strategy interface implementation, backtesting, and result visualization.

## Features

* Data Loading & Caching: Downloads 1-minute OHLCV data for 100 BTC pairs from Binance for February 2025, caches it, and stores it in .parquet format with compression.
* Strategy Interface: A base interface for creating trading strategies with methods generate_signals(), run_backtest(), and get_metrics().
* Multiple Trading Strategies: Implements strategies such as SMA Crossover, RSI with Bollinger Band confirmation, and VWAP Reversion Intraday.
* Backtesting: Runs backtests using VectorBT, considering slippage, commission, and time drift.
* Result Generation: Saves performance metrics, equity curves, and strategy comparisons in .csv and .png files.

## Technology stack

* Python ≥ 3.10
* VectorBT: Framework for backtesting and analyzing trading strategies.
* Pandas: Data manipulation and analysis library, used for handling the OHLCV data.
* TA-Lib (ta): Technical analysis library for calculating indicators like RSI, SMA, and more.
* ccxt: Library for working with cryptocurrency exchanges, for future integration with live trading.
* unittest: Framework for running unit tests on the project’s key components.

## Installation

### 1. Clone the repository:
* git clone https://github.com/oleg-potichnyi/vectorbt-backtesting
* cd vectorbt_backtesting

### 2. Create a virtual environment and activate it:
* python -m venv venv
* source venv/bin/activate  # On Windows use venv\Scripts\activate


### 3. Install the required dependencies:
* pip install -r requirements.txt

## Usage

### Step1: Data Loading
* Run the data_loader.py script to download and process the historical 1-minute OHLCV data.

### Step2: Running the Backtests
#### Run the backtests by executing the main.py script. This will:
* Run the backtest for each strategy implemented in the strategies/ directory.
* Save the results such as metrics, equity curves, and performance heatmaps in the results/ folder.

## Running Tests

### To run the unit tests, execute: python -m unittest discover tests/
