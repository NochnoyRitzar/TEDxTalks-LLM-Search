import os
import requests


def download_dataset_from_gdrive(
    destination: str, file_id: str = "1AjkMy6kjvYGgFKivRpXaxV5e6FTo7HxN"
):
    """
    Downloads a file from Google Drive using its file ID and saves it to the specified destination.

    :param destination: The path to save the downloaded file.
    :param file_id: The ID of the file to download.
    """
    URL = f"https://drive.google.com/uc?export=download&id={file_id}"

    try:
        session = requests.Session()
        response = session.get(URL, stream=True)
        token = get_confirm_token(response)

        if token:
            params = {"confirm": token}
            response = session.get(URL, params=params, stream=True)

        save_response_content(response, destination)
        print("File downloaded successfully!")

    except Exception as e:
        print(f"Download failed: {e}")


def get_confirm_token(response):
    """Extracts the confirmation token from the response if needed."""

    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None


def save_response_content(response, destination):
    """Saves the content of the response to a file."""
    os.makedirs(os.path.split(destination)[0], exist_ok=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(1024):
            if chunk:  # Filter out keep-alive new chunks
                f.write(chunk)
