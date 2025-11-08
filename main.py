# main.py

"""
Main entry point for the AI Options Trader

This script starts the automated trading system that:
1. Connects to Interactive Brokers
2. Fetches live market data
3. Generates ML predictions
4. Executes trades based on configured rules
"""

import sys
import os
import argparse

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from execution.scheduler import run_scheduled_trading
import config

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='AI Options Trader')
    parser.add_argument(
        '--interval',
        type=int,
        default=config.TRADING_INTERVAL_SEC,
        help=f'Trading interval in seconds (default: {config.TRADING_INTERVAL_SEC})'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run in dry-run mode (no actual trades)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 AI Options Trader Starting...")
    print("=" * 60)
    print(f"📊 Configuration:")
    print(f"   Trading Interval: {args.interval} seconds")
    print(f"   Confidence Threshold: {config.CONFIDENCE_THRESHOLD:.0%}")
    print(f"   Symbols: {', '.join(config.TRADING_SYMBOLS)}")
    print(f"   IBKR Connection: {config.IBKR_HOST}:{config.IBKR_PORT}")
    print(f"   Dry Run: {args.dry_run}")
    print("=" * 60)
    
    if args.dry_run:
        print("\n⚠️  DRY RUN MODE - No actual trades will be placed")
    
    print("\n⚠️  DISCLAIMER:")
    print("   Options trading carries significant risk.")
    print("   Use at your own risk. Past performance does not guarantee future results.")
    print("   Make sure you're using a paper trading account for testing.")
    print("\n")
    
    try:
        run_scheduled_trading(interval_sec=args.interval)
    except KeyboardInterrupt:
        print("\n\n⏹️  Trading stopped by user")
        print("Goodbye! 👋")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
