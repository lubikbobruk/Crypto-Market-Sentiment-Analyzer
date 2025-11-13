"""Helper functions for data collectors and working with APIs."""

import yaml
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pandas as pd

from config import config

INVALID_MARKERS = {"[removed]", "[deleted]", "", None}


def load_api(data_source: str):
    """Load API credentials from secrets.yaml."""
    with open(config.SECRETS_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)[data_source]


def load_defaults(source: str):
    """Load default collector settings (limit, period, channels/subreddits)."""
    with open(config.DEFAULTS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)["defaults"]

    return data[source], data["limit"], data["period"]


def is_valid_post(text: str):
    """Filter out empty/removed posts."""
    return bool(text and text.strip() not in INVALID_MARKERS)


def get_since_time(period: str):
    """Return datetime threshold."""
    spans = {"day": 1, "week": 7, "month": 30, "year": 365}
    return datetime.now(timezone.utc) - timedelta(days=spans.get(period, 7))


def save_to_csv(data, folder: str, name: str):
    """Save records to CSV inside correct raw folder."""
    if not data:
        print("No data to save.")
        return None

    out_dir = config.RAW_DIR / folder
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{name}_{datetime.now().date()}.csv"
    path = out_dir / filename

    pd.DataFrame(data).to_csv(path, index=False, encoding=config.DEFAULT_ENCODING)
    print(f"Saved to {path}")
    return path
