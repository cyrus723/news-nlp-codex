"""Lesson 4: Compute the most common bigrams from tokenized news text."""

from ast import literal_eval
from collections import Counter
from pathlib import Path

import pandas as pd


INPUT_PATH = Path("outputs/tokenized_news.csv")
OUTPUT_PATH = Path("outputs/top_bigrams_overall.csv")
TOP_N = 30


def parse_tokens(tokens_text: str) -> list[str]:
    """Convert list-like token text from CSV into a Python list."""
    if pd.isna(tokens_text) or not str(tokens_text).strip():
        return []

    # tokens are stored as strings like "['word1', 'word2']" in CSV files.
    parsed = literal_eval(tokens_text)
    return parsed if isinstance(parsed, list) else []


def make_bigrams(tokens: list[str]) -> list[tuple[str, str]]:
    """Create bigrams (pairs of neighboring tokens) from one article."""
    # Example: ["new", "york", "city"] -> [("new", "york"), ("york", "city")]
    return list(zip(tokens, tokens[1:]))


def main() -> None:
    # 1) Load tokenized data from Lesson 2
    df = pd.read_csv(INPUT_PATH)

    # 2) Parse the existing tokens column from CSV text to Python lists
    df["tokens_list"] = df["tokens"].apply(parse_tokens)

    # 3) Build one combined list of bigrams from all articles
    all_bigrams: list[tuple[str, str]] = []
    for tokens in df["tokens_list"]:
        all_bigrams.extend(make_bigrams(tokens))

    # 4) Count bigram frequency and keep the top 30
    bigram_counts = Counter(all_bigrams)
    top_bigrams = bigram_counts.most_common(TOP_N)

    # 5) Save as a simple CSV with a readable bigram string
    top_bigrams_df = pd.DataFrame(top_bigrams, columns=["bigram_tuple", "count"])
    top_bigrams_df["bigram"] = top_bigrams_df["bigram_tuple"].apply(lambda pair: f"{pair[0]} {pair[1]}")
    top_bigrams_df = top_bigrams_df[["bigram", "count"]]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    top_bigrams_df.to_csv(OUTPUT_PATH, index=False)

    print("Bigram frequency calculation complete.")
    print(f"Input file: {INPUT_PATH}")
    print(f"Output file: {OUTPUT_PATH}")
    print(top_bigrams_df.head(10))


if __name__ == "__main__":
    main()
