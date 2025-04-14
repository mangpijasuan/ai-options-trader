# backtest/metrics.py

import numpy as np

def compute_metrics(returns: list[float]):
    returns = np.array(returns)
    avg_return = np.mean(returns)
    std_return = np.std(returns)
    sharpe = (avg_return / std_return) * np.sqrt(252) if std_return > 0 else 0

    cumulative = np.cumprod(1 + returns)
    peak = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - peak) / peak
    max_drawdown = np.min(drawdown)

    win_rate = np.sum(returns > 0) / len(returns)

    return {
        'Sharpe Ratio': round(sharpe, 3),
        'Max Drawdown': round(max_drawdown, 3),
        'Win Rate': round(win_rate, 3)
    }
