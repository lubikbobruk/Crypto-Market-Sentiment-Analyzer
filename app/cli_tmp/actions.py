"""Pipeline actions for data collection and sentiment processing."""

import asyncio
from app.collectors import utils_collectors as utls
from app.collectors.reddit_collector import collect_reddit
from app.collectors.telegram_collector import (
    telegram_collect_async,
    collect_telegram)
from app.src.text_preprocessing import preprocess_csv
from app.src.sentiment import analyze_sentiment
from config.config import PROCESSED_DIR
from app.cli.telegram_auth import telegram_login, is_telegram_logged_in


def ensure_telegram_login():
    """Force Telegram login before running the program."""

    if not is_telegram_logged_in():
        print("Telegram is not authenticated yet.")
        print("You must log in once to enable Telegram data collection.\n")
        input("Press ENTER to begin Telegram login...")

        telegram_login()

        print("\nTelegram login complete. ✅\n")
        input("Press ENTER to continue...")


async def tg_collect(keyword, chans, limit, period, creds):
    return await telegram_collect_async(keyword, chans, limit, period, creds)


def run_telegram(keyword, period):
    """Streamlit Telegram wrapper."""
    chans, limit, _ = utls.load_defaults("telegram")
    creds = utls.load_api("telegram")

    try:
        msgs = asyncio.run(tg_collect(keyword, chans, limit, period, creds))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        msgs = loop.run_until_complete(
            tg_collect(keyword, chans, limit, period, creds))

    if not msgs:
        return None

    return utls.save_to_csv(msgs, "telegram", f"{keyword}_{period}")


def collect_platform_data(platform, coin, period):
    """Reddit/Telegram collector for CLI."""
    if platform == "reddit":
        subs, limit, _ = utls.load_defaults("reddit")
        posts = collect_reddit(
            coin,
            subs["subreddits"],
            limit,
            period)
        return utls.save_to_csv(posts, "reddit", f"{coin}_{period}")

    if platform == "telegram":
        chans, limit, _ = utls.load_defaults("telegram")
        creds = utls.load_api("telegram")
        msgs = collect_telegram(
            coin,
            chans,
            limit,
            period,
            creds)
        return utls.save_to_csv(msgs, "telegram", f"{coin}_{period}")

    return None


def run_preprocessing(csv_path, platform):
    """"Runs soft preprocessing."""
    soft, _ = preprocess_csv(
        csv_path,
        PROCESSED_DIR,
        platform)
    return soft


def run_sentiment(soft_csv_path, platform):
    return analyze_sentiment(
        soft_csv_path,
        PROCESSED_DIR,
        platform)
