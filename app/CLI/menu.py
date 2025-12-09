from .utils_cli import *
from app.src.sentiment import *
from app.cli.actions import get_sample_reviews
from config.config import PROCESSED_DIR

def start_menu():
    clear_screen()
    print("Welcome to Crypto Sentiment Analyzer!")
    print("Analyze crypto sentiment from Reddit or Telegram.\n")
    wait("Press ENTER to start.")

def platform_menu():
    """Select valid platform."""
    while True:
        clear_screen()
        choices = {"1": "reddit", "2": "telegram"}
        selection = ask_choice("Choose a platform:", choices)

        if selection:
            return selection.lower()

        wait("Invalid choice. Try again.")


def coin_menu():
    """Select valid coin or a custom one."""
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

        selection = ask_choice("Choose a coin:", choices)

        if selection is None:
            wait("Invalid choice. Try again.")
            continue

        if selection == "Custom":
            while True:
                coin = input("\nEnter custom coin name: ").strip()
                if coin:
                    return coin.upper()
                wait("Invalid coin name. Try again.")

        return selection.upper()

def date_menu():
    """Select valid time period."""
    while True:
        clear_screen()
        choices = {
            "1": "day",
            "2": "week",
            "3": "month",
            "4": "year"
        }

        selection = ask_choice("Choose a time period:", choices)

        if selection:
            return selection

        wait("Invalid choice. Try again.")


def options_menu(csv_path, soft_path, platform):
    """
    Executes the selected action:
    1: Sentiment analysis + total score.
    2: Print reviews.
    3: Exit program.
    """

    while True:
        clear_screen()
        choices = {
            "1": "Get sentiment",
            "2": "Get reviews",
            "3": "Exit"
        }

        selection = ask_choice("What would you like to do?", choices)
        if not selection:
            wait("Invalid choice. Try again.")
            continue

        if selection == "Get sentiment":
            print("\nRunning sentiment analysis...\n")

            sentiment_csv = analyze_sentiment(
                soft_path,
                processed_root=PROCESSED_DIR,
                source=platform,
            )

            score = total_sentiment(sentiment_csv, platform)
            print(f"\nTotal sentiment score: {score:.3f}\n")
            trend = "positive" if score > 0 else "negative"
            print(f"\nThe market looks {trend}.")
            wait()
            continue

        # --- Option 2: sample reviews ---
        elif selection == "Get reviews":
            print("\n📰 Showing sample posts:")
            get_sample_reviews(csv_path)
            wait()
            continue

        # --- Option 3: exit program ---
        elif selection == "Exit":
            print("\n👋 Goodbye!")
            raise SystemExit(0)