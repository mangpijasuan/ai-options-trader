# brokers/data_fetcher.py

import pandas as pd
import numpy as np
from typing import List
from .base_broker import BaseBroker


def fetch_live_option_data(broker: BaseBroker, symbols: List[str]) -> None:
    """
    Fetch live market data for given symbols using the provided broker.
    
    Args:
        broker: Broker instance implementing BaseBroker interface
        symbols: List of stock symbols to fetch data for
    """
    if not broker.is_connected():
        broker.connect()
    
    data = []
    
    for symbol in symbols:
        print(f"🔍 Fetching market data for {symbol}...")
        
        try:
            market_data = broker.fetch_market_data(symbol)
            last_price = market_data.get('last_price', 100.0)
            
            # TEMP: mocked Greeks for now (to be replaced with live values later)
            row = {
                "symbol": symbol,
                "delta": round(np.random.uniform(0.3, 0.7), 2),
                "gamma": round(np.random.uniform(0.01, 0.15), 3),
                "vega": round(np.random.uniform(0.05, 0.25), 3),
                "theta": round(np.random.uniform(-0.1, -0.01), 3),
                "iv": round(np.random.uniform(0.2, 0.5), 3),
                "underlying_close": last_price if last_price else 100.0,
                "volume": int(np.random.uniform(1000, 5000)),
                "direction": 0,  # Dummy for now, model ignores this in live
                "underlying_return_1d": 0  # Will be calculated inside feature_engineering
            }
            
            data.append(row)
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {e}")
            continue
    
    df = pd.DataFrame(data)
    df.to_csv('data/live_input.csv', index=False)
    print("✅ Live input updated: data/live_input.csv")
