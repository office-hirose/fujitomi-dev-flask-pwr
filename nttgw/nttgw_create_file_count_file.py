from _mod import fs_config
from googleapiclient.errors import HttpError
from nttgw.nttgw_create_file_service import get_drive_service


def main_count_file():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    service = get_drive_service()
    count_file_result = []

    folder_ids = {
        "1.upload_folder": fs_dic["upload_folder_id"],
        "2.dat_folder": fs_dic["dat_folder_id"],
        "3.fee_folder": fs_dic["fee_folder_id"],
        "4.processed_folder": fs_dic["processed_folder_id"],
        "5.result_folder": fs_dic["result_folder_id"],
        "6.backup_folder": fs_dic["backup_folder_id"],
    }

    for folder_name, folder_id in folder_ids.items():
        cnt = count_files_in_folder(service, folder_id)
        # Create the folder URL using the folder ID
        folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
        count_file_result.append(
            {
                "folder_id": folder_id,
                "folder_name": folder_name,
                "file_cnt": cnt,
                "folder_url": folder_url,
            }
        )

    # trash url only
    trash_url = fs_dic["trash_url"]

    return count_file_result, trash_url


def count_files_in_folder(service, folder_id):
    file_cnt = 0
    items = []

    query = f"'{folder_id}' in parents and mimeType!='application/vnd.google-apps.folder'"
    try:
        results = (
            service.files()
            .list(
                q=query,
                fields="nextPageToken, files(id, name)",
                corpora="allDrives",
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
            )
            .execute()
        )
        items = results.get("files", [])
    except HttpError as error:
        return f"エラー・フォルダにファイルが存在しません: {error}"

    file_cnt = len(items)
    return file_cnt
