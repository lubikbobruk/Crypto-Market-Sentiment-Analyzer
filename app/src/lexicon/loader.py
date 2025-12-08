"""
Loads custom sentiment lexicon JSON files and merges them into one dictionary.
Used to extend VADER with specific words and emoji sentiment scores.
"""

import json
from pathlib import Path
from config.config import LEXICON_DIR

def get_lexicon(filename: str) -> dict:
    """Load JSON file."""
    full_path = LEXICON_DIR / filename

    if not full_path.exists():
        raise FileNotFoundError(f"Lexicon file not found: {full_path}")

    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_all_lexicons() -> dict:
    """Combine all lexicon overrides into one dict."""
    overrides = {}

    lex_files = [
        "crypto_positive.json",
        "crypto_negative.json",
        "crypto_neutral.json",
        "crypto_emojis.json"]

    for name in lex_files:
        overrides.update(get_lexicon(name))

    return overrides
