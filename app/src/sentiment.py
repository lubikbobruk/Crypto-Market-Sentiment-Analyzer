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

''''
FOR CLI run
if __name__ == "__main__":
    from config.config import PROCESSED_DIR
    analyze_sentiment(
        csv_path="data/processed/Reddit/soft/xrp_2025-11-13_soft.csv",
        processed_root=PROCESSED_DIR,
        source="reddit"
    )
'''
    