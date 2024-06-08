import os
import ast
import pandas as pd


def save_dataframe_as_json(df: pd.DataFrame, output_file_path: str):
    """
    Save a pandas dataframe as a JSON file.

    :param df: The pandas dataframe to save as JSON file.
    :param output_file_path: The path to save JSON file.
    """
    if not os.path.exists(os.path.dirname(output_file_path)):
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    df.to_json(output_file_path, orient="records")
    print("Dataset downloaded and saved as JSON file.")


def load_df_from_gdrive(file_id: str = "1AjkMy6kjvYGgFKivRpXaxV5e6FTo7HxN") -> pd.DataFrame:
    """
    Loads a pandas dataframe from CSV file in Google Drive and stores it in-memory.

    :param file_id: The ID of the file to download.
    :return: A pandas dataframe.
    """
    URL = f"https://drive.google.com/uc?export=download&id={file_id}"
    try:
        df = pd.read_csv(
            URL,
            converters={
                'related_videos': ast.literal_eval,
                'speakers': ast.literal_eval,
                'subtitle_languages': ast.literal_eval,
                'topics': ast.literal_eval
            }
        )
    except Exception as e:
        print(f"Download failed: {e}")

    return df
