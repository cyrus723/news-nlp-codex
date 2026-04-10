"""Lesson 3: Find the most frequent tokens across all newspaper articles."""

from ast import literal_eval
from collections import Counter
from pathlib import Path

import pandas as pd


INPUT_PATH = Path("outputs/tokenized_news.csv")
OUTPUT_PATH = Path("outputs/top_words_overall.csv")
TOP_N = 30


def parse_tokens(tokens_text: str) -> list[str]:
    """Convert list-like token text from CSV into a Python list."""
    if pd.isna(tokens_text) or not str(tokens_text).strip():
        return []

    # tokens are stored as text like "['word1', 'word2']"
    parsed = literal_eval(tokens_text)
    return parsed if isinstance(parsed, list) else []


def main() -> None:
    # 1) Load tokenized data from Lesson 2
    df = pd.read_csv(INPUT_PATH)

    # 2) Convert tokens column from CSV text to Python lists
    df["tokens_list"] = df["tokens"].apply(parse_tokens)

    # 3) Flatten all tokens into one list
    all_tokens: list[str] = []
    for tokens in df["tokens_list"]:
        all_tokens.extend(tokens)

    # 4) Count token frequency and keep the top 30
    token_counts = Counter(all_tokens)
    top_words = token_counts.most_common(TOP_N)

    # 5) Save results to CSV
    top_words_df = pd.DataFrame(top_words, columns=["token", "count"])
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    top_words_df.to_csv(OUTPUT_PATH, index=False)

    print("Top words calculation complete.")
    print(f"Input file: {INPUT_PATH}")
    print(f"Output file: {OUTPUT_PATH}")
    print(top_words_df.head(10))


if __name__ == "__main__":
    main()
