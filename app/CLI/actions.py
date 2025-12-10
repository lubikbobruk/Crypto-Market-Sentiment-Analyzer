# actions.py — CLEAN VERSION
import asyncio
import pandas as pd
from pathlib import Path

from app.collectors import utils_collectors as utls
from app.collectors.reddit_collector import collect_reddit
from app.collectors.telegram_collector import telegram_collect_async  # async collector

from app.src.text_preprocessing import preprocess_csv
from app.src.sentiment import analyze_sentiment

from config.config import PROCESSED_DIR


# ============================================================
# ASYNC TELEGRAM COLLECTOR (Streamlit-safe)
# ============================================================

async def _tg_async(keyword, chans, limit, period, creds):
    """Internal async wrapper."""
    return await telegram_collect_async(keyword, chans, limit, period, creds)


def run_telegram_safe(keyword: str, period: str):
    """
    Telegram collector wrapper that works inside Streamlit
    even when an event loop already exists.
    """
    chans, limit, _ = utls.load_defaults("telegram")
    creds = utls.load_api("telegram")

    try:
        msgs = asyncio.run(_tg_async(keyword, chans, limit, period, creds))
    except RuntimeError:
        # Streamlit already has its own event loop → we create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        msgs = loop.run_until_complete(_tg_async(keyword, chans, limit, period, creds))

    if not msgs:
        return None

    return utls.save_to_csv(msgs, "telegram", f"{keyword}_{period}")


# ============================================================
# CLASSIC COLLECTOR (CLI)
# ============================================================

def collect_platform_data(platform, coin, period):
    """
    Called by CLI.
    Returns raw CSV path.
    """

    if platform == "reddit":
        subs, limit, _ = utls.load_defaults("reddit")
        posts = collect_reddit(coin, subs["subreddits"], limit, period)
        return utls.save_to_csv(posts, "reddit", f"{coin}_{period}")

    if platform == "telegram":
        # CLI uses the synchronous collector inside telegram_collector
        from app.collectors.telegram_collector import collect_telegram

        chans, limit, _ = utls.load_defaults("telegram")
        creds = utls.load_api("telegram")

        msgs = collect_telegram(coin, chans, limit, period, creds)
        return utls.save_to_csv(msgs, "telegram", f"{coin}_{period}")

    return None


# ============================================================
# PREPROCESSING & SENTIMENT
# ============================================================

def run_preprocessing(csv_path, platform):
    """Run text preprocessing and return soft file path."""
    soft_path, hard_path = preprocess_csv(
        csv_path,
        platform,
        processed_root=PROCESSED_DIR
    )
    return soft_path


def run_sentiment(soft_csv_path, platform):
    """Run sentiment scoring on preprocessed CSV."""
    return analyze_sentiment(
        soft_csv_path,
        processed_root=PROCESSED_DIR,
        source=platform
    )


# ============================================================
# SAMPLE REVIEWS (CLI)
# ============================================================

def get_sample_reviews(csv_path):
    """Print 3 random posts."""
    df = pd.read_csv(csv_path)
    sample = df.sample(min(3, len(df)))

    print("\nSample Posts:\n")
    for _, row in sample.iterrows():
        title = row.get("title", "(no title)")
        text = row.get("text", row.get("combined", "(no text)"))
        print("-" * 50)
        print(f"Title: {title}\nText: {text}\n")


# ============================================================
# CHECK DATA EXISTS (CLI)
# ============================================================

def check_data_exists(platform, coin, period):
    """
    Try to collect & save raw CSV.
    Returns path or None.
    """
    print(f"\nSearching for {coin} {period} data...")

    csv_path = collect_platform_data(platform, coin, period)

    if csv_path is None or not Path(csv_path).exists():
        print("No data found.")
        return None

    print(f"Data found: {csv_path}")
    return csv_path
