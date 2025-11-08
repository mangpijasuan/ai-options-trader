# brokers/ibkr_data_fetcher.py

from ib_insync import *
import pandas as pd
import numpy as np
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def connect_ibkr():
    """Connect to IBKR with a different client ID than the trader"""
    ib = IB()
    try:
        # Use clientId + 1 to avoid conflicts with the trader connection
        ib.connect(config.IBKR_HOST, config.IBKR_PORT, clientId=config.IBKR_CLIENT_ID + 1)
        print("✅ Connected to IBKR for data fetching.")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        raise
    return ib

def fetch_live_option_data(symbols):
    ib = connect_ibkr()
    data = []

    for symbol in symbols:
        print(f"🔍 Fetching market data for {symbol}...")

        # Define underlying stock
        stock = Stock(symbol, 'SMART', 'USD')
        ib.qualifyContracts(stock)

        # Request market data
        ticker = ib.reqMktData(stock, "", False, False)
        ib.sleep(2)  # Give IBKR time to respond

        # Fallback in case ticker.last is None
        last_price = ticker.last if ticker.last is not None else ticker.close if ticker.close else 100.0

        # TEMP: mocked Greeks for now (to be replaced with live values later)
        row = {
            "symbol": symbol,
            "delta": round(np.random.uniform(0.3, 0.7), 2),
            "gamma": round(np.random.uniform(0.01, 0.15), 3),
            "vega": round(np.random.uniform(0.05, 0.25), 3),
            "theta": round(np.random.uniform(-0.1, -0.01), 3),
            "iv": round(np.random.uniform(0.2, 0.5), 3),
            "underlying_close": last_price,
            "volume": int(np.random.uniform(1000, 5000)),
            "direction": 0,  # Dummy for now, model ignores this in live
            "underlying_return_1d": 0  # Will be calculated inside feature_engineering
        }

        data.append(row)

        # Cancel the market data request to avoid resource lock
        ib.cancelMktData(ticker)

    ib.disconnect()

    df = pd.DataFrame(data)
    df.to_csv(config.LIVE_INPUT_PATH, index=False)
    print(f"✅ Live input updated: {config.LIVE_INPUT_PATH}")
