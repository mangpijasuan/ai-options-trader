#!/usr/bin/env python3
# examples/test_broker_credentials.py

"""
Test script to verify broker credential validation.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from brokers import BrokerFactory


def test_alpaca_missing_credentials():
    """Test that missing Alpaca credentials raise appropriate error."""
    print("\n📝 Testing Alpaca with missing credentials...")
    
    try:
        broker = BrokerFactory.create_broker('alpaca')
        print("❌ Should have raised ValueError for missing credentials")
        return False
    except ValueError as e:
        error_msg = str(e)
        assert 'credentials required' in error_msg.lower()
        assert 'ALPACA_API_KEY' in error_msg
        assert 'ALPACA_SECRET_KEY' in error_msg
        print("✅ Correctly raises error for missing credentials")
        return True


def test_alpaca_placeholder_credentials():
    """Test that placeholder Alpaca credentials are detected and rejected."""
    print("\n📝 Testing Alpaca with placeholder credentials...")
    
    placeholder_patterns = [
        ('your_alpaca_api_key_here', 'your_alpaca_secret_key_here'),
        ('PLACEHOLDER_KEY', 'PLACEHOLDER_SECRET'),
        ('example_key', 'example_secret'),
        ('change_me_key', 'change_me_secret'),
    ]
    
    for api_key, secret_key in placeholder_patterns:
        try:
            broker = BrokerFactory.create_broker('alpaca', api_key=api_key, secret_key=secret_key)
            print(f"❌ Should have raised ValueError for placeholder: {api_key}")
            return False
        except ValueError as e:
            error_msg = str(e)
            assert 'invalid' in error_msg.lower() or 'placeholder' in error_msg.lower()
            assert 'alpaca.markets' in error_msg
    
    print("✅ Correctly detects and rejects placeholder credentials")
    return True


def test_alpaca_valid_format_credentials():
    """Test that valid-looking credentials are accepted."""
    print("\n📝 Testing Alpaca with valid-format credentials...")
    
    try:
        # Use realistic-looking fake credentials
        broker = BrokerFactory.create_broker(
            'alpaca',
            api_key='PKABCDEF123456789',
            secret_key='abc123def456ghi789jkl012mno345pqr678stu'
        )
        assert broker is not None
        assert broker.api_key == 'PKABCDEF123456789'
        print("✅ Accepts valid-format credentials")
        return True
    except Exception as e:
        print(f"❌ Should accept valid-format credentials: {e}")
        return False


def test_alpaca_empty_credentials():
    """Test that empty Alpaca credentials are rejected."""
    print("\n📝 Testing Alpaca with empty credentials...")
    
    try:
        broker = BrokerFactory.create_broker('alpaca', api_key='', secret_key='')
        print("❌ Should have raised ValueError for empty credentials")
        return False
    except ValueError as e:
        error_msg = str(e)
        assert 'credentials required' in error_msg.lower()
        print("✅ Correctly rejects empty credentials")
        return True


def test_ibkr_still_works():
    """Test that IBKR broker creation still works."""
    print("\n📝 Testing IBKR broker creation...")
    
    try:
        broker = BrokerFactory.create_broker('ibkr')
        assert broker is not None
        print("✅ IBKR broker creation still works")
        return True
    except Exception as e:
        print(f"❌ IBKR broker creation failed: {e}")
        return False


def main():
    print("🧪 Running Broker Credential Validation Tests")
    print("=" * 60)
    
    tests = [
        test_alpaca_missing_credentials,
        test_alpaca_placeholder_credentials,
        test_alpaca_valid_format_credentials,
        test_alpaca_empty_credentials,
        test_ibkr_still_works,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n❌ Test {test.__name__} failed with unexpected error: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"✅ All {total} tests passed!")
        print("=" * 60)
        return 0
    else:
        print(f"❌ {total - passed} out of {total} tests failed")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
