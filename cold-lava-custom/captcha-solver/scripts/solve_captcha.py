#!/usr/bin/env python3
"""
Captcha solver using 2captcha.com API.
Requires TWOCAPTCHA_API_KEY environment variable.
"""

import argparse
import base64
import json
import os
import sys
import time

try:
    import requests
except ImportError:
    print(json.dumps({"ok": False, "error": "requests library required: pip install requests"}))
    sys.exit(1)

API_KEY = os.environ.get("TWOCAPTCHA_API_KEY")
BASE_URL = "http://2captcha.com"


def submit_captcha(params: dict) -> str:
    """Submit captcha and return task ID."""
    params["key"] = API_KEY
    params["json"] = 1
    
    resp = requests.post(f"{BASE_URL}/in.php", data=params, timeout=30)
    data = resp.json()
    
    if data.get("status") != 1:
        raise Exception(data.get("request", "Unknown error"))
    
    return data["request"]


def get_result(task_id: str, max_wait: int = 120) -> str:
    """Poll for captcha solution."""
    params = {"key": API_KEY, "action": "get", "id": task_id, "json": 1}
    
    start = time.time()
    while time.time() - start < max_wait:
        time.sleep(5)
        resp = requests.get(f"{BASE_URL}/res.php", params=params, timeout=30)
        data = resp.json()
        
        if data.get("status") == 1:
            return data["request"]
        elif data.get("request") != "CAPCHA_NOT_READY":
            raise Exception(data.get("request", "Unknown error"))
    
    raise Exception("Timeout waiting for solution")


def solve_recaptcha_v2(sitekey: str, pageurl: str, invisible: bool = False) -> str:
    """Solve reCAPTCHA v2."""
    params = {
        "method": "userrecaptcha",
        "googlekey": sitekey,
        "pageurl": pageurl,
    }
    if invisible:
        params["invisible"] = 1
    
    task_id = submit_captcha(params)
    return get_result(task_id)


def solve_recaptcha_v3(sitekey: str, pageurl: str, action: str, min_score: float = 0.3) -> str:
    """Solve reCAPTCHA v3."""
    params = {
        "method": "userrecaptcha",
        "googlekey": sitekey,
        "pageurl": pageurl,
        "version": "v3",
        "action": action,
        "min_score": min_score,
    }
    
    task_id = submit_captcha(params)
    return get_result(task_id)


def solve_hcaptcha(sitekey: str, pageurl: str) -> str:
    """Solve hCaptcha."""
    params = {
        "method": "hcaptcha",
        "sitekey": sitekey,
        "pageurl": pageurl,
    }
    
    task_id = submit_captcha(params)
    return get_result(task_id)


def solve_image(image_data: str) -> str:
    """Solve image captcha. image_data is base64 encoded."""
    params = {
        "method": "base64",
        "body": image_data,
    }
    
    task_id = submit_captcha(params)
    return get_result(task_id, max_wait=60)


def solve_text(question: str) -> str:
    """Solve text-based captcha/question."""
    params = {
        "method": "textcaptcha",
        "textcaptcha": question,
    }
    
    task_id = submit_captcha(params)
    return get_result(task_id, max_wait=60)


def main():
    parser = argparse.ArgumentParser(description="Solve CAPTCHAs via 2captcha API")
    subparsers = parser.add_subparsers(dest="type", required=True)
    
    # reCAPTCHA v2
    p_recaptcha = subparsers.add_parser("recaptcha", help="Solve reCAPTCHA v2")
    p_recaptcha.add_argument("--sitekey", required=True)
    p_recaptcha.add_argument("--pageurl", required=True)
    p_recaptcha.add_argument("--invisible", action="store_true")
    
    # reCAPTCHA v3
    p_recaptcha3 = subparsers.add_parser("recaptcha3", help="Solve reCAPTCHA v3")
    p_recaptcha3.add_argument("--sitekey", required=True)
    p_recaptcha3.add_argument("--pageurl", required=True)
    p_recaptcha3.add_argument("--action", required=True)
    p_recaptcha3.add_argument("--min-score", type=float, default=0.3)
    
    # hCaptcha
    p_hcaptcha = subparsers.add_parser("hcaptcha", help="Solve hCaptcha")
    p_hcaptcha.add_argument("--sitekey", required=True)
    p_hcaptcha.add_argument("--pageurl", required=True)
    
    # Image
    p_image = subparsers.add_parser("image", help="Solve image captcha")
    p_image.add_argument("--file", help="Path to image file")
    p_image.add_argument("--base64", help="Base64 encoded image")
    
    # Text
    p_text = subparsers.add_parser("text", help="Solve text captcha/question")
    p_text.add_argument("--text", required=True, help="The question to answer")
    
    args = parser.parse_args()
    
    if not API_KEY:
        print(json.dumps({"ok": False, "error": "TWOCAPTCHA_API_KEY not set"}))
        sys.exit(1)
    
    try:
        if args.type == "recaptcha":
            solution = solve_recaptcha_v2(args.sitekey, args.pageurl, args.invisible)
        elif args.type == "recaptcha3":
            solution = solve_recaptcha_v3(args.sitekey, args.pageurl, args.action, args.min_score)
        elif args.type == "hcaptcha":
            solution = solve_hcaptcha(args.sitekey, args.pageurl)
        elif args.type == "image":
            if args.file:
                with open(args.file, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()
            elif args.base64:
                image_data = args.base64
            else:
                print(json.dumps({"ok": False, "error": "Provide --file or --base64"}))
                sys.exit(1)
            solution = solve_image(image_data)
        elif args.type == "text":
            solution = solve_text(args.text)
        else:
            print(json.dumps({"ok": False, "error": f"Unknown type: {args.type}"}))
            sys.exit(1)
        
        print(json.dumps({"ok": True, "solution": solution}))
        
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
