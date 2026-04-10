"""Lesson 5: Assign simple topic labels using keyword matching."""

from ast import literal_eval
from pathlib import Path

import pandas as pd


INPUT_PATH = Path("outputs/tokenized_news.csv")
OUTPUT_PATH = Path("outputs/topic_labeled_news.csv")

# Beginner-friendly keyword lists for each topic label.
TOPIC_KEYWORDS = {
    "politics": {"election", "debate", "candidate", "candidates", "government", "policy", "vote"},
    "economy": {"market", "markets", "stocks", "inflation", "economy", "trade", "investors"},
    "sports": {"team", "goal", "championship", "match", "coach", "league", "final"},
    "crime": {"crime", "police", "arrest", "court", "suspect", "theft", "violence"},
    "health": {"health", "hospital", "doctor", "disease", "vaccine", "medicine", "virus"},
}

DEFAULT_TOPIC = "other"


def parse_tokens(tokens_text: str) -> list[str]:
    """Convert list-like token text from CSV into a Python list."""
    if pd.isna(tokens_text) or not str(tokens_text).strip():
        return []

    parsed = literal_eval(tokens_text)
    return parsed if isinstance(parsed, list) else []


def assign_topic(tokens: list[str]) -> str:
    """Assign one topic label by counting keyword matches per topic."""
    if not tokens:
        return DEFAULT_TOPIC

    token_set = {token.lower() for token in tokens}
    best_topic = DEFAULT_TOPIC
    best_score = 0

    for topic, keywords in TOPIC_KEYWORDS.items():
        score = len(token_set.intersection(keywords))

        # Keep the topic with the highest number of keyword matches.
        if score > best_score:
            best_topic = topic
            best_score = score

    return best_topic


def main() -> None:
    # 1) Load tokenized data from previous lesson
    df = pd.read_csv(INPUT_PATH)

    # 2) Parse the existing tokens column from CSV text to Python lists
    tokens_list = df["tokens"].apply(parse_tokens)

    # 3) Assign one topic label per article with simple keyword matching
    df["topic_label"] = tokens_list.apply(assign_topic)

    # 4) Save topic-labeled output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("Topic labeling complete.")
    print(f"Input file: {INPUT_PATH}")
    print(f"Output file: {OUTPUT_PATH}")
    print(df[["id", "tokens", "topic_label"]])


if __name__ == "__main__":
    main()
