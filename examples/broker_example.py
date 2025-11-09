#!/usr/bin/env python3
# examples/broker_example.py

"""
Example script demonstrating how to use the broker abstraction layer.
This shows how to switch between IBKR and Alpaca brokers.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from brokers import BrokerFactory


def demo_ibkr_broker():
    """
    Demonstrate IBKR broker usage.
    Note: Requires TWS/Gateway to be running.
    """
    print("\n" + "="*60)
    print("IBKR Broker Demo")
    print("="*60)
    
    try:
        # Create IBKR broker
        broker = BrokerFactory.create_broker('ibkr')
        print(f"✅ Created broker: {type(broker).__name__}")
        
        # Note: Actual connection will fail without TWS/Gateway running
        # broker.connect()
        # broker.disconnect()
        
        print("📝 IBKR broker ready (connection not tested - requires TWS/Gateway)")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_alpaca_broker():
    """
    Demonstrate Alpaca broker usage.
    Note: Requires valid API credentials.
    """
    print("\n" + "="*60)
    print("Alpaca Broker Demo")
    print("="*60)
    
    try:
        # Check if credentials are available
        api_key = os.getenv('ALPACA_API_KEY')
        secret_key = os.getenv('ALPACA_SECRET_KEY')
        
        if not api_key or not secret_key:
            print("⚠️ Alpaca credentials not found in environment")
            print("Set ALPACA_API_KEY and ALPACA_SECRET_KEY to test Alpaca broker")
            return
        
        # Create Alpaca broker
        broker = BrokerFactory.create_broker('alpaca')
        print(f"✅ Created broker: {type(broker).__name__}")
        
        # Note: Actual connection will be tested
        # broker.connect()
        # broker.disconnect()
        
        print("📝 Alpaca broker ready (connection not tested)")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_factory():
    """
    Demonstrate broker factory usage.
    """
    print("\n" + "="*60)
    print("Broker Factory Demo")
    print("="*60)
    
    # Show available broker types
    print("\n📋 Available broker types: ibkr, alpaca")
    
    # Create brokers
    for broker_type in ['ibkr', 'alpaca']:
        try:
            if broker_type == 'alpaca':
                # Skip if no credentials
                if not os.getenv('ALPACA_API_KEY'):
                    print(f"⏭️ Skipping {broker_type} - no credentials")
                    continue
            
            broker = BrokerFactory.create_broker(broker_type)
            print(f"✅ {broker_type.upper()}: {type(broker).__name__}")
        except Exception as e:
            print(f"❌ {broker_type.upper()}: {e}")


def main():
    print("🚀 Broker Abstraction Layer Demo")
    print("This script demonstrates the multi-broker support")
    
    demo_factory()
    demo_ibkr_broker()
    demo_alpaca_broker()
    
    print("\n" + "="*60)
    print("✅ Demo completed!")
    print("="*60)
    print("\n📖 For more information, see BROKER_SETUP.md")


if __name__ == "__main__":
    main()
