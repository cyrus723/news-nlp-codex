"""Beginner-friendly NLP workflow for newspaper articles."""

from pathlib import Path
import re

import pandas as pd


DATA_PATH = Path("data/sample_news.csv")
OUTPUT_PATH = Path("outputs/cleaned_news.csv")


def clean_text(text: str) -> str:
    """Lowercase text and remove punctuation/extra spaces."""
    if pd.isna(text):
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main() -> None:
    # 1) Load the CSV with pandas
    df = pd.read_csv(DATA_PATH)

    print("Dataset preview:")
    print(df.head(), end="\n\n")

    # Simple sanity checks for beginners
    print(f"DataFrame shape: {df.shape}")
    print(f"Column names: {list(df.columns)}")
    text_missing_rows = df["text"].isna().sum()
    print(f"Rows with missing text: {text_missing_rows}", end="\n\n")

    # 2) Compute missing values per column
    missing_values = df.isna().sum()
    print("Missing values by column:")
    print(missing_values, end="\n\n")

    # 3) Compute article length (word count) from the text column
    df["article_length"] = df["text"].fillna("").str.split().str.len()

    shortest_length = df["article_length"].min()
    longest_length = df["article_length"].max()
    print(f"Shortest article_length: {shortest_length}")
    print(f"Longest article_length: {longest_length}", end="\n\n")

    # 4) Create a clean_text column
    df["clean_text"] = df["text"].apply(clean_text)

    print("Updated dataset with article_length and clean_text:")
    print(df[["id", "title", "article_length", "clean_text"]])

    # 5) Save the processed DataFrame for later use
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved processed data to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
