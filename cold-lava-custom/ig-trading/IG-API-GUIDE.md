# IG Markets Demo API — Agent Integration Guide

## Base URL

**Demo:** `https://demo-api.ig.com/gateway/deal`  
**Live:** `https://api.ig.com/gateway/deal` (do NOT use until tested on demo)

All endpoints below are relative to this base URL.

---

## Step 1: Authentication (Required Before Anything Else)

IG uses a two-step auth flow. The API key alone is NOT enough.

### POST `/session`

**Headers:**
```
Content-Type: application/json
Accept: application/json
X-IG-API-KEY: <your-api-key>
VERSION: 2
```

**Body:**
```json
{
  "identifier": "<your-ig-username>",
  "password": "<your-ig-password>"
}
```

**Response headers you need to capture:**
- `CST` — Client Session Token
- `X-SECURITY-TOKEN` — Account security token

**Both tokens expire after ~6 hours of inactivity.** If you get 401 errors mid-session, re-authenticate.

---

## Step 2: Authenticated Requests

Every subsequent API call must include ALL THREE of these headers:

```
X-IG-API-KEY: <your-api-key>
CST: <from-session-response>
X-SECURITY-TOKEN: <from-session-response>
```

Plus the standard:
```
Content-Type: application/json
Accept: application/json
VERSION: <1, 2, or 3 depending on endpoint>
```

---

## Step 3: Get Account Info

### GET `/accounts`

**Headers:** Standard authenticated headers + `VERSION: 1`

Returns your account balances, IDs, and available funds. Use this to confirm auth is working before attempting trades.

---

## Step 4: Search for a Market

### GET `/markets?searchTerm=EURUSD`

**Headers:** Standard authenticated headers + `VERSION: 1`

Returns a list of matching markets. The key field you need is `epic` — this is IG's unique identifier for each instrument (e.g., `CS.D.EURUSD.CFD.IP`).

---

## Step 5: Get Market Details

### GET `/markets/{epic}`

**Headers:** Standard authenticated headers + `VERSION: 3`

Returns full market info including:
- Current bid/offer prices
- Minimum stop distance
- Margin requirements
- Trading status (is the market open?)
- Lot size / contract details

---

## Step 6: Place a Trade

### POST `/positions/otc`

**Headers:** Standard authenticated headers + `VERSION: 2`

**Body:**
```json
{
  "epic": "CS.D.EURUSD.CFD.IP",
  "direction": "BUY",
  "size": 1,
  "orderType": "MARKET",
  "currencyCode": "GBP",
  "expiry": "-",
  "guaranteedStop": false,
  "forceOpen": true
}
```

**Key fields:**
- `direction`: `BUY` or `SELL`
- `size`: Position size (check minDealSize from market details)
- `orderType`: `MARKET` for instant execution, `LIMIT` for limit orders
- `expiry`: Use `"-"` for non-expiring (most CFDs), or `"DFB"` for daily funded bets
- `forceOpen`: Set to `true` to open a new position rather than closing an existing opposite one

**Response:** Returns a `dealReference`. Use this to confirm the trade.

---

## Step 7: Confirm a Trade

### GET `/confirms/{dealReference}`

**Headers:** Standard authenticated headers + `VERSION: 1`

Check `dealStatus`:
- `ACCEPTED` — trade went through
- `REJECTED` — check `reason` field for why

---

## Step 8: Close a Position

### DELETE `/positions/otc`

**Headers:** Standard authenticated headers + `VERSION: 1`  
**Note:** IG requires DELETE with a body, which some HTTP clients don't support. If so, use POST with the header `_method: DELETE`.

**Body:**
```json
{
  "dealId": "<deal-id-from-open-position>",
  "direction": "SELL",
  "size": 1,
  "orderType": "MARKET"
}
```

The `direction` must be the OPPOSITE of the opening trade (opened BUY → close with SELL).

---

## Step 9: View Open Positions

### GET `/positions`

**Headers:** Standard authenticated headers + `VERSION: 2`

Returns all open positions with P&L, entry prices, and deal IDs needed for closing.

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Missing CST/Security tokens | Complete the `/session` auth flow first |
| 403 Forbidden | API key not activated for demo | Log into IG demo web platform to activate |
| `error.security.api-key-missing` | No `X-IG-API-KEY` header | Add the header to every request |
| `REJECTED` with `MARKET_CLOSED` | Trading outside market hours | Check market hours via `/markets/{epic}` |
| `REJECTED` with `MINIMUM_ORDER_SIZE` | Size too small | Check `minDealSize` from market details |
| Connection refused | Wrong base URL | Demo uses `demo-api.ig.com`, not `api.ig.com` |
| `VERSION` errors | Wrong or missing version header | Each endpoint requires a specific version — check docs |

---

## Agent Implementation Checklist

- [ ] Store API key, username, and password securely
- [ ] Authenticate via `/session` on startup
- [ ] Cache CST and X-SECURITY-TOKEN for reuse
- [ ] Implement automatic re-authentication on 401 responses
- [ ] Always check `/confirms/{dealReference}` after placing trades
- [ ] Validate market is open before attempting trades
- [ ] Respect rate limits (roughly 30 requests per minute on non-trading, 15 per minute on trading)
- [ ] Log all deal references and confirmations

---

## Rate Limits

IG enforces rate limits per API key:
- **Trading endpoints:** ~15 requests/min
- **Non-trading endpoints:** ~30 requests/min
- **Historical data:** ~15 requests/min

Exceeding these returns 403. Build in delays between rapid-fire calls.

---

## Useful Reference

- [IG REST API Documentation](https://labs.ig.com/rest-trading-api-reference)
- [IG API Companion (Swagger)](https://labs.ig.com/sample-apps/api-companion/index.html)
