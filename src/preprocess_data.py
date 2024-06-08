import re
import os
from ast import literal_eval
import pandas as pd


def remove_bracketed_text(input_text):
    """

    :param input_text:
    :return:
    """
    # Regex to find text inside round and square brackets
    pattern = r"[\(\[]([^()\[\]]*)[\)\]]"
    result_text = re.sub(pattern, "", input_text)

    return result_text


def remove_special_chars(input_text):
    """
    Remove special characters from input text.
    :param input_text:
    :return:
    """
    result_text = re.sub(r"\r|\n", "", input_text)

    return result_text


def collapse_multiple_chars(input_text):
    """
    Collapse multiple occurrences of characters in input text.
    :param input_text:
    :return:
    """
    # Collapse repeating whitespaces
    result_text = re.sub(r"\s+", " ", input_text)
    # Collapse repeating dashes
    result_text = re.sub(r"\-+", "-", result_text)
    # Collapse repeating dots
    result_text = re.sub(r"\.+", ".", result_text)

    return result_text


def clean_text_column(input_text):
    """
    Combine text cleaning functions.
    :param input_text: text to clean
    :return: cleaned text
    """
    input_text = remove_special_chars(input_text)
    input_text = remove_bracketed_text(input_text)
    input_text = collapse_multiple_chars(input_text)

    return input_text


def process_rel_videos_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts lists in 'related_videos' column to comma-separated strings.

    :param df: DataFrame with 'related_videos' lists.
    :return: DataFrame with updated 'related_videos' as strings.
    """
    df["related_videos"] = df["related_videos"].apply(lambda x: ", ".join(x))

    return df


def process_speakers_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts and splits 'speakers' data into 'speakers_names' and 'speakers_occupation' columns, then removes
    'speakers' column.

    :param df: DataFrame with 'speakers' data.
    :return: Updated DataFrame with new columns and without 'speakers'.
    """
    speakers_list = df["speakers"].to_list()
    speakers_names_list = []
    speakers_occupation_list = []
    for data in speakers_list:
        names_str = ", ".join([item["name"] for item in data])
        occupations_str = ", ".join([item["occupation"] for item in data])
        speakers_names_list.append(names_str)
        speakers_occupation_list.append(occupations_str)
    df["speakers_names"] = speakers_names_list
    df["speakers_occupation"] = speakers_occupation_list
    df.drop(columns=["speakers"], inplace=True)

    return df


def process_sub_lang_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts 'subtitle_languages' from list of dictionaries to comma-separated strings.

    :param df: DataFrame with 'subtitle_languages'.
    :return: DataFrame with 'subtitle_languages' as strings.
    """
    subtitle_list = df["subtitle_languages"].to_list()
    languages_list = []
    for data in subtitle_list:
        languages_str = ", ".join([item["name"] for item in data])
        languages_list.append(languages_str)
    df["subtitle_languages"] = languages_list

    return df


def process_topics_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Splits 'topics' data into 'topics_names' and 'topics_ids' columns, then removes 'topics'.

    :param df: DataFrame with 'topics' data.
    :return: Updated DataFrame with new columns and without 'topics'.
    """
    topics_list = df["topics"].to_list()
    topics_ids_list = []
    topics_names_list = []
    for data in topics_list:
        ids_str = ", ".join([item["id"] for item in data])
        names_str = ", ".join([item["name"] for item in data])
        topics_ids_list.append(ids_str)
        topics_names_list.append(names_str)
    df["topics_names"] = topics_names_list
    df["topics_ids"] = topics_ids_list
    df.drop(columns=["topics"], inplace=True)

    return df


def preprocess_raw_dataset(raw_csv_path: str, output_dir: str = os.path.join("data", "preprocessed")):
    df = pd.read_csv(
        os.path.join(raw_csv_path),
        converters={
            "related_videos": literal_eval,
            "speakers": literal_eval,
            "subtitle_languages": literal_eval,
            "topics": literal_eval,
        },
    )

    df = process_rel_videos_column(df)
    df = process_speakers_column(df)
    df = process_topics_column(df)
    df = process_sub_lang_column(df)

    df["summary"] = df["summary"].apply(clean_text_column)

    df["transcript"] = df["transcript"].fillna("")
    df["transcript"] = df["transcript"].apply(clean_text_column)

    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(os.path.join(output_dir, "preprocessed_ted_talks.csv"), index=False)

    print("Data successfully preprocessed and saved.")
