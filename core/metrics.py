def calculate_metrics(portfolio) -> dict:
    stats = portfolio.stats()
    total_return = portfolio.total_return()
    sharpe_ratio = portfolio.sharpe_ratio()
    max_drawdown = portfolio.max_drawdown()
    win_rate = portfolio.trades.win_rate()
    expectancy = portfolio.trades.expectancy()
    exposure_time = stats.get("Exposure Time [%]", None)

    metrics = {
        "Total Return": round(total_return * 100, 2),
        "Sharpe Ratio": round(sharpe_ratio, 2),
        "Max Drawdown": round(max_drawdown * 100, 2),
        "Win Rate": round(win_rate * 100, 2),
        "Expectancy": round(expectancy, 2),
        "Exposure Time": round(exposure_time, 2) if exposure_time else None,
    }
    return metrics
