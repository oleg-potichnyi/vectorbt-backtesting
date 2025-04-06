import os
import pandas as pd
from core.metrics import calculate_metrics


def run_backtest_on_single_pair(
    strategy_class,
    price_data: pd.DataFrame,
    strategy_name: str,
    results_dir="results"
):
    os.makedirs(f"{results_dir}/screenshots", exist_ok=True)

    strategy = strategy_class(price_data)
    strategy.generate_signals()
    portfolio = strategy.run_backtest()

    metrics = calculate_metrics(portfolio)
    metrics["Strategy"] = strategy_name

    fig = portfolio.plot()
    fig.write_image(f"{results_dir}/screenshots/{strategy_name}_equity.png")

    metrics_df = pd.DataFrame([metrics])
    metrics_file = f"{results_dir}/metrics.csv"

    if os.path.exists(metrics_file):
        existing_df = pd.read_csv(metrics_file)
        if "Strategy" not in existing_df.columns:
            existing_df["Strategy"] = None
        updated_df = pd.concat([existing_df, metrics_df], ignore_index=True)
        updated_df.to_csv(metrics_file, index=False)
    else:
        metrics_df.to_csv(metrics_file, index=False)

    return metrics_df
