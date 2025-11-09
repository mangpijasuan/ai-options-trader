#!/usr/bin/env python3
# examples/test_brokers.py

"""
Simple test script to verify broker implementations.
This performs basic checks without requiring actual broker connections.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from brokers import BaseBroker, IBKRBroker, AlpacaBroker, BrokerFactory


def test_base_broker_interface():
    """Test that BaseBroker defines the correct interface."""
    print("\n📝 Testing BaseBroker interface...")
    
    required_methods = [
        'connect',
        'disconnect', 
        'is_connected',
        'place_option_trade',
        'fetch_market_data',
        'get_account_info'
    ]
    
    for method in required_methods:
        assert hasattr(BaseBroker, method), f"BaseBroker missing method: {method}"
    
    print("✅ BaseBroker interface is complete")


def test_ibkr_broker():
    """Test IBKR broker instantiation."""
    print("\n📝 Testing IBKRBroker...")
    
    # Test default instantiation
    broker = IBKRBroker()
    assert broker.host == '127.0.0.1'
    assert broker.port == 7497
    assert broker.client_id == 1
    print("✅ IBKRBroker instantiation with defaults")
    
    # Test custom parameters
    broker = IBKRBroker(host='192.168.1.1', port=4002, client_id=5)
    assert broker.host == '192.168.1.1'
    assert broker.port == 4002
    assert broker.client_id == 5
    print("✅ IBKRBroker instantiation with custom parameters")
    
    # Test interface compliance
    assert isinstance(broker, BaseBroker)
    print("✅ IBKRBroker implements BaseBroker interface")


def test_alpaca_broker():
    """Test Alpaca broker instantiation."""
    print("\n📝 Testing AlpacaBroker...")
    
    # Test instantiation
    broker = AlpacaBroker(api_key='test_key', secret_key='test_secret', paper=True)
    assert broker.api_key == 'test_key'
    assert broker.secret_key == 'test_secret'
    assert broker.paper == True
    print("✅ AlpacaBroker instantiation")
    
    # Test interface compliance
    assert isinstance(broker, BaseBroker)
    print("✅ AlpacaBroker implements BaseBroker interface")


def test_broker_factory():
    """Test broker factory."""
    print("\n📝 Testing BrokerFactory...")
    
    # Test IBKR creation
    broker = BrokerFactory.create_broker('ibkr')
    assert isinstance(broker, IBKRBroker)
    print("✅ BrokerFactory creates IBKRBroker")
    
    # Test Alpaca creation (with credentials)
    broker = BrokerFactory.create_broker('alpaca', api_key='test', secret_key='test')
    assert isinstance(broker, AlpacaBroker)
    print("✅ BrokerFactory creates AlpacaBroker")
    
    # Test invalid broker type
    try:
        broker = BrokerFactory.create_broker('invalid')
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert 'Unsupported broker type' in str(e)
        print("✅ BrokerFactory raises error for invalid type")


def test_broker_methods_exist():
    """Test that all broker methods exist."""
    print("\n📝 Testing broker methods exist...")
    
    brokers = [
        IBKRBroker(),
        AlpacaBroker(api_key='test', secret_key='test')
    ]
    
    required_methods = [
        'connect',
        'disconnect',
        'is_connected',
        'place_option_trade',
        'fetch_market_data',
        'get_account_info'
    ]
    
    for broker in brokers:
        broker_name = type(broker).__name__
        for method in required_methods:
            assert hasattr(broker, method), f"{broker_name} missing method: {method}"
            assert callable(getattr(broker, method)), f"{broker_name}.{method} is not callable"
        print(f"✅ {broker_name} has all required methods")


def main():
    print("🧪 Running Broker Tests")
    print("=" * 60)
    
    try:
        test_base_broker_interface()
        test_ibkr_broker()
        test_alpaca_broker()
        test_broker_factory()
        test_broker_methods_exist()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
