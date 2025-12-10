"""
Main CLI entry point for the Crypto Sentiment Analyzer.
Platform → Coin → Period → Options (Sentiment / Reviews).
"""
from app.cli.menu import *
from app.cli.actions import check_data_exists,run_preprocessing
from app.cli.utils_cli import clear_screen


def main():
    """Main menu loop for the CLI."""
    clear_screen()
    start_menu()

    while True:
        platform = platform_menu().lower()
        coin = coin_menu().upper()
        period = date_menu()

        csv_path = check_data_exists(platform, coin, period)

        if csv_path is None:
            print("\nNo data available for this selection. Try different period.")
            input("Press ENTER to continue...")
            continue

        soft_path = run_preprocessing(csv_path, platform)

        result = options_menu(csv_path, soft_path, platform)
        if result == "restart":
            continue

if __name__ == "__main__":
    main()