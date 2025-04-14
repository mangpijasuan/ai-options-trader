# utils/feature_engineering.py

import pandas as pd

def prepare_features(df: pd.DataFrame):
    df['underlying_return_1d'] = df['underlying_close'].pct_change(fill_method=None).fillna(0)

    # Example normalization or clipping if needed
    df['delta'] = df['delta'].clip(-1, 1)
    df['gamma'] = df['gamma'].clip(0, 1)
    df['vega'] = df['vega'].clip(0, 2)
    df['theta'] = df['theta'].clip(-1, 0)
    df['iv'] = df['iv'].fillna(df['iv'].mean())

    feature_cols = ['delta', 'gamma', 'vega', 'theta', 'iv', 'underlying_return_1d', 'volume']
    return df[feature_cols]
