# portfolio/trade_logger.py

"""
Trade logging functionality

TODO: Implement trade logging features:
- Log all trades to file/database
- Track trade performance
- Generate trade reports
"""

import csv
import os
from datetime import datetime
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class TradeLogger:
    """Log all trading activity"""
    
    def __init__(self, log_file=None):
        if log_file is None:
            os.makedirs(config.LOG_DIR, exist_ok=True)
            log_file = os.path.join(config.LOG_DIR, 'trades.csv')
        
        self.log_file = log_file
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """Create log file with headers if it doesn't exist"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp',
                    'action',
                    'symbol',
                    'type',
                    'strike',
                    'expiry',
                    'quantity',
                    'price',
                    'confidence',
                    'status',
                    'notes'
                ])
    
    def log_trade(self, action, symbol, contract_type, strike, expiry, 
                  quantity, price=None, confidence=None, status='executed', notes=''):
        """
        Log a trade to the file
        
        Args:
            action: 'BUY' or 'SELL'
            symbol: Underlying symbol
            contract_type: 'CALL' or 'PUT'
            strike: Strike price
            expiry: Expiration date
            quantity: Number of contracts
            price: Execution price (if available)
            confidence: ML model confidence (if applicable)
            status: Trade status ('executed', 'pending', 'failed', etc.)
            notes: Additional notes
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                action,
                symbol,
                contract_type,
                strike,
                expiry,
                quantity,
                price if price else '',
                confidence if confidence else '',
                status,
                notes
            ])
    
    def log_signal(self, symbol, prediction, confidence, traded=False, reason=''):
        """
        Log a trading signal
        
        Args:
            symbol: Symbol that generated signal
            prediction: 'CALL' or 'PUT'
            confidence: Confidence level
            traded: Whether trade was executed
            reason: Reason for trade/no-trade decision
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        signal_file = os.path.join(config.LOG_DIR, 'signals.csv')
        
        # Create signal log if it doesn't exist
        if not os.path.exists(signal_file):
            with open(signal_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'symbol', 'prediction', 'confidence', 'traded', 'reason'])
        
        with open(signal_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, symbol, prediction, confidence, traded, reason])
    
    def get_recent_trades(self, n=10):
        """
        Get the most recent N trades
        
        Args:
            n: Number of trades to retrieve
        
        Returns:
            list: List of recent trades
        """
        if not os.path.exists(self.log_file):
            return []
        
        trades = []
        with open(self.log_file, 'r') as f:
            reader = csv.DictReader(f)
            trades = list(reader)
        
        return trades[-n:] if len(trades) > n else trades
    
    def get_trades_for_symbol(self, symbol):
        """
        Get all trades for a specific symbol
        
        Args:
            symbol: Symbol to filter by
        
        Returns:
            list: List of trades for the symbol
        """
        if not os.path.exists(self.log_file):
            return []
        
        trades = []
        with open(self.log_file, 'r') as f:
            reader = csv.DictReader(f)
            trades = [row for row in reader if row['symbol'] == symbol]
        
        return trades
