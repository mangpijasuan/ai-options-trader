# strategies/rules.py

"""
Rule-based trading strategies

TODO: Implement rule-based strategies:
- Technical indicators
- Price action rules
- Volume-based rules
- Time-based rules
"""

import pandas as pd
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_momentum_rule(df: pd.DataFrame, lookback=5, threshold=0.02):
    """
    Check if stock has positive momentum
    
    Args:
        df: DataFrame with price data
        lookback: Number of periods to look back
        threshold: Minimum return threshold
    
    Returns:
        bool: True if momentum condition is met
    """
    if len(df) < lookback:
        return False
    
    recent_return = (df['underlying_close'].iloc[-1] / df['underlying_close'].iloc[-lookback] - 1)
    return recent_return > threshold

def check_volume_rule(df: pd.DataFrame, volume_multiplier=1.5):
    """
    Check if volume is above average
    
    Args:
        df: DataFrame with volume data
        volume_multiplier: Multiplier for average volume
    
    Returns:
        bool: True if volume condition is met
    """
    if len(df) < 2:
        return False
    
    avg_volume = df['volume'].mean()
    current_volume = df['volume'].iloc[-1]
    
    return current_volume > (avg_volume * volume_multiplier)

def check_iv_rule(current_iv, historical_iv_percentile=50):
    """
    Check if IV is within acceptable range
    
    Args:
        current_iv: Current implied volatility
        historical_iv_percentile: Target IV percentile
    
    Returns:
        bool: True if IV condition is met
    """
    # TODO: Implement with historical IV data
    # For now, just check if IV is reasonable
    return 0.1 < current_iv < 0.8

def apply_entry_rules(df: pd.DataFrame, signal: str):
    """
    Apply all entry rules to validate a trade signal
    
    Args:
        df: DataFrame with market data
        signal: 'CALL' or 'PUT'
    
    Returns:
        tuple: (bool, list) - (is_valid, list of passed rules)
    """
    passed_rules = []
    
    # Check momentum (should align with signal)
    has_momentum = check_momentum_rule(df)
    if (signal == 'CALL' and has_momentum) or (signal == 'PUT' and not has_momentum):
        passed_rules.append('momentum_aligned')
    
    # Check volume
    if check_volume_rule(df):
        passed_rules.append('volume_adequate')
    
    # Check IV
    if len(df) > 0:
        current_iv = df['iv'].iloc[-1]
        if check_iv_rule(current_iv):
            passed_rules.append('iv_acceptable')
    
    # Need at least 2 rules to pass
    is_valid = len(passed_rules) >= 2
    
    return is_valid, passed_rules

def apply_exit_rules(entry_price, current_price, days_held, contract_type='CALL'):
    """
    Apply exit rules to determine if position should be closed
    
    Args:
        entry_price: Entry price
        current_price: Current price
        days_held: Number of days position has been held
        contract_type: 'CALL' or 'PUT'
    
    Returns:
        tuple: (bool, str) - (should_exit, reason)
    """
    pnl_pct = (current_price / entry_price - 1) * 100
    
    # Take profit at 50%
    if pnl_pct > 50:
        return True, 'take_profit_50pct'
    
    # Stop loss at -30%
    if pnl_pct < -30:
        return True, 'stop_loss_30pct'
    
    # Time-based exit (close 2 days before expiry)
    # TODO: Calculate actual days to expiry
    if days_held > 5:
        return True, 'approaching_expiry'
    
    return False, 'hold'
