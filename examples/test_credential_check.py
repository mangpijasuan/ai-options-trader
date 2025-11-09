#!/usr/bin/env python3
# examples/test_credential_check.py

"""
Test script to verify credential validation functionality in main.py.
"""

import os
import sys
import subprocess

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_alpaca_without_credentials():
    """Test that main.py provides helpful error when Alpaca credentials are missing."""
    print("\n📝 Testing Alpaca without credentials...")
    
    # Clear environment variables if they exist
    env = os.environ.copy()
    env.pop('ALPACA_API_KEY', None)
    env.pop('ALPACA_SECRET_KEY', None)
    
    # Run main.py with alpaca argument
    result = subprocess.run(
        [sys.executable, 'main.py', 'alpaca'],
        cwd=os.path.join(os.path.dirname(__file__), '..'),
        capture_output=True,
        text=True,
        timeout=5,
        env=env
    )
    
    # Should exit with non-zero status
    assert result.returncode != 0, "Should exit with error when credentials missing"
    
    # Should contain helpful error message
    assert 'credentials not configured' in result.stdout.lower(), \
        "Should show credentials not configured message"
    assert 'setup instructions' in result.stdout.lower(), \
        "Should show setup instructions"
    assert '.env' in result.stdout, \
        "Should mention .env file"
    assert 'alpaca.markets' in result.stdout.lower(), \
        "Should mention Alpaca website"
    
    print("✅ Alpaca without credentials shows helpful error message")


def test_alpaca_with_credentials():
    """Test that main.py proceeds when Alpaca credentials are provided."""
    print("\n📝 Testing Alpaca with credentials...")
    
    # Set test credentials
    env = os.environ.copy()
    env['ALPACA_API_KEY'] = 'test_key'
    env['ALPACA_SECRET_KEY'] = 'test_secret'
    
    # Run main.py with alpaca argument (will timeout or fail on connection, which is expected)
    result = subprocess.run(
        [sys.executable, 'main.py', 'alpaca'],
        cwd=os.path.join(os.path.dirname(__file__), '..'),
        capture_output=True,
        text=True,
        timeout=5,
        env=env
    )
    
    # Should NOT show credential configuration error
    assert 'credentials not configured' not in result.stdout.lower(), \
        "Should not show credentials error when credentials are provided"
    assert 'Starting AI Option Trader' in result.stdout, \
        "Should start the trader when credentials are provided"
    
    print("✅ Alpaca with credentials proceeds past validation")


def test_ibkr_no_credential_check():
    """Test that IBKR doesn't require credential validation."""
    print("\n📝 Testing IBKR (no credential check needed)...")
    
    # Run main.py with ibkr argument
    result = subprocess.run(
        [sys.executable, 'main.py', 'ibkr'],
        cwd=os.path.join(os.path.dirname(__file__), '..'),
        capture_output=True,
        text=True,
        timeout=5,
        env=os.environ.copy()
    )
    
    # Should NOT show credential configuration error
    assert 'credentials not configured' not in result.stdout.lower(), \
        "IBKR should not require credential validation"
    assert 'Starting AI Option Trader' in result.stdout, \
        "Should start the trader for IBKR"
    
    print("✅ IBKR proceeds without credential check")


def test_invalid_broker():
    """Test that invalid broker type shows appropriate error."""
    print("\n📝 Testing invalid broker type...")
    
    result = subprocess.run(
        [sys.executable, 'main.py', 'invalid_broker'],
        cwd=os.path.join(os.path.dirname(__file__), '..'),
        capture_output=True,
        text=True,
        timeout=5,
        env=os.environ.copy()
    )
    
    # Should exit with non-zero status
    assert result.returncode != 0, "Should exit with error for invalid broker"
    
    # Should contain error message about unsupported broker
    assert 'unsupported broker' in result.stdout.lower(), \
        "Should show unsupported broker message"
    
    print("✅ Invalid broker type shows appropriate error")


def main():
    print("🧪 Running Credential Check Tests")
    print("=" * 60)
    
    try:
        test_alpaca_without_credentials()
        test_alpaca_with_credentials()
        test_ibkr_no_credential_check()
        test_invalid_broker()
        
        print("\n" + "=" * 60)
        print("✅ All credential check tests passed!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except subprocess.TimeoutExpired as e:
        print(f"\n❌ Test timed out: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
