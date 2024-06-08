import os
import subprocess
import sys
from dotenv import load_dotenv
from src.pinecone_utils import create_index, populate_pinecone_db
from src.download_data import load_df_from_gdrive, save_dataframe_as_json
from src.preprocess_data import preprocess_raw_dataset

load_dotenv(".env")


def setup_environment():
    """
    Set up and activate a virtual environment.
    """
    if not os.path.exists("venv"):
        subprocess.run([sys.executable, "-m", "venv", "venv"])
    # Activate the virtual environment
    activate_script = (
        os.path.join("venv", "Scripts", "activate_this.py")
        if os.name == "nt"
        else os.path.join("venv", "bin", "activate_this.py")
    )
    with open(activate_script, "rb") as file:
        exec(file.read(), dict(__file__=activate_script))

    print("Virtual environment successfully setup and activated.")


def check_prerequisites():
    """
    Install necessary Python packages from the requirements.txt file into the activated virtual environment.
    """
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Prerequisites successfully installed.")


if __name__ == "__main__":
    setup_environment()
    check_prerequisites()

    raw_data_path = os.path.join("data", "raw", "ted_talks.json")
    if not os.path.exists(raw_data_path):
        df = load_df_from_gdrive()
        save_dataframe_as_json(df, raw_data_path)
    preprocess_raw_dataset(raw_data_path)

    create_index(dims=768, metric="cosine")
    populate_pinecone_db(
        os.path.join("data", "preprocessed", "preprocessed_ted_talks.json")
    )
