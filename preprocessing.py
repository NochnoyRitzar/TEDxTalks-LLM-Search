import re
import os
from utilities import load_csv_data


def remove_bracketed_text(input_text):
    """Remove text inside brackets from input text."""
    # Define a regular expression pattern to find text inside round and square brackets
    pattern = r'[\(\[]([^()\[\]]*)[\)\]]'

    # Use re.sub to replace matches with an empty string
    result_text = re.sub(pattern, '', input_text)

    return result_text


def collapse_whitespace(input_text):
    # Define a regular expression pattern for repeated spaces
    pattern = r'\s+'

    # Replace repeated spaces with a single space
    result_text = re.sub(pattern, ' ', input_text)

    return result_text


def collapse_multiple_dots(input_text):
    # Define a regular expression pattern for repeated dots
    pattern = r'\.+'

    # Replace repeated dots with a single dot
    result_text = re.sub(pattern, '.', input_text)

    return result_text


def main():
    df = load_csv_data(os.path.join('data', 'raw', 'ted_talks.csv'))
    df = df[['title', 'summary', 'transcript']]

    df['summary'] = df['summary'].apply(remove_bracketed_text)
    df['summary'] = df['summary'].apply(collapse_whitespace)
    df['summary'] = df['summary'].apply(collapse_multiple_dots)

    df['transcript'] = df['transcript'].fillna('')
    df['transcript'] = df['transcript'].apply(remove_bracketed_text)
    df['transcript'] = df['transcript'].apply(collapse_whitespace)
    df['transcript'] = df['transcript'].apply(collapse_multiple_dots)

    df.to_csv(os.path.join('data', 'preprocessed', 'preprocessed_ted_talks.csv'), index=False)


if __name__ == "__main__":
    main()
