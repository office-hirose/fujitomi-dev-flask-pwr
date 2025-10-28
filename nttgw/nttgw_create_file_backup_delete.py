from _mod import fs_config
from googleapiclient.errors import HttpError
from nttgw.nttgw_create_file_service import get_drive_service


# ------------------------------------------------------------------------
# バックアップと削除
# ------------------------------------------------------------------------
def main_backup_delete():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # folder id
    # UPLOAD_FOLDER_ID = fs_dic["upload_folder_id"]
    DAT_FOLDER_ID = fs_dic["dat_folder_id"]
    FEE_FOLDER_ID = fs_dic["fee_folder_id"]
    PROCESSED_FOLDER_ID = fs_dic["processed_folder_id"]
    RESULT_FOLDER_ID = fs_dic["result_folder_id"]
    BACKUP_FOLDER_ID = fs_dic["backup_folder_id"]

    service = get_drive_service()
    backup_delete_result = []
    try:
        backup_cnt = move_files_to_backup_folder(service, RESULT_FOLDER_ID, BACKUP_FOLDER_ID)
        delete_cnt = send_files_to_trash(
            service,
            [DAT_FOLDER_ID, FEE_FOLDER_ID, PROCESSED_FOLDER_ID, RESULT_FOLDER_ID],
        )

        backup_delete_result.append({"exe_cat": "バックアップ", "file_cnt": f"{backup_cnt} 件"})
        backup_delete_result.append({"exe_cat": "ゴミ箱へ移動", "file_cnt": f"{delete_cnt} 件"})
    except Exception as error:
        backup_delete_result.append({"error": f"バックアップまたは削除処理中にエラーが発生しました: {error}"})

    return backup_delete_result


# バックアップフォルダに移動
def move_files_to_backup_folder(service, folder_id, backup_folder_id):
    backup_cnt = 0
    try:
        query = f"'{folder_id}' in parents and mimeType!='application/vnd.google-apps.folder'"
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

        for item in items:
            file_id = item["id"]
            try:
                move_to_processed_folder(service, file_id, backup_folder_id)
                backup_cnt += 1
            except HttpError as error1:
                print(f"Backup エラー :{error1}")
                raise

    except Exception as error2:
        print(f"バックアップ処理中にエラーが発生しました: {error2}")
        raise

    return backup_cnt


# 処理済みのファイルを別のフォルダに移動
def move_to_processed_folder(service, file_id, destination_folder_id):
    try:
        file = (
            service.files()
            .get(
                fileId=file_id,
                fields="parents",
                supportsAllDrives=True,
            )
            .execute()
        )
    except HttpError as error:
        print(f"ファイル読み取りエラー: {error}")
        file = None
        raise

    if file:
        previous_parents = ",".join(file.get("parents"))
        try:
            service.files().update(
                fileId=file_id,
                addParents=destination_folder_id,
                removeParents=previous_parents,
                fields="id, parents",
                supportsAllDrives=True,
            ).execute()
        except HttpError as error:
            print(f"ファイル移動エラー : {error}")
            raise
    else:
        print("エラーファイルが見つかりません")
        raise
    return


# 処理済ファイルをゴミ箱へ
def send_files_to_trash(service, folder_ids):
    delete_cnt = 0
    try:
        for folder_id in folder_ids:
            query = f"'{folder_id}' in parents and mimeType!='application/vnd.google-apps.folder'"
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

            for item in items:
                file_id = item["id"]
                try:
                    service.files().update(
                        fileId=file_id,
                        body={"trashed": True},
                        supportsAllDrives=True,
                    ).execute()
                    delete_cnt += 1

                except HttpError as error1:
                    print(f"Delete エラー :{error1}")
                    raise

    except Exception as error2:
        print(f"削除処理中にエラーが発生しました: {error2}")
        raise

    return delete_cnt
