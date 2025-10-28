import os
import zipfile
import tempfile
from _mod import fs_config
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from nttgw.nttgw_create_file_service import get_drive_service


def main_upload_zip(zip_file):
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # folder id
    UPLOAD_FOLDER_ID = fs_dic["upload_folder_id"]

    try:
        service = get_drive_service()
        upload_zip_result = ""

        sub_upload_zip(service, zip_file, UPLOAD_FOLDER_ID)
        upload_zip_result = "成功！ ZIPファイルが解凍され、指定されたフォルダに追加されました"

    except Exception as e:
        upload_zip_result = f"失敗！ エラーが発生しました: {str(e)}"

    return upload_zip_result


def sub_upload_zip(service, zip_file, UPLOAD_FOLDER_ID):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_ref = zipfile.ZipFile(zip_file, "r")
            zip_ref.extractall(temp_dir)

            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_metadata = {
                        "name": file,
                        "parents": [UPLOAD_FOLDER_ID],
                    }
                    media = MediaFileUpload(file_path)

                    service.files().create(
                        body=file_metadata,
                        media_body=media,
                        fields="id",
                        supportsAllDrives=True,
                    ).execute()

        print(f"ZIPファイルが解凍され、フォルダID {UPLOAD_FOLDER_ID} に追加されました")

    except HttpError as error:
        print(f"エラーが発生しました: {error}")
        raise

    return
