# main.py

import os
import sys
from dotenv import load_dotenv
from execution.scheduler import run_scheduled_trading

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    # Get broker type from environment variable or command line argument
    broker_type = os.getenv('BROKER_TYPE', 'ibkr').lower()
    
    # Allow command line override: python main.py alpaca
    if len(sys.argv) > 1:
        broker_type = sys.argv[1].lower()
    
    if broker_type not in ['ibkr', 'alpaca']:
        print(f"❌ Unsupported broker: {broker_type}")
        print("Supported brokers: ibkr, alpaca")
        sys.exit(1)
    
    print(f"🚀 Starting AI Option Trader with {broker_type.upper()} broker...")
    run_scheduled_trading(interval_sec=300, broker_type=broker_type)  # Every 5 minutes
