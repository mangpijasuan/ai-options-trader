import time
import pandas as pd
from models.predict import predict_from_live_data
from brokers.option_trader import connect_ibkr, place_option_trade
from brokers.ibkr_data_fetcher import fetch_live_option_data
from utils.helpers import get_next_friday
from strategies.greeks_optimizer import filter_trades_by_greeks

CONFIDENCE_THRESHOLD = 0.8
TRADE_QUANTITY = 1
EXPIRY = get_next_friday() # Static for now
STRIKE = 180         # Static for now

def run_scheduled_trading(interval_sec=300):
    ib = connect_ibkr()
    print("✅ Connected to IBKR. Starting live auto-trading loop...")

    while True:
        try:
            print("\n⏳ Fetching live data...")
            fetch_live_option_data(['AAPL', 'TSLA', 'MSFT', 'NVDA', 'SPY', 'QQQ'])  # Add more symbols as needed

            print("🔍 Reading data & generating predictions...")
            df = pd.read_csv("data/live_input.csv")
            predictions = predict_from_live_data(df)

            for pred in predictions:
                if pred['confidence'] >= CONFIDENCE_THRESHOLD:
                    print(f"✅ Placing trade for {pred['symbol']} — {pred['prediction']} (conf: {pred['confidence']:.2f})")
                    place_option_trade(
                        ib=ib,
                        symbol=pred['symbol'],
                        right='C' if pred['prediction'] == 'CALL' else 'P',
                        strike=STRIKE,
                        expiry=EXPIRY,
                        action='BUY',
                        quantity=TRADE_QUANTITY
                    )
                else:
                    print(f"⏭️ Skipped {pred['symbol']} — confidence too low: {pred['confidence']:.2f}")

        except Exception as e:
            print(f"❌ Error in loop: {e}")

        print(f"⏳ Sleeping {interval_sec} seconds...\n")
        time.sleep(interval_sec)
