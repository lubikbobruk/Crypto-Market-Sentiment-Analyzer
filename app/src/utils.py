'''Provides a stack of different helper functions.'''
import re
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentiment_core import get_analyzer

URL_PATTERN = re.compile(r"(https?://\S+|www\.\S+)")
MENTION_PATTERN = re.compile(r"@\w+")
MARKDOWN_LINK_PATTERN = re.compile(r"\[.*?\]\(.*?\)")
MULTISPACE_PATTERN = re.compile(r"\s+")

# ------------------------
# Text processing helpers
# ------------------------

def remove_urls(text: str) -> str:
    """Remove URLs."""
    return URL_PATTERN.sub("", text)

def remove_mentions(text: str) -> str:
    """Remove @mentions (Telegram/X/Reddit)."""
    return MENTION_PATTERN.sub("", text)

def remove_markdown(text: str) -> str:
    """
    Remove Markdown artifacts such as:
    [link](https://binance.com)
    """
    return MARKDOWN_LINK_PATTERN.sub("", text)

def remove_non_ascii(text: str) -> str:
    """Remove non-ASCII characters (emojis, non-latin symbols)."""
    return "".join(ch for ch in text if ch.isascii())

def remove_punctuation(text: str) -> str:
    """Remove punctuation characters."""
    return "".join(ch for ch in text if ch.isalnum() or ch.isspace())

def normalize_whitespace(text: str) -> str:
    """Collapse multiple whitespaces into a single space."""
    return MULTISPACE_PATTERN.sub(" ", text)


# -----------------------
# csv processing helpers
# -----------------------

def combine_csv(csv_path: str) -> pd.DataFrame:
    """
    Load a CSV and create a unified 'combined' field
    from text/title columns.
    """
    df = pd.read_csv(csv_path)

    has_title = "title" in df.columns
    has_text = "text" in df.columns

    # Fill NaN values with empty string
    if has_title:
        df["title"] = df["title"].fillna("").astype(str).str.strip()
    if has_text:
        df["text"] = df["text"].fillna("").astype(str).str.strip()

    if has_title and has_text:
        df["combined"] = (df["title"] + " " + df["text"]).str.strip()

    elif has_text:
        df["combined"] = df["text"]

    elif has_title:
        df["combined"] = df["title"]

    else:
        df["combined"] = ""

    return df

# ----------
# Sentiment 
# ----------

def classify_sentiment(score: float) -> str:
    """Interpret VADER compound score."""
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

def compute_sentiment(text: str) -> float:
    analyzer = get_analyzer()
    scores = analyzer.polarity_scores(str(text))
    return scores["compound"]