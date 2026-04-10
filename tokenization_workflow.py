"""Lesson 2: Tokenize cleaned newspaper text and remove stopwords."""

from pathlib import Path

import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize


INPUT_PATH = Path("outputs/cleaned_news.csv")
OUTPUT_PATH = Path("outputs/tokenized_news.csv")

# Small fallback list for offline environments where NLTK stopwords data is unavailable.
FALLBACK_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he",
    "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were", "will", "with"
}


def get_stopwords() -> set[str]:
    """Return English stopwords from NLTK, or a small fallback set if unavailable."""
    try:
        return set(stopwords.words("english"))
    except LookupError:
        print("NLTK stopwords data not found locally. Using a small fallback stopword list.")
        return FALLBACK_STOPWORDS


def tokenize_without_stopwords(text: str, stop_words: set[str]) -> list[str]:
    """Tokenize text and remove English stopwords."""
    if pd.isna(text) or not str(text).strip():
        return []

    # wordpunct_tokenize splits text into tokens without extra downloads.
    tokens = wordpunct_tokenize(text)

    # Keep alphabetic tokens and remove common stopwords.
    filtered_tokens = [
        token for token in tokens if token.isalpha() and token.lower() not in stop_words
    ]
    return filtered_tokens


def main() -> None:
    # 1) Load the cleaned data from Lesson 1
    df = pd.read_csv(INPUT_PATH)

    # 2) Build an English stopword set
    stop_words = get_stopwords()

    # 3) Create a new tokens column from clean_text
    df["tokens"] = df["clean_text"].apply(lambda text: tokenize_without_stopwords(text, stop_words))

    # 4) Count how many tokens each article has
    df["token_count"] = df["tokens"].apply(len)

    # 5) Save the tokenized output for the next lesson
    # 4) Save the tokenized output for the next lesson
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("Tokenization complete.")
    print(f"Input file: {INPUT_PATH}")
    print(f"Output file: {OUTPUT_PATH}")
    print(df[["id", "clean_text", "tokens", "token_count"]].head())
    print(df[["id", "clean_text", "tokens"]].head())


if __name__ == "__main__":
    main()
