"""
Reddit data collector for Crypto Market Sentiment Analyzer.

Fetches Reddit submissions from the 'cryptocurrency' subreddit based on the given query and datetime. 
Saves them as a raw csv metadata into data/raw/reddit as <query>_<period>_<date>.csv
"""

import praw
from datetime import datetime, timezone
from app.collectors import utils_collectors as utls

def collect_reddit(query, subs, limit, period):
    creds = utls.load_api("reddit")
    reddit = praw.Reddit(**creds)

    posts = []
    print(f"Searching {len(subs)} subreddits for '{query}' ({period})...")

    for sub in subs:
        for submitions in reddit.subreddit(sub).search(query, sort="new", time_filter=period, limit=limit):
            text = (submitions.selftext or "").strip()
            if not utls.is_valid_post(text):
                continue
            posts.append({
                "subreddit": sub,
                "id": submitions.id,
                "title": submitions.title,
                "text": text,
                "author": str(submitions.author),
                "score": submitions.score,
                "datetime": datetime.fromtimestamp(submitions.created_utc, tz=timezone.utc).isoformat(),
                "link": f"https://reddit.com{submitions.permalink}",
            })
            
    print(f"Collected {len(posts)} posts")
    return posts