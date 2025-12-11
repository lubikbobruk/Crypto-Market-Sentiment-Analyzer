"""Helper functions for CLI implementation."""

from os import system, name
import pandas as pd
from pathlib import Path
from app.cli.actions import collect_platform_data


def get_sample_reviews(csv_path):
    """"Get at min 3 samples of reviews from csv and display it."""
    df = pd.read_csv(csv_path)
    sample = df.sample(min(3, len(df)))
    print("\nSample posts:\n")

    for _, row in sample.iterrows():
        print("-" * 50)
        print(f"Title: {row.get('title', '(no title)')}")
        print(f"Text: {row.get('text', row.get('combined', '(no text)'))}")


def check_data_exists(platform, coin, period):
    print(f"\nSearching for {coin} {period} data...")

    csv_path = collect_platform_data(platform, coin, period)

    if not csv_path or not Path(csv_path).exists():
        print("No data found.")
        return None

    print(f"Data found: {csv_path}")
    return csv_path


def clear_screen():
    """Clear terminal screen depending on os."""
    # if os is  windows
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def ask_choice(prompt: str, choices: dict, aliases: dict = None):
    """
    Flexible choice parser that supports numbers and texts.
    """

    while True:
        print(prompt)
        for key, val in choices.items():
            print(f"{key}) {val}")

        answer = input("> ").strip().lower()

        if answer in choices:
            return choices[answer]

        if aliases and answer in aliases:
            key = aliases[answer]
            return choices[key]

        for key, val in choices.items():
            if answer == val.lower():
                return val

        print("Invalid choice, try again.\n")


def wait(message: str = "\nPress ENTER to continue..."):
    """Pause before returning to menu."""
    input(message)
