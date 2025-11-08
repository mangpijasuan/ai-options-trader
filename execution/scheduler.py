import time
import pandas as pd
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.predict import predict_from_live_data
from brokers.option_trader import connect_ibkr, place_option_trade
from brokers.ibkr_data_fetcher import fetch_live_option_data
from utils.helpers import get_next_friday
from strategies.greeks_optimizer import filter_trades_by_greeks
import config

def run_scheduled_trading(interval_sec=None):
    """
    Run the automated trading loop
    
    Args:
        interval_sec: Trading interval in seconds (defaults to config value)
    """
    if interval_sec is None:
        interval_sec = config.TRADING_INTERVAL_SEC
    
    try:
        ib = connect_ibkr()
        print("✅ Connected to IBKR. Starting live auto-trading loop...")
    except Exception as e:
        print(f"❌ Failed to connect to IBKR: {e}")
        print("Please ensure TWS or IB Gateway is running and API access is enabled.")
        return

    while True:
        try:
            print("\n⏳ Fetching live data...")
            fetch_live_option_data(config.TRADING_SYMBOLS)

            print("🔍 Reading data & generating predictions...")
            df = pd.read_csv(config.LIVE_INPUT_PATH)
            predictions = predict_from_live_data(df)

            for pred in predictions:
                if pred['confidence'] >= config.CONFIDENCE_THRESHOLD:
                    # Use static strike if configured, otherwise would need to calculate ATM
                    strike = config.STATIC_STRIKE if config.STATIC_STRIKE else 180
                    expiry = get_next_friday()
                    
                    print(f"✅ Placing trade for {pred['symbol']} — {pred['prediction']} (conf: {pred['confidence']:.2f})")
                    place_option_trade(
                        ib=ib,
                        symbol=pred['symbol'],
                        right='C' if pred['prediction'] == 'CALL' else 'P',
                        strike=strike,
                        expiry=expiry,
                        action='BUY',
                        quantity=config.TRADE_QUANTITY
                    )
                else:
                    print(f"⏭️ Skipped {pred['symbol']} — confidence too low: {pred['confidence']:.2f}")

        except KeyboardInterrupt:
            print("\n⏹️ Stopping trading loop...")
            ib.disconnect()
            break
        except Exception as e:
            print(f"❌ Error in loop: {e}")
            import traceback
            traceback.print_exc()

        print(f"⏳ Sleeping {interval_sec} seconds...\n")
        time.sleep(interval_sec)
