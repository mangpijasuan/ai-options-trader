# portfolio/portfolio_tracker.py

"""
Portfolio tracking functionality for monitoring positions and performance

TODO: Implement portfolio tracking features:
- Track open positions
- Calculate portfolio value
- Monitor P&L
- Track Greeks across portfolio
"""

class PortfolioTracker:
    """Track and manage the options portfolio"""
    
    def __init__(self):
        self.positions = {}
        self.closed_trades = []
        self.total_pnl = 0.0
    
    def add_position(self, symbol, contract_type, strike, expiry, quantity, entry_price):
        """Add a new position to the portfolio"""
        position_key = f"{symbol}_{contract_type}_{strike}_{expiry}"
        
        if position_key in self.positions:
            # Update existing position
            pos = self.positions[position_key]
            total_qty = pos['quantity'] + quantity
            avg_price = (pos['entry_price'] * pos['quantity'] + entry_price * quantity) / total_qty
            pos['quantity'] = total_qty
            pos['entry_price'] = avg_price
        else:
            # Create new position
            self.positions[position_key] = {
                'symbol': symbol,
                'type': contract_type,
                'strike': strike,
                'expiry': expiry,
                'quantity': quantity,
                'entry_price': entry_price
            }
    
    def close_position(self, position_key, exit_price, quantity=None):
        """Close a position (partial or full)"""
        if position_key not in self.positions:
            raise ValueError(f"Position {position_key} not found")
        
        pos = self.positions[position_key]
        close_qty = quantity if quantity else pos['quantity']
        
        if close_qty > pos['quantity']:
            raise ValueError(f"Cannot close {close_qty} contracts, only {pos['quantity']} available")
        
        pnl = (exit_price - pos['entry_price']) * close_qty * 100  # Options multiply by 100
        self.total_pnl += pnl
        
        # Record closed trade
        self.closed_trades.append({
            'position_key': position_key,
            'entry_price': pos['entry_price'],
            'exit_price': exit_price,
            'quantity': close_qty,
            'pnl': pnl
        })
        
        # Update or remove position
        if close_qty == pos['quantity']:
            del self.positions[position_key]
        else:
            pos['quantity'] -= close_qty
        
        return pnl
    
    def get_total_positions(self):
        """Get count of open positions"""
        return len(self.positions)
    
    def get_portfolio_value(self):
        """Calculate total portfolio value (would need current prices)"""
        # TODO: Implement with live pricing
        return sum(p['quantity'] * p['entry_price'] * 100 for p in self.positions.values())
    
    def get_portfolio_summary(self):
        """Get portfolio summary statistics"""
        return {
            'open_positions': len(self.positions),
            'total_pnl': self.total_pnl,
            'closed_trades': len(self.closed_trades),
            'portfolio_value': self.get_portfolio_value()
        }
