'''Provides a stack of different helper functions.'''

import yaml
from pathlib import Path

def load_settings(path="config/settings.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)