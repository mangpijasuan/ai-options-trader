# portfolio/risk_engine.py

"""
Risk management engine for the trading system

TODO: Implement risk management features:
- Position sizing
- Max loss limits
- Portfolio delta limits
- Exposure monitoring
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class RiskEngine:
    """Risk management and position sizing engine"""
    
    def __init__(self):
        self.max_position_size = config.MAX_POSITION_SIZE
        self.max_daily_loss = config.MAX_DAILY_LOSS
        self.max_portfolio_delta = config.MAX_PORTFOLIO_DELTA
        self.daily_pnl = 0.0
        self.portfolio_delta = 0.0
    
    def check_position_size(self, quantity):
        """
        Check if position size is within limits
        
        Args:
            quantity: Number of contracts
        
        Returns:
            tuple: (bool, str) - (is_valid, message)
        """
        if quantity > self.max_position_size:
            return False, f"Position size {quantity} exceeds max {self.max_position_size}"
        return True, "Position size OK"
    
    def check_daily_loss_limit(self, potential_loss):
        """
        Check if potential loss would exceed daily limit
        
        Args:
            potential_loss: Potential loss amount
        
        Returns:
            tuple: (bool, str) - (is_valid, message)
        """
        if abs(self.daily_pnl + potential_loss) > self.max_daily_loss:
            return False, f"Daily loss limit would be exceeded: {self.daily_pnl + potential_loss:.2f}"
        return True, "Daily loss limit OK"
    
    def check_portfolio_delta(self, additional_delta):
        """
        Check if additional delta would exceed portfolio limit
        
        Args:
            additional_delta: Delta to be added
        
        Returns:
            tuple: (bool, str) - (is_valid, message)
        """
        new_delta = abs(self.portfolio_delta + additional_delta)
        if new_delta > self.max_portfolio_delta:
            return False, f"Portfolio delta {new_delta:.2f} would exceed max {self.max_portfolio_delta}"
        return True, "Portfolio delta OK"
    
    def validate_trade(self, quantity, position_delta, potential_loss=0):
        """
        Validate if a trade passes all risk checks
        
        Args:
            quantity: Number of contracts
            position_delta: Delta of the position
            potential_loss: Potential loss amount
        
        Returns:
            tuple: (bool, list) - (is_valid, list of messages)
        """
        checks = []
        all_valid = True
        
        # Check position size
        valid, msg = self.check_position_size(quantity)
        checks.append(msg)
        if not valid:
            all_valid = False
        
        # Check daily loss
        valid, msg = self.check_daily_loss_limit(potential_loss)
        checks.append(msg)
        if not valid:
            all_valid = False
        
        # Check portfolio delta
        valid, msg = self.check_portfolio_delta(position_delta * quantity)
        checks.append(msg)
        if not valid:
            all_valid = False
        
        return all_valid, checks
    
    def update_daily_pnl(self, pnl):
        """Update daily P&L"""
        self.daily_pnl += pnl
    
    def update_portfolio_delta(self, delta_change):
        """Update portfolio delta"""
        self.portfolio_delta += delta_change
    
    def reset_daily_metrics(self):
        """Reset daily metrics (call at start of trading day)"""
        self.daily_pnl = 0.0
    
    def get_risk_summary(self):
        """Get risk metrics summary"""
        return {
            'daily_pnl': self.daily_pnl,
            'portfolio_delta': self.portfolio_delta,
            'daily_loss_limit': self.max_daily_loss,
            'remaining_loss_capacity': self.max_daily_loss - abs(self.daily_pnl),
            'delta_limit': self.max_portfolio_delta,
            'remaining_delta_capacity': self.max_portfolio_delta - abs(self.portfolio_delta)
        }
