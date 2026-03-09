#!/usr/bin/env python3
"""
Configuration for IG Trading Skill
Loads settings from environment variables with safe defaults.
"""

import os
import json
from pathlib import Path

# Warren's workspace root
WARREN_ROOT = Path("/home/moltbot/.clawdbot-warren")
VENV_PYTHON = WARREN_ROOT / "venv/bin/python"

# Session storage
SESSION_FILE = Path.home() / ".ig_session.json"

# Logging
LOG_DIR = WARREN_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Position tracking
POSITIONS_DIR = WARREN_ROOT / "positions"
POSITIONS_DIR.mkdir(exist_ok=True)

def get_config():
    """Get IG API configuration from environment."""
    return {
        "api_key": os.getenv("IG_API_KEY"),
        "username": os.getenv("IG_USERNAME"),
        "password": os.getenv("IG_PASSWORD"),
        "account_id": os.getenv("IG_ACCOUNT_ID"),
        "acc_type": os.getenv("IG_ACC_TYPE", "DEMO"),  # DEMO or LIVE
        "trading_mode": os.getenv("IG_TRADING_MODE", "paper"),  # paper or live
    }

def validate_config():
    """Validate that required config is present."""
    config = get_config()
    required = ["api_key", "username", "password", "account_id"]
    missing = [k for k in required if not config.get(k)]
    
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}\n"
                        f"Set: {', '.join('IG_' + k.upper() for k in missing)}")
    return config

def is_live_trading_enabled():
    """Check if live trading is explicitly enabled."""
    config = get_config()
    return (
        config["trading_mode"] == "live" and 
        config["acc_type"] == "LIVE"
    )

def is_paper_mode():
    """Check if we're in paper trading mode."""
    return not is_live_trading_enabled()

def get_api_base_url():
    """Get the correct API URL based on mode."""
    config = get_config()
    if config["acc_type"] == "LIVE":
        return "https://api.ig.com/gateway/deal"
    return "https://demo-api.ig.com/gateway/deal"

def save_session(session_data):
    """Save session data to file."""
    with open(SESSION_FILE, 'w') as f:
        json.dump(session_data, f)

def load_session():
    """Load session data from file."""
    if SESSION_FILE.exists():
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    return None

def clear_session():
    """Clear stored session."""
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()

# Market EPICs for common commodities
MARKET_EPICS = {
    # Cotton
    "cotton_dec26": "CT.D.CFI2Z6.MONTH.IP",
    "cotton_mar27": "CT.D.CFI2H7.MONTH.IP",
    "cotton_jul27": "CT.D.CFI2N7.MONTH.IP",
    # Coffee
    "coffee_dec26": "CF.D.KC.Z6.IP",
    "coffee_mar27": "CF.D.KC.H7.IP",
    # Cocoa
    "cocoa_dec26": "CC.D.CC.Z6.IP",
    "cocoa_mar27": "CC.D.CC.H7.IP",
    # Sugar
    "sugar_mar27": "SB.D.SB.H7.IP",
    # Grains
    "corn_dec26": "CN.D.C.Z6.IP",
    "soy_jan27": "S.D.S.F7.IP",
    "wheat_dec26": "W.D.W.Z6.IP",
}

if __name__ == "__main__":
    # Test configuration
    print("=" * 50)
    print("IG Trading Configuration Test")
    print("=" * 50)
    
    try:
        config = validate_config()
        print("✅ Configuration valid")
        print(f"   Account Type: {config['acc_type']}")
        print(f"   Trading Mode: {config['trading_mode']}")
        print(f"   API URL: {get_api_base_url()}")
        print(f"   Paper Mode: {is_paper_mode()}")
        print(f"   Live Trading: {is_live_trading_enabled()}")
    except ValueError as e:
        print(f"❌ Configuration error:\n{e}")
