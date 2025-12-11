"""This file is a container for global variables used in the project."""
from pathlib import Path

# Paths 
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SRC_DIR = PROJECT_ROOT / "app" / "src"
REDDIT_RAW = RAW_DIR / "reddit"
TELEGRAM_RAW = RAW_DIR / "telegram"

# Session files
SESSION_FILE = DATA_DIR / "telegram_cli.session"

# Lexicon directory
LEXICON_DIR = SRC_DIR / "lexicon"

# Config files
SECRETS_FILE = CONFIG_DIR / "secrets.yaml"
DEFAULTS_FILE = CONFIG_DIR / "collector_defaults.yaml"

# Runtime constants
DEFAULT_ENCODING = "utf-8-sig"
DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"

INVALID_MARKERS = {"[removed]", "[deleted]", "", None}

SENTIMENT_THRESHOLD = 0.05

# Streamlit UI constants

PLATFORM_LABELS = ["Reddit", "Telegram"]
PLATFORM_MAP = {"Reddit": "reddit", "Telegram": "telegram"}

COIN_OPTIONS = ["BTC", "ETH", "BNB", "SOL", "XRP", "Custom"]

PERIOD_LABELS = ["Last day", "Last week", "Last month", "Last year"]
PERIOD_MAP = {
    "Last day": "day",
    "Last week": "week",
    "Last month": "month",
    "Last year": "year",
}
