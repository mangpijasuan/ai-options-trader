import time
import sys
import pandas as pd
from models.predict import predict_from_live_data
from brokers.broker_factory import BrokerFactory
from brokers.data_fetcher import fetch_live_option_data
from utils.helpers import get_next_friday
from strategies.greeks_optimizer import filter_trades_by_greeks

CONFIDENCE_THRESHOLD = 0.8
TRADE_QUANTITY = 1
EXPIRY = get_next_friday() # Static for now
STRIKE = 180         # Static for now

def run_scheduled_trading(interval_sec=300, broker_type='ibkr'):
    """
    Run the scheduled trading loop.
    
    Args:
        interval_sec: Interval between trading cycles in seconds
        broker_type: Type of broker to use ('ibkr' or 'alpaca')
    """
    broker = BrokerFactory.create_broker(broker_type)
    
    # Attempt to connect to broker with proper error handling
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(1, max_retries + 1):
        try:
            broker.connect()
            print(f"✅ Connected to {broker_type.upper()}. Starting live auto-trading loop...")
            break
        except Exception as e:
            if attempt < max_retries:
                print(f"⚠️  Connection attempt {attempt}/{max_retries} failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"\n❌ Failed to connect to {broker_type.upper()} after {max_retries} attempts.")
                print("\n📋 Troubleshooting steps:")
                if broker_type == 'ibkr':
                    print("   1. Ensure TWS (Trader Workstation) or IB Gateway is running")
                    print("   2. Check that API connections are enabled in TWS/Gateway settings:")
                    print("      - File → Global Configuration → API → Settings")
                    print("      - Enable 'Enable ActiveX and Socket Clients'")
                    print("      - Verify the socket port matches your configuration (default: 7497)")
                    print("   3. Verify your .env file has correct IBKR_HOST and IBKR_PORT settings")
                    print("   4. Make sure no firewall is blocking the connection")
                elif broker_type == 'alpaca':
                    print("   1. Verify your API keys are correct in the .env file")
                    print("   2. Check that you have an active internet connection")
                    print("   3. Ensure you're using the correct environment (paper vs live)")
                print(f"\nOriginal error: {e}")
                sys.exit(1)

    while True:
        try:
            print("\n⏳ Fetching live data...")
            fetch_live_option_data(broker, ['AAPL', 'TSLA', 'MSFT', 'NVDA', 'SPY', 'QQQ'])  # Add more symbols as needed

            print("🔍 Reading data & generating predictions...")
            df = pd.read_csv("data/live_input.csv")
            predictions = predict_from_live_data(df)

            for pred in predictions:
                if pred['confidence'] >= CONFIDENCE_THRESHOLD:
                    print(f"✅ Placing trade for {pred['symbol']} — {pred['prediction']} (conf: {pred['confidence']:.2f})")
                    broker.place_option_trade(
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
