---
name: captcha-solver
description: Solve CAPTCHAs programmatically using 2captcha API. Use when encountering reCAPTCHA, hCaptcha, image CAPTCHAs, or any verification challenges during web automation or API signup flows.
---

# Captcha Solver

Solve CAPTCHAs using 2captcha.com API service.

## Prerequisites

- 2captcha API key stored in `TWOCAPTCHA_API_KEY` environment variable
- Python 3 with `requests` library

## Quick Usage

### reCAPTCHA v2

```bash
python3 scripts/solve_captcha.py recaptcha \
  --sitekey "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-" \
  --pageurl "https://example.com/signup"
```

### hCaptcha

```bash
python3 scripts/solve_captcha.py hcaptcha \
  --sitekey "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2" \
  --pageurl "https://example.com/signup"
```

### Image CAPTCHA

```bash
python3 scripts/solve_captcha.py image --file /path/to/captcha.png
# Or from base64:
python3 scripts/solve_captcha.py image --base64 "iVBORw0KGgo..."
```

## Finding Sitekey

For reCAPTCHA/hCaptcha, find the sitekey in page HTML:
- Look for `data-sitekey` attribute
- Or search for `sitekey` in page source
- Example: `<div class="g-recaptcha" data-sitekey="6Le...">`

## Integration Pattern

1. Navigate to page with captcha
2. Extract sitekey from page HTML
3. Run solver script with sitekey + page URL
4. Script returns solution token
5. Inject token into form/submit with token

## Output

Script prints JSON with solution:
```json
{"ok": true, "solution": "03AGdBq24...", "cost": "$0.003"}
```

On error:
```json
{"ok": false, "error": "ERROR_WRONG_USER_KEY"}
```

## Supported Types

| Type | Flag | Required Params |
|------|------|-----------------|
| reCAPTCHA v2 | `recaptcha` | `--sitekey`, `--pageurl` |
| reCAPTCHA v3 | `recaptcha3` | `--sitekey`, `--pageurl`, `--action` |
| hCaptcha | `hcaptcha` | `--sitekey`, `--pageurl` |
| Image | `image` | `--file` or `--base64` |
| Text | `text` | `--text` (e.g., "What is 2+2?") |

## Cost

- reCAPTCHA v2: ~$2.99/1000
- hCaptcha: ~$2.99/1000  
- Image: ~$1.00/1000
- Average solve time: 10-60 seconds
