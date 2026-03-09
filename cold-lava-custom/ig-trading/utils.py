#!/usr/bin/env python3
"""
Utility functions for IG Trading Skill
Rate limiting, error handling, logging.
"""

import time
import json
import logging
from datetime import datetime
from pathlib import Path
from functools import wraps

from config import LOG_DIR, POSITIONS_DIR

# Setup logging
def setup_logging(name="ig_trading"):
    """Setup logging with file and console output."""
    log_file = LOG_DIR / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(name)

logger = setup_logging()

# Rate limiting
class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, calls_per_minute=25):
        self.calls_per_minute = calls_per_minute
        self.calls = []
    
    def wait_if_needed(self):
        """Wait if we're approaching rate limit."""
        now = time.time()
        # Remove calls older than 1 minute
        self.calls = [c for c in self.calls if now - c < 60]
        
        if len(self.calls) >= self.calls_per_minute:
            sleep_time = 60 - (now - self.calls[0]) + 1
            logger.warning(f"Rate limit approaching, sleeping {sleep_time:.1f}s")
            time.sleep(sleep_time)
        
        self.calls.append(now)

rate_limiter = RateLimiter()

def rate_limited(func):
    """Decorator to apply rate limiting to API calls."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        rate_limiter.wait_if_needed()
        return func(*args, **kwargs)
    return wrapper

# Error handling
class IGError(Exception):
    """Base exception for IG API errors."""
    pass

class AuthenticationError(IGError):
    """Authentication failed."""
    pass

class TradingError(IGError):
    """Trading operation failed."""
    pass

class MarketError(IGError):
    """Market data operation failed."""
    pass

def handle_ig_error(response):
    """Parse and raise appropriate error from IG response."""
    if response.status_code == 200:
        return
    
    try:
        error_data = response.json()
        error_code = error_data.get("errorCode", "UNKNOWN")
        error_msg = error_data.get("message", str(error_data))
    except:
        error_code = f"HTTP_{response.status_code}"
        error_msg = response.text
    
    error_mapping = {
        "invalid.token": AuthenticationError,
        "error.security.api-key-invalid": AuthenticationError,
        "error.security.invalid-credentials": AuthenticationError,
        "insufficient.funds": TradingError,
        "market.closed": TradingError,
        "position.not.found": TradingError,
        "minimum.order.value": TradingError,
    }
    
    exception_class = error_mapping.get(error_code, IGError)
    raise exception_class(f"{error_code}: {error_msg}")

# Trade logging
def log_trade_intent(trade_data):
    """Log intended trade before execution."""
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "status": "PENDING",
        "data": trade_data
    }
    
    pending_dir = POSITIONS_DIR / "pending"
    pending_dir.mkdir(exist_ok=True)
    
    filename = f"trade_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(pending_dir / filename, 'w') as f:
        json.dump(log_entry, f, indent=2)
    
    logger.info(f"Trade intent logged: {filename}")
    return pending_dir / filename

def log_trade_result(intent_file, result, status="EXECUTED"):
    """Log trade result after execution."""
    # Read intent
    with open(intent_file, 'r') as f:
        log_entry = json.load(f)
    
    # Update with result
    log_entry["status"] = status
    log_entry["result"] = result
    log_entry["completed_at"] = datetime.now().isoformat()
    
    # Move to history
    history_dir = POSITIONS_DIR / "history"
    history_dir.mkdir(exist_ok=True)
    
    new_file = history_dir / intent_file.name
    with open(new_file, 'w') as f:
        json.dump(log_entry, f, indent=2)
    
    # Remove pending file
    intent_file.unlink()
    
    logger.info(f"Trade result logged: {new_file.name} - {status}")
    return new_file

def log_position_update(position_data):
    """Log position update to current positions file."""
    positions_file = POSITIONS_DIR / "current_positions.json"
    
    if positions_file.exists():
        with open(positions_file, 'r') as f:
            positions = json.load(f)
    else:
        positions = {"positions": [], "last_updated": None}
    
    positions["positions"] = position_data
    positions["last_updated"] = datetime.now().isoformat()
    
    with open(positions_file, 'w') as f:
        json.dump(positions, f, indent=2)
    
    logger.info(f"Positions updated: {len(position_data)} open positions")

def log_pnl(pnl_data):
    """Log daily P&L."""
    pnl_dir = POSITIONS_DIR / "pnl"
    pnl_dir.mkdir(exist_ok=True)
    
    today = datetime.now().strftime('%Y-%m-%d')
    pnl_file = pnl_dir / f"{today}.json"
    
    pnl_entry = {
        "date": today,
        "timestamp": datetime.now().isoformat(),
        "data": pnl_data
    }
    
    with open(pnl_file, 'w') as f:
        json.dump(pnl_entry, f, indent=2)
    
    logger.info(f"P&L logged for {today}")

# Formatting helpers
def format_price(price, decimals=2):
    """Format price for display."""
    if price is None:
        return "N/A"
    return f"{float(price):.{decimals}f}"

def format_currency(amount, currency="USD"):
    """Format currency amount."""
    if amount is None:
        return "N/A"
    return f"{currency} {float(amount):,.2f}"

def format_position(position):
    """Format position data for display."""
    return {
        "deal_id": position.get("dealId"),
        "market": position.get("market", {}).get("instrumentName", "Unknown"),
        "epic": position.get("market", {}).get("epic"),
        "direction": position.get("position", {}).get("direction"),
        "size": position.get("position", {}).get("size"),
        "open_level": format_price(position.get("position", {}).get("openLevel")),
        "current_level": format_price(position.get("market", {}).get("bid")),
        "pnl": format_currency(position.get("position", {}).get("profit")),
        "stop_level": format_price(position.get("position", {}).get("stopLevel")),
        "limit_level": format_price(position.get("position", {}).get("limitLevel")),
    }

if __name__ == "__main__":
    print("Utils module loaded successfully")
    print(f"Log directory: {LOG_DIR}")
    print(f"Positions directory: {POSITIONS_DIR}")
