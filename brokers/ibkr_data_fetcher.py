# brokers/ibkr_data_fetcher.py

from ib_insync import *
import pandas as pd
import numpy as np

def connect_ibkr():
    ib = IB()
    try:
        ib.connect('127.0.0.1', 7497, clientId=2)
        print("✅ Connected to IBKR.")
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
    df.to_csv('data/live_input.csv', index=False)
    print("✅ Live input updated: data/live_input.csv")
