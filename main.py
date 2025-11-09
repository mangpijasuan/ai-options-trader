# main.py

import os
import sys
from execution.scheduler import run_scheduled_trading


def check_broker_credentials(broker_type):
    """
    Check if required credentials are configured for the specified broker.
    
    Args:
        broker_type: Type of broker ('ibkr' or 'alpaca')
        
    Returns:
        bool: True if credentials are configured, False otherwise
    """
    if broker_type == 'alpaca':
        api_key = os.getenv('ALPACA_API_KEY')
        secret_key = os.getenv('ALPACA_SECRET_KEY')
        
        if not api_key or not secret_key:
            return False
    
    # IBKR doesn't require API credentials (uses local TWS/Gateway connection)
    return True


def print_setup_instructions(broker_type):
    """
    Print setup instructions for the specified broker.
    
    Args:
        broker_type: Type of broker ('ibkr' or 'alpaca')
    """
    print(f"\n❌ {broker_type.upper()} credentials not configured!")
    print("\n📋 Setup Instructions:")
    print("=" * 60)
    
    if broker_type == 'alpaca':
        print("1. Create a .env file from the example:")
        print("   cp .env.example .env")
        print()
        print("2. Get your Alpaca API credentials:")
        print("   • Sign up at https://alpaca.markets/")
        print("   • Go to your dashboard and generate API keys")
        print("   • Use paper trading keys for testing")
        print()
        print("3. Edit .env and set your credentials:")
        print("   ALPACA_API_KEY=your_api_key_here")
        print("   ALPACA_SECRET_KEY=your_secret_key_here")
        print("   ALPACA_PAPER=true")
        print()
        print("For more details, see: BROKER_SETUP.md")
    
    print("=" * 60)


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
    
    # Check if broker credentials are configured
    if not check_broker_credentials(broker_type):
        print_setup_instructions(broker_type)
        sys.exit(1)
    
    print(f"🚀 Starting AI Option Trader with {broker_type.upper()} broker...")
    run_scheduled_trading(interval_sec=300, broker_type=broker_type)  # Every 5 minutes
