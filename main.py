# main.py

from execution.scheduler import run_scheduled_trading

if __name__ == "__main__":
    print("🚀 Starting AI Option Trader...")
    run_scheduled_trading(interval_sec=300)  # Every 5 minutes
