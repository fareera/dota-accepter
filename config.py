import json
import sys

DEFAULTS = {
    "scan_interval": 0.5,
    "match_threshold": 0.8,
    "cooldown_seconds": 30,
}

REQUIRED_WECHAT_KEYS = ["app_id", "app_secret", "template_id", "user_openid"]


def load_config(path: str = "config.json") -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found: {path}")
        print("Copy config.example.json to config.json and fill in your settings.")
        sys.exit(1)

    config = {**DEFAULTS, **data}

    wechat = config.get("wechat", {})
    missing = [k for k in REQUIRED_WECHAT_KEYS if k not in wechat or not wechat[k]]
    if missing:
        print(f"Error: Missing required wechat config keys: {', '.join(missing)}")
        sys.exit(1)

    config["wechat"] = wechat
    return config
