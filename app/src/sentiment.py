"""
Sentiment analysis using VADER for the Crypto Market Sentiment Analyzer.
"""

import pandas as pd
from pathlib import Path
from .utils import classify_sentiment, compute_sentiment

def analyze_sentiment(csv_path: str, processed_root: Path, source: str):
    """
    Runs VADER sentiment on a soft-preprocessed CSV.
    """
    df = pd.read_csv(csv_path)

    if "clean_soft" not in df.columns:
        raise ValueError("CSV must be soft preprocessed first.")

    # Compute VADER sentiment
    df["compound"] = df["clean_soft"].apply(compute_sentiment)
    df["sentiment"] = df["compound"].apply(classify_sentiment)

    source = source.capitalize()
    filename = Path(csv_path).stem.replace("_soft", "")
    out_dir = processed_root / source / "sentiment"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{filename}_sentiment.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"Sentiment computed and saved here: {out_path}")
    return out_path

def total_sentiment(csv_path: str, platform: str):
    """
    Compute total sentiment score weighted by post score(reddit) & views (telegram). 
    """
    df = pd.read_csv(csv_path)

    if "compound" not in df.columns:
        raise ValueError("CSV does not contain sentiment info.")

    if platform == "reddit" and "score" not in df.columns:
        raise ValueError("Reddit sentiment requires a score column for weighting.")

    if platform == "reddit":
        df["weight"] = df["score"].clip(lower=0)

        total_weight = df["weight"].sum()

        if total_weight == 0:
            simple_average = df["compound"].mean()
            return round(simple_average, 3)

        weighted_sum = (df["compound"] * df["weight"]).sum()
        weighted_average = weighted_sum / total_weight

        return round(weighted_average, 3)
    
    if platform == "telegram":
            if "views" not in df.columns:
                raise ValueError("Telegram messages must include a 'views' column.")

            df["weight"] = df["views"].fillna(0).clip(lower=1)

            total_weight = df["weight"].sum()

            if total_weight == 0:
                return round(df["compound"].mean(), 3)

            weighted_sum = (df["compound"] * df["weight"]).sum()
            weighted_avg = weighted_sum / total_weight

            return round(weighted_avg, 3)