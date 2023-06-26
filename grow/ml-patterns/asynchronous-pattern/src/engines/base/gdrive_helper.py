import concurrent.futures as executor
import io
import os
import re
from src.core.config import settings
from google.auth.exceptions import RefreshError
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.metadata",
]


class GoogleDriveHelper:
    def __init__(self, service_json=settings.GOOGLE_SA_FILE):
        try:
            service_json = os.path.abspath(service_json)
            has_client_secret = os.path.isfile(service_json)
            if not has_client_secret:
                url = "https://console.cloud.google.com/iam-admin/serviceaccounts"
                raise NameError(
                    f"{service_json} not found, please go to {url} to generate new file service key !"
                )

            credentials = service_account.Credentials.from_service_account_file(
                service_json, scopes=SCOPES
            )

            self.gdrive_service = build("drive", "v3", credentials=credentials)
        except RefreshError as exc:
            print(f"Couldn't refresh credentials because: {exc}.")

    def getIdFromUrl(self, url):
        regex = "(?<=/folders/)([\w-]+)|(?<=%2Ffolders%2F)([\w-]+)|(?<=/file/d/)([\w-]+)|(?<=%2Ffile%2Fd%2F)([\w-]+)|(?<=id=)([\w-]+)|(?<=id%3D)([\w-]+)"
        return re.search(regex, url)

    def download_file(self, file_id, output_path):
        try:
            status = False
            request = self.gdrive_service.files().get_media(
                fileId=file_id, supportsAllDrives=True
            )
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {output_path}: {int(status.progress() * 100)} %")

            print(output_path)
            with io.open(output_path, "wb") as f:
                fh.seek(0)
                f.write(fh.read())
            status = True
        except HttpError as error:
            print(f"An error occurred: {error}")
        finally:
            return status

    def download_file_with_multithread(self, files):
        try:
            if files:
                with executor.ThreadPoolExecutor() as exec:
                    for file in files:
                        exec.submit(file["gdrive_id"], file["file_name"])
        except HttpError as error:
            print(f"An error occurred: {error}")
