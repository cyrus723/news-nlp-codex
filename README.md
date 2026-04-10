# news-nlp-codex

## Lesson 1: Load and Clean Newspaper Articles

This first lesson introduces a beginner-friendly NLP workflow in `nlp_workflow.py`.
The script helps you practice core preprocessing steps before doing more advanced NLP.

### What the script does

- Loads a CSV file into a pandas DataFrame.
- Prints basic checks (shape, columns, missing values).
- Computes `article_length` as a simple word-count feature.
- Creates a `clean_text` column by lowercasing text, removing punctuation, and normalizing extra spaces.
- Saves the processed data so you can reuse it in later lessons.

### What file it reads

The script reads this input file:

- `data/sample_news.csv`

### What output file it creates

After processing, the script writes the cleaned dataset to:

- `outputs/cleaned_news.csv`

If the `outputs/` folder does not exist, the script creates it automatically.

### Why cleaning text matters

Raw text often includes punctuation, inconsistent capitalization, and messy spacing.
Cleaning makes text more consistent, which helps many NLP tasks work better and become easier to debug.

For example, cleaning is useful before:

- **Tokenization**: cleaner text leads to cleaner tokens.
- **Sentiment analysis**: consistent input reduces noise.
- **Topic analysis**: normalized text helps reveal clearer themes.

In short, text cleaning is a strong first step for almost every NLP pipeline.


### Lesson 2 note: token output format

In `outputs/tokenized_news.csv`, the `tokens` column is saved as **list-like text** because CSV files store plain text values.
For example, one row may look like:

- `['stocks', 'rose', 'investors', 'reacted']`

This is normal for beginner workflows. Later, you can convert this text back to a Python list when needed.
