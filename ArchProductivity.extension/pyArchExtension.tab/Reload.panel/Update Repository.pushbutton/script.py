__title__ = "Update \nRepository"
__doc__ = """Version: 1.1
Date: 05.04.2024
_____________________________________________________________________
Description:
Download the latest update of repository.
_____________________________________________________________________
How-to:

_____________________________________________________________________
Last update:
- [05.04.2024] - 1.1 RELEASE
_____________________________________________________________________
Author: Luis Ibanez"""

import os
import requests


def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/drive/folders/1xj3K41mkJKQZk2Aw2cBEsTVXHnPGOVHY?usp=drive_link" + file_id

    session = requests.Session()
    response = session.get(URL, stream=True)

    save_response_content(response, destination)


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)


def download_from_link(link, destination_folder):
    try:
        file_id = extract_file_id(link)
        file_name = "pyarchextension"  # Update this with the actual file name

        destination_path = os.path.join(destination_folder, file_name)
        download_file_from_google_drive(file_id, destination_path)

    except ValueError as e:
        print(f"Error: {e}")


def extract_file_id(google_drive_link):
    try:
        start_idx = google_drive_link.find("id=")
        if start_idx == -1:
            raise ValueError("Invalid Google Drive link")

        start_idx += 3
        end_idx = google_drive_link.find("&", start_idx)
        if end_idx == -1:
            end_idx = None

        return google_drive_link[start_idx:end_idx]

    except Exception as e:
        raise ValueError("Invalid Google Drive link") from e


if __name__ == "__main__":
    google_drive_link = "https://drive.google.com/drive/folders/1xj3K41mkJKQZk2Aw2cBEsTVXHnPGOVHY?usp=drive_link"  # Update this link
    destination_folder = "C:\Users\ibanezl3110\OneDrive - ARCADIS\Desktop\Test Download gdrive"  # Update this path

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    download_from_link(google_drive_link, destination_folder)
