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

# Lexicon directory
LEXICON_DIR = SRC_DIR / "lexicon"

# Config files
SECRETS_FILE = CONFIG_DIR / "secrets.yaml"
DEFAULTS_FILE = CONFIG_DIR / "collector_defaults.yaml"

# Runtime constants
DEFAULT_ENCODING = "utf-8-sig"
DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"

INVALID_MARKERS = {"[removed]", "[deleted]", "", None}