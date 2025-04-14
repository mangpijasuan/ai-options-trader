# utils/generate_fake_data.py

import pandas as pd
import numpy as np
import random

def generate_fake_option_data(num_rows=1000):
    symbols = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'AMZN']
    data = []

    for _ in range(num_rows):
        symbol = random.choice(symbols)
        delta = round(np.clip(np.random.normal(0.5, 0.2), -1, 1), 2)
        gamma = round(np.random.uniform(0.01, 0.15), 3)
        vega = round(np.random.uniform(0.05, 0.3), 3)
        theta = round(np.random.uniform(-0.1, -0.01), 3)
        iv = round(np.random.uniform(0.15, 0.5), 3)
        close = round(np.random.uniform(100, 1000), 2)
        volume = int(np.random.uniform(500, 5000))
        direction = np.random.choice([0, 1], p=[0.45, 0.55])

        data.append([
            symbol, delta, gamma, vega, theta, iv, close, volume, direction
        ])

    df = pd.DataFrame(data, columns=[
        'symbol', 'delta', 'gamma', 'vega', 'theta',
        'iv', 'underlying_close', 'volume', 'direction'
    ])
    return df

if __name__ == "__main__":
    df = generate_fake_option_data(1000)
    df.to_csv('data/historical_data.csv', index=False)
    print("✅ Generated data/historical_data.csv with 1000 rows.")
