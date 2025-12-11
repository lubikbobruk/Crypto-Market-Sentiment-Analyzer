"""Menus for CLI visualization."""

from .utils_cli import *
from app.src.sentiment import *
from app.cli.utils_cli import get_sample_reviews
from config.config import PROCESSED_DIR

def start_menu():
    clear_screen()
    print("Welcome to Crypto Sentiment Analyzer!")
    print("Analyze crypto sentiment from Reddit or Telegram.\n")
    wait("Press ENTER to start.")

def platform_menu():
    while True:
        clear_screen()
        choices = {"1": "reddit", "2": "telegram"}

        aliases = {
            "r": "1",
            "reddit": "1",
            "t": "2",
            "telegram": "2"
        }

        selection = ask_choice("Choose a platform:", choices, aliases)
        return selection.lower()

def coin_menu():
    while True:
        clear_screen()

        choices = {
            "1": "BTC",
            "2": "ETH",
            "3": "BNB",
            "4": "SOL",
            "5": "XRP",
            "6": "Custom"
        }

        aliases = {
            "btc": "1", "b": "1",
            "eth": "2", "e": "2",
            "bnb": "3",
            "sol": "4",
            "xrp": "5",
            "custom": "6", "c": "6"
        }

        selection = ask_choice("Choose a coin:", choices, aliases)

        if selection == "Custom":
            while True:
                coin = input("Enter custom coin name: ").strip()
                if coin:
                    return coin.upper()
                wait("Invalid coin name. Try again.")

        return selection

def date_menu():
    while True:
        clear_screen()

        choices = {
            "1": "day",
            "2": "week",
            "3": "month",
            "4": "year"
        }

        aliases = {
            "d": "1", "day": "1",
            "w": "2", "week": "2",
            "m": "3", "month": "3",
            "y": "4", "year": "4"
        }

        selection = ask_choice("Choose a time period:", choices, aliases)
        return selection


def options_menu(csv_path, soft_path, platform):
    while True:
        clear_screen()

        choices = {
            "1": "Get sentiment",
            "2": "Get reviews",
            "3": "Go back",
            "4": "Exit"
        }

        aliases = {
            "s": "1", "sentiment": "1",
            "r": "2", "review": "2", "reviews": "2",
            "b": "3", "back": "3", "menu": "3",
            "e": "4", "exit": "4", "quit": "4"
        }

        selection = ask_choice("What would you like to do?", choices, aliases)

        if selection == "Get sentiment":
            clear_screen()
            print("Running sentiment analysis...\n")

            sentiment_csv = analyze_sentiment(soft_path,PROCESSED_DIR,platform)

            score = total_sentiment(sentiment_csv, platform)

            print(f"\nTotal sentiment score: {score:.3f}")
            trend = "positive" if score > 0 else "negative"
            print(f"The market looks {trend}.")

            wait()
            continue

        elif selection == "Get reviews":
            clear_screen()
            print("Showing sample posts:\n")
            get_sample_reviews(csv_path)
            wait()
            continue

        elif selection == "Exit":
            print("\nGoodbye! 👋")
            raise SystemExit(0)

        elif selection == "Go back":
            return "restart"