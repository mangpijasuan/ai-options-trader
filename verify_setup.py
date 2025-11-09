#!/usr/bin/env python3
"""
Setup Verification Script
Run this to verify your multi-broker implementation is working correctly.
"""

import sys
import os

def check_imports():
    """Verify all broker modules can be imported."""
    print("🔍 Checking imports...")
    try:
        from brokers import BaseBroker, IBKRBroker, AlpacaBroker, BrokerFactory
        from brokers.data_fetcher import fetch_live_option_data
        from execution.scheduler import run_scheduled_trading
        print("  ✅ All imports successful")
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False


def check_broker_creation():
    """Verify brokers can be instantiated."""
    print("\n🔍 Checking broker creation...")
    try:
        from brokers import BrokerFactory
        
        # Test IBKR
        ibkr = BrokerFactory.create_broker('ibkr')
        print(f"  ✅ IBKR broker created: {type(ibkr).__name__}")
        
        # Test Alpaca (with dummy credentials)
        alpaca = BrokerFactory.create_broker('alpaca', api_key='test', secret_key='test')
        print(f"  ✅ Alpaca broker created: {type(alpaca).__name__}")
        
        return True
    except Exception as e:
        print(f"  ❌ Broker creation error: {e}")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    print("\n🔍 Checking dependencies...")
    required_packages = {
        'ib_insync': 'IBKR broker',
        'alpaca': 'Alpaca broker (alpaca-py package)',
        'pandas': 'Data processing',
        'numpy': 'Numerical operations'
    }
    
    all_present = True
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"  ✅ {package} installed ({description})")
        except ImportError:
            print(f"  ❌ {package} NOT installed ({description})")
            all_present = False
    
    return all_present


def check_configuration():
    """Check if configuration files exist."""
    print("\n🔍 Checking configuration...")
    
    checks = {
        '.env.example': 'Configuration template',
        'BROKER_SETUP.md': 'Setup guide',
        'README.md': 'Documentation',
        'requirements.txt': 'Dependencies list'
    }
    
    all_present = True
    for file, description in checks.items():
        if os.path.exists(file):
            print(f"  ✅ {file} exists ({description})")
        else:
            print(f"  ⚠️  {file} missing ({description})")
            all_present = False
    
    # Check for .env (optional)
    if os.path.exists('.env'):
        print(f"  ✅ .env exists (configuration file)")
    else:
        print(f"  ℹ️  .env not found (optional - copy from .env.example)")
    
    return all_present


def check_examples():
    """Check if example files exist and can run."""
    print("\n🔍 Checking examples...")
    
    examples = [
        'examples/broker_example.py',
        'examples/test_brokers.py'
    ]
    
    all_present = True
    for example in examples:
        if os.path.exists(example):
            print(f"  ✅ {example} exists")
        else:
            print(f"  ❌ {example} missing")
            all_present = False
    
    return all_present


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Multi-Broker Setup Verification")
    print("=" * 60)
    
    results = {
        'Imports': check_imports(),
        'Broker Creation': check_broker_creation(),
        'Dependencies': check_dependencies(),
        'Configuration': check_configuration(),
        'Examples': check_examples()
    }
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for check, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{check:.<30} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Configure your broker credentials in .env")
        print("3. Run: python main.py [ibkr|alpaca]")
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        print("\nTo fix:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Ensure all files are present")
        print("3. Run this script again")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
