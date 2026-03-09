# IG Trading Skill

## Overview
Execute trades on IG Markets via their REST API using the `trading-ig` Python library.

**⚠️ CRITICAL: Paper trading mode is DEFAULT. Real trading requires explicit configuration change.**

---

## Setup

### 1. Environment Variables
Create `.env` file in Warren's workspace or export these:

```bash
# Required
export IG_API_KEY="your-api-key-from-ig"
export IG_USERNAME="your-ig-username"
export IG_PASSWORD="your-ig-password"
export IG_ACCOUNT_ID="your-account-id"

# Trading Mode (CRITICAL!)
export IG_TRADING_MODE="paper"  # paper (default) | live

# Optional
export IG_ACC_TYPE="DEMO"  # DEMO (default) | LIVE
```

### 2. Get IG API Credentials
1. Create IG account: https://www.ig.com
2. Request API access: https://labs.ig.com/
3. Get API key from Labs dashboard
4. Note your account ID (visible in IG platform)

### 3. Demo vs Live API
- **Demo API:** `demo-api.ig.com` (paper trading)
- **Live API:** `api.ig.com` (real money)

---

## Available Scripts

### Authentication & Session
```bash
# Test connection (always run this first)
./venv/bin/python skills/ig-trading/auth.py

# Get account info
./venv/bin/python skills/ig-trading/account.py
```

### Positions & Orders
```bash
# Get all open positions
./venv/bin/python skills/ig-trading/positions.py list

# Open a position (ALWAYS paper mode first!)
./venv/bin/python skills/ig-trading/positions.py open --market CT.D.CFI2Z6.MONTH.IP --direction BUY --size 1

# Close a position
./venv/bin/python skills/ig-trading/positions.py close --deal-id <deal_id>
```

### Market Data
```bash
# Get current price for a market
./venv/bin/python skills/ig-trading/markets.py price CT.D.CFI2Z6.MONTH.IP

# Search for markets
./venv/bin/python skills/ig-trading/markets.py search "cotton"

# Get market details
./venv/bin/python skills/ig-trading/markets.py info CT.D.CFI2Z6.MONTH.IP
```

### Position Sizing
```bash
# Calculate position size based on risk
./venv/bin/python skills/ig-trading/sizing.py --account-size 10000 --risk-pct 2 --stop-distance 50 --market cotton
```

---

## IG Market EPICs (Key Markets)

### Cotton
| Description | EPIC | Type |
|-------------|------|------|
| Cotton Dec 2026 | CT.D.CFI2Z6.MONTH.IP | CFD |
| Cotton Mar 2027 | CT.D.CFI2H7.MONTH.IP | CFD |
| Cotton Jul 2027 | CT.D.CFI2N7.MONTH.IP | CFD |

### Coffee
| Description | EPIC | Type |
|-------------|------|------|
| Coffee Dec 2026 | CF.D.KC.Z6.IP | CFD |
| Coffee Mar 2027 | CF.D.KC.H7.IP | CFD |

### Cocoa
| Description | EPIC | Type |
|-------------|------|------|
| Cocoa Dec 2026 | CC.D.CC.Z6.IP | CFD |
| Cocoa Mar 2027 | CC.D.CC.H7.IP | CFD |

### Sugar
| Description | EPIC | Type |
|-------------|------|------|
| Sugar Mar 2027 | SB.D.SB.H7.IP | CFD |

### Grains
| Description | EPIC | Type |
|-------------|------|------|
| Corn Dec 2026 | CN.D.C.Z6.IP | CFD |
| Soybeans Jan 2027 | S.D.S.F7.IP | CFD |
| Wheat Dec 2026 | W.D.W.Z6.IP | CFD |

**Note:** Search for exact EPICs using the market search - they may vary.

---

## Rate Limits

IG enforces these limits:
- **REST API:** 30 requests per minute
- **Trading:** 10 orders per second
- **Historical data:** 10,000 allowance per week

Scripts include automatic rate limiting.

---

## Error Handling

### Common Errors
| Error | Meaning | Action |
|-------|---------|--------|
| `invalid.token` | Session expired | Re-authenticate |
| `insufficient.funds` | Not enough margin | Reduce position size |
| `market.closed` | Market not trading | Wait for market hours |
| `position.not.found` | Deal ID invalid | Check deal reference |
| `minimum.order.value` | Size too small | Increase position size |

### Session Management
- Sessions expire after 6 hours of inactivity
- Scripts auto-refresh sessions when needed
- Store session tokens in `~/.ig_session.json`

---

## Trading Mode Safety

```python
# This is ALWAYS checked before any trade execution
if os.getenv('IG_TRADING_MODE', 'paper') != 'live':
    print("🔒 PAPER MODE - No real trade executed")
    # Log the intended trade
    return None
```

**To enable live trading:**
1. Set `IG_TRADING_MODE=live` in environment
2. Set `IG_ACC_TYPE=LIVE`
3. Both must be set or trades won't execute

---

## Integration with Warren

Warren should:
1. Always validate signals through TRADE-CHECKLIST.md first
2. Calculate position size using `sizing.py`
3. Log intended trade to `positions/pending/`
4. Execute via `positions.py open`
5. Log result to `positions/history/`
6. Track P&L daily

---

## Testing Commands

```bash
# 1. Test authentication
./venv/bin/python skills/ig-trading/auth.py

# 2. Get account balance
./venv/bin/python skills/ig-trading/account.py

# 3. Search for cotton market
./venv/bin/python skills/ig-trading/markets.py search "cotton"

# 4. Get price
./venv/bin/python skills/ig-trading/markets.py price CT.D.CFI2Z6.MONTH.IP

# 5. Paper trade test
IG_TRADING_MODE=paper ./venv/bin/python skills/ig-trading/positions.py open \
  --market CT.D.CFI2Z6.MONTH.IP \
  --direction BUY \
  --size 1 \
  --stop 6500 \
  --limit 7500
```

---

## Files

```
skills/ig-trading/
├── SKILL.md          # This file
├── auth.py           # Authentication & session management
├── account.py        # Account info & balance
├── positions.py      # Open/close/list positions
├── markets.py        # Market data & search
├── sizing.py         # Position size calculator
├── config.py         # Shared configuration
└── utils.py          # Error handling & rate limiting
```
