"""
Reddit data collector for Crypto Market Sentiment Analyzer.

Fetches Reddit submissions from the 'cryptocurrency' subreddit based on the given query and datetime. 
Saves them as a raw csv metadata into data/raw/reddit as <query>_<period>_<date>.csv
"""

import praw
import yaml
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd

def load_reddit_api():
    """Load Reddit's credentials from config/secrets.yaml."""

    secrets_path = Path("config/secrets.yaml")
    if not secrets_path.exists():
        raise FileNotFoundError("Missing config/secrets.yaml credentials for reddit.")
    
    with open(secrets_path, "r", encoding="utf-8") as f:
        creds = yaml.safe_load(f)["reddit"] #extract reddit dict
    
    return praw.Reddit(
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        user_agent=creds["user_agent"]
    )

INVALID_MARKERS = {"[removed]", "[deleted]", ""}

def is_valid_submission(submission):
    """Check validity of both title and text."""
    title_valid = bool((submission.title).strip())
    text = (submission.selftext).strip()
    text_valid = text not in INVALID_MARKERS
    return text_valid and title_valid

def collect_reddit_posts(query: str, limit: int = 100, period: str = "week"):
    """Collect posts from multiple crypto-related subreddits."""
    reddit = load_reddit_api()
    subreddits = [
        "cryptocurrency", "CryptoMarkets", "CryptoCurrencyTrading",
        "bitcoin", "ethereum", "altcoin", "CryptoMoonShots", "crypto"
    ]
    posts = []
    max_attempts = limit * 3
    print(f"Searching subreddits {subreddits} for '{query}' ({period})...")

    for sub_name in subreddits:
        subreddit = reddit.subreddit(sub_name)
        for submission in subreddit.search(query, sort="new", time_filter=period, limit=max_attempts):
            if not is_valid_submission(submission):
                continue
            posts.append({
                "subreddit": sub_name,
                "id": submission.id,
                "title": (submission.title or "").strip(),
                "text": (submission.selftext or "").strip(),
                "score": submission.score,
                "author": str(submission.author) if submission.author else "[deleted]",
                "datetime": datetime.fromtimestamp(submission.created_utc, tz=timezone.utc).isoformat(),
                "link": "https://www.reddit.com" + submission.permalink,
            })
            if len(posts) >= limit:
                break
        if len(posts) >= limit:
            break

    print(f"Collected {len(posts)} valid posts across {len(subreddits)} subreddits.")
    return posts if posts else None


def save_reddit(posts, query: str, period: str):
    """Save list of posts to data/raw/reddit as <query>_<period>_<date>.csv and return the path."""
    if not posts:
        print("There are no posts to save.")
        return None
    path = Path(f"data/raw/reddit/{query.lower()}_{period}_{datetime.now().date()}.csv")
    pd.DataFrame(posts).to_csv(path, index=False)
    print(f"Saved posts into: {path}")
    return path

def reddit_collector_sample():
    print("=== Reddit Collector ===")
    query = input("Enter your query: ").strip()
    limit_str = input("Number of posts to fetch: ").strip()
    limit = int(limit_str) if limit_str.isdigit() else 50

    period = input("Select time range:\n" \
                "* last day (d)\n" \
                "* last week (w)\n" \
                "* last month (m)\n" \
                "* last year (y)\n" \
                "* all (a)\n"
                "--> ").strip().lower()
    
    period_map = {
    "d": "day",
    "w": "week",
    "m": "month",
    "y": "year",
    "a": "all"
    }

    period = period_map.get(period, period)

    if period not in ["day", "week", "month", "year", "all"]:
        period = "week"
    if period in ["d", "w", "m", "y", "a"]:
        period = period_map[period]
        
    try:
        posts = collect_reddit_posts(query, limit, period)
        save_reddit(posts, query, period)
    except Exception as e:
        print(f"Error: {e}")

reddit_collector_sample()