import pandas as pd
from pathlib import Path

from app.collectors import utils_collectors as utls
from app.collectors.reddit_collector import collect_reddit
from app.collectors.telegram_collector import collect_telegram

from app.src.text_preprocessing import preprocess_csv
from app.src.sentiment import analyze_sentiment

from config.config import PROCESSED_DIR


def collect_platform_data(platform, coin, period):
    """
    Returns path to saved CSV or None. Collect raw data and save to CSV.
    """

    if platform == "reddit":
        subs, limit, _ = utls.load_defaults("reddit")
        posts = collect_reddit(coin,subs["subreddits"],limit,period)

        return utls.save_to_csv(posts, "reddit", f"{coin}_{period}")
    
    if platform == "telegram":
        chans, limit, _ = utls.load_defaults("telegram")
        creds = utls.load_api("telegram")

        msgs = collect_telegram(coin,chans,limit,period,creds)

        return utls.save_to_csv(msgs, "telegram", f"{coin}_{period}")

    return None

def run_preprocessing(csv_path, platform):
    """Run text preprocessing and return soft file path."""
    soft_path, hard_path = preprocess_csv(csv_path, platform, processed_root=PROCESSED_DIR)
    return soft_path

def run_sentiment(soft_csv_path, platform):
    """Run sentiment scoring on preprocessed CSV."""
    return analyze_sentiment(soft_csv_path, processed_root=PROCESSED_DIR, source=platform)

def get_sample_reviews(csv_path):
    """Print three random posts (title + text)."""
    df = pd.read_csv(csv_path)

    print("\nSample Posts:\n")

    sample = df.sample(min(3, len(df)))

    for _, row in sample.iterrows():
        title = row.get("title", "(no title)")
        text = row.get("text", row.get("combined", "(no text)"))
        sep = '-' * 50
        print(f"{sep}\nTitle: {title}\nText: {text}\n")


def check_data_exists(platform, coin, period):
    """
    Try to find or download raw CSV.
    Return csv_path or None.
    """
    print(f"\nSearching for {coin} {period} data...")

    csv_path = collect_platform_data(platform, coin, period)

    if csv_path is None or not Path(csv_path).exists():
        print("No data found.")
        return None

    print(f"Data found: {csv_path}")
    return csv_path