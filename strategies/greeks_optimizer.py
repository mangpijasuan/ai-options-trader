# strategies/greeks_optimizer.py

import pandas as pd

def filter_trades_by_greeks(df: pd.DataFrame,
                            delta_range=(0.3, 0.7),
                            max_gamma=0.2,
                            min_vega=0.1,
                            max_theta_decay=-0.05):
    """
    Filter options based on Greek profile:
    - delta between 0.3 and 0.7
    - gamma < max_gamma (to avoid explosive price sensitivity)
    - vega > min_vega (some volatility exposure)
    - theta > max_theta_decay (don't trade if time decay too steep)
    """

    filtered = df[
        df['delta'].between(delta_range[0], delta_range[1]) &
        (df['gamma'] < max_gamma) &
        (df['vega'] > min_vega) &
        (df['theta'] > max_theta_decay)
    ]

    return filtered.reset_index(drop=True)
