import io
from datetime import datetime

from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from googleapiclient.discovery import build


def init_gdrive_service(credentials_file):
    """
    Initialize the Google Drive API service using a service account.

    Arguments:
    - str credentials_file: Path to the service account credentials JSON file.

    Returns:
    - drive_service: An authorized Google Drive API service instance.
    """
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)


def list_files(drive_service, folder_id):
    """
    List all files in a specified Google Drive folder.
    Arguments:
    - drive_service: An authorized Google Drive API service instance.
    - str folder_id: The ID of the Google Drive folder to list files from.
    Returns:
    - list: A list of files in the specified folder.
    """
    query = f"'{folder_id}' in parents and trashed = false"
    response = (
        drive_service.files()
        .list(
            q=query,
            spaces="drive",
            fields="files(id, name, mimeType, parents)",
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
        )
        .execute()
    )
    return response.get("files", [])


def download_file(drive_service, file_id, filename):
    """
    Download a file from Google Drive.
    Arguments:
    - drive_service: An authorized Google Drive API service instance.
    - str file_id: The ID of the file to download.
    - str filename: The local path where the file will be saved.
    """
    request = drive_service.files().get_media(fileId=file_id)
    with io.FileIO(filename, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()


def create_timestamped_folder(drive_service, parent_folder_id):
    """
    Create a timestamped folder in Google Drive.
    Arguments:
    - drive_service: An authorized Google Drive API service instance.
    - str parent_folder_id: The ID of the parent folder where the new folder will be created.
    Returns:
    - str: The ID of the newly created folder.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_metadata = {
        "name": timestamp,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_folder_id],
    }
    folder = (
        drive_service.files()
        .create(body=folder_metadata, fields="id", supportsAllDrives=True)
        .execute()
    )
    return folder["id"]


def move_file(drive_service, file_id, src_folder_id, dest_folder_id):
    """
    Move a file from one folder to another in Google Drive.
    Arguments:
    - drive_service: An authorized Google Drive API service instance.
    - str file_id: The ID of the file to move.
    - str src_folder_id: The ID of the source folder.
    - str dest_folder_id: The ID of the destination folder.
    """
    file = (
        drive_service.files()
        .update(
            fileId=file_id,
            addParents=dest_folder_id,
            removeParents=src_folder_id,
            fields="id, parents",
            supportsAllDrives=True,
        )
        .execute()
    )
