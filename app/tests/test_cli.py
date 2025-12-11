"""
Tests for CLI utilities, menus and Telegram authentication.
"""

from pathlib import Path

from app.cli.utils_cli import ask_choice
from app.cli.menu import platform_menu, coin_menu, date_menu
from app.cli.telegram_auth import is_telegram_logged_in


# -------------------------------------------
# Helper for handling input with monkeypatch
# -------------------------------------------

def input_handler(monkeypatch, value):
    """Instead of taking an input, always return the given value."""
    monkeypatch.setattr("builtins.input", lambda *args: value)


def input_handler_sequence(monkeypatch, sequence):
    """Input handler that returns multiple values in order."""
    it = iter(sequence)
    monkeypatch.setattr("builtins.input", lambda *args: next(it))


# ----------------
# Utils CLI tests
# ----------------

def test_ask_choice(monkeypatch):
    """
    Takes inputs one by one using monkeypatch,
    and validates output. Test both main choices
    and aliases.
    """
    reddit_inputs = ["1", "r", "reddit", "red"]
    telegram_inputs = ["2", "telegram", "t"]

    choices = {
        "1": "reddit",
        "2": "telegram",
        "3": "facebook",
    }

    aliases = {
        "r": "1",
        "t": "2",
        "red": "1",
        "fb": "3",
    }

    # validate output sequentially
    input_handler_sequence(monkeypatch, reddit_inputs)

    for _ in reddit_inputs:
        assert ask_choice("empty", choices, aliases) == "reddit"

    input_handler_sequence(monkeypatch, telegram_inputs)

    for _ in telegram_inputs:
        assert ask_choice("empty", choices, aliases) == "telegram"


# -----------------
# Menus input test
# -----------------

def test_menus(monkeypatch):
    """Tests ask_choice on different choices and aliases."""
    input_handler(monkeypatch, "1")
    assert platform_menu() == "reddit"

    input_handler(monkeypatch, "telegram")
    assert platform_menu() == "telegram"

    input_handler(monkeypatch, "2")
    assert coin_menu() == "ETH"

    # First is a choice number, second is an inserted coin
    input_handler_sequence(monkeypatch, ["6", "doge"])
    assert coin_menu() == "DOGE"

    input_handler_sequence(monkeypatch, ["6", "anything"])
    assert coin_menu() == "ANYTHING"

    input_handler(monkeypatch, "3")
    assert date_menu() == "month"


# ---------------------
# Telegram log in test
# ---------------------

def test_is_logged_in(monkeypatch):
    fake_path = Path("test.session")

    # Replace the variable SESSION_FILE inside telegram_auth with fake_path.
    monkeypatch.setattr(
        "app.cli.telegram_auth.SESSION_FILE",
        fake_path,
    )

    assert is_telegram_logged_in() is False
