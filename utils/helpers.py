# utils/helpers.py

from datetime import datetime, timedelta

def get_next_friday():
    today = datetime.today()
    days_ahead = 4 - today.weekday()  # Friday = 4
    if days_ahead <= 0:
        days_ahead += 7
    next_friday = today + timedelta(days=days_ahead)
    return next_friday.strftime('%Y%m%d')
