import os
import requests


def download_file_from_google_drive(file_id, destination):
    """Downloads a file from Google Drive using its file ID and saves it to the specified destination.

    Args:
        file_id (str): The ID of the file to download.
        destination (str): The path to save the downloaded file.

    Returns:
        bool: True if the download was successful, False otherwise.
    """

    URL = f"https://drive.google.com/uc?export=download&id={file_id}"

    try:
        session = requests.Session()
        response = session.get(URL, stream=True)
        token = get_confirm_token(response)

        if token:
            params = {'confirm': token}
            response = session.get(URL, params=params, stream=True)

        save_response_content(response, destination)

        return True

    except Exception as e:
        print(f"Download failed: {e}")
        return False


def get_confirm_token(response):
    """Extracts the confirmation token from the response if needed."""

    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    """Saves the content of the response to a file."""

    with open(destination, "wb") as f:
        for chunk in response.iter_content(1024):
            if chunk:  # Filter out keep-alive new chunks
                f.write(chunk)


if __name__ == "__main__":
    file_id = '1AjkMy6kjvYGgFKivRpXaxV5e6FTo7HxN'

    if download_file_from_google_drive(file_id, os.path.join('data', 'ted_talks.csv')):
        print("File downloaded successfully!")
    else:
        print("Download failed.")
