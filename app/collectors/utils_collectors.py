"""Helper functions for data collectors and working with APIs."""

import yaml
from datetime import datetime, timezone, timedelta
import pandas as pd
from config.config import *

def is_valid_post(text: str) -> bool:
    """Basic text validation."""
    return bool(text and text.strip() not in INVALID_MARKERS)

def is_valid(m, keyword, since) -> bool:
    """Shared message validation."""
    if not m.text or m.date < since:
        return False
    if keyword and keyword.lower() not in m.text.lower():
        return False
    return is_valid_post(m.text)

def extract_features(m, ch):
    """Format message fields for storage."""
    dt = m.date.astimezone(timezone.utc).isoformat()
    return {
        "channel": ch,
        "id": m.id,
        "datetime": dt,
        "text": m.text.strip(),
        "views": m.views or 0
    }

def get_since_time(period: str):
    """Convert period label to datetime threshold."""
    days = {"day": 1, "week": 7, "month": 30, "year": 365}
    return datetime.now(timezone.utc) - timedelta(days=days.get(period, 7))

def load_api(source: str):
    with open(SECRETS_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f).get(source)

def load_defaults(source: str):
    with open(DEFAULTS_FILE, "r", encoding="utf-8") as f:
        d = yaml.safe_load(f)["defaults"]
    return d[source], d["limit"], d["period"]

def save_to_csv(records, folder: str, name: str):
    """Save list of dicts to CSV in proper raw folder."""
    if not records:
        print("No data to save.")
        return None
    out_dir = RAW_DIR / folder
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{name}_{datetime.now().date()}.csv"
    path = out_dir / filename

    pd.DataFrame(records).to_csv(path, index=False, encoding=DEFAULT_ENCODING)
    print(f"Saved to {path}")
    return path
