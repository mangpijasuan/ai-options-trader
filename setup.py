#!/usr/bin/env python3
"""
Setup script for AI Options Trader

This script helps with initial setup and validation
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is adequate"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def check_data_files():
    """Check if required data files exist"""
    print("\n📊 Checking data files...")
    required_files = [
        'data/historical_data.csv',
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"⚠️  {file} not found")
            all_exist = False
    
    return all_exist

def create_directories():
    """Create required directories"""
    print("\n📁 Creating directories...")
    dirs = ['logs', 'data', 'models']
    
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✅ {dir_name}/")
    
    return True

def train_initial_model():
    """Train the initial model if it doesn't exist"""
    print("\n🤖 Checking model...")
    
    if os.path.exists('models/model.pkl'):
        print("✅ Model already exists")
        return True
    
    if not os.path.exists('data/historical_data.csv'):
        print("⚠️  Cannot train model: data/historical_data.csv not found")
        return False
    
    print("🎓 Training initial model...")
    try:
        subprocess.check_call([sys.executable, "models/train_model.py"])
        print("✅ Model trained successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to train model")
        return False

def main():
    """Run setup"""
    print("=" * 60)
    print("🚀 AI Options Trader Setup")
    print("=" * 60)
    
    steps = [
        ("Python Version", check_python_version),
        ("Directories", create_directories),
        ("Requirements", install_requirements),
        ("Data Files", check_data_files),
        ("Model", train_initial_model),
    ]
    
    results = {}
    for step_name, step_func in steps:
        try:
            results[step_name] = step_func()
        except Exception as e:
            print(f"❌ Error in {step_name}: {e}")
            results[step_name] = False
    
    print("\n" + "=" * 60)
    print("📋 Setup Summary")
    print("=" * 60)
    
    for step_name, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {step_name}")
    
    all_success = all(results.values())
    
    print("\n" + "=" * 60)
    if all_success:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Configure IBKR connection in config.py")
        print("2. Start TWS or IB Gateway")
        print("3. Run: python main.py")
        print("4. View dashboard: streamlit run dashboard/dashboard.py")
    else:
        print("⚠️  Setup completed with warnings")
        print("\nPlease address the issues above before running the trader.")
    print("=" * 60)
    
    return 0 if all_success else 1

if __name__ == "__main__":
    sys.exit(main())
