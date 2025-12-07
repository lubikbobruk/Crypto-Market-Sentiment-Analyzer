"""
Text preprocessing module for Crypto Market Sentiment Analyzer.
Provides two cleaning pipelines - Soft and Hard preprocessings.
Applies it to csv and creates 2 new csvs with processed text.
"""
from pathlib import Path
from .utils import *

def soft_clean(text: str) -> str:
    """
    Light preprocessing.
    Suitable for sentiment analysis (VADER).
    """
    if not text:
        return ""

    text = remove_urls(text)
    text = remove_mentions(text)
    text = normalize_whitespace(text)

    return text.strip()


def hard_clean(text: str) -> str:
    """
    Heavy preprocessing.
    Suitable for ML models, clustering, embeddings, topic modeling.
    """
    if not text:
        return ""

    text = text.lower()
    text = remove_urls(text)
    text = remove_mentions(text)
    text = remove_markdown(text)
    text = remove_non_ascii(text)
    text = remove_punctuation(text)
    text = normalize_whitespace(text)

    return text.strip()


def preprocess_csv(csv_path: str, source: str, processed_root: Path):
    """
    Combines title and text cols of csv files
    applies soft & hard cleaning and saves two files.
    """
    df = combine_csv(csv_path)

    filename = Path(csv_path).stem
    source = source.capitalize()

    # Build output directories
    soft_dir = processed_root / source / "soft"
    hard_dir = processed_root / source / "hard"
    soft_dir.mkdir(parents=True, exist_ok=True)
    hard_dir.mkdir(parents=True, exist_ok=True)

    # apply preprocessings
    df["clean_soft"] = df["combined"].apply(soft_clean)
    df["clean_hard"] = df["combined"].apply(hard_clean)

    soft_out = soft_dir / f"{filename}_soft.csv"
    hard_out = hard_dir / f"{filename}_hard.csv"

    df.to_csv(soft_out, index=False, encoding="utf-8-sig")
    df.to_csv(hard_out, index=False, encoding="utf-8-sig")

    print(f"Saved soft cleaned here: {soft_out}")
    print(f"Saved hard cleaned here: {hard_out}")

    return soft_out, hard_out