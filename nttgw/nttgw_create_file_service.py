import os
import tempfile
from _mod import fs_config
from google.cloud import storage
from google.oauth2 import service_account
from googleapiclient.discovery import build


def get_drive_service():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # env
    PROJECT_NAME = fs_dic["project_name"]
    BUCKET_NAME = fs_dic["oauth_key_gcs_bucket"]
    BLOB_NAME = fs_dic["google_drive_oauth_key_json"]

    # GCS, service account key download
    client = storage.Client(project=PROJECT_NAME)
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(BLOB_NAME)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        blob.download_to_file(temp_file)
        temp_file.flush()

    # Authenticate and create Google Drive API client
    SERVICE_ACCOUNT_FILE = temp_file.name
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("drive", "v3", credentials=creds)

    # Clean up the temporary file
    os.unlink(temp_file.name)

    return service
