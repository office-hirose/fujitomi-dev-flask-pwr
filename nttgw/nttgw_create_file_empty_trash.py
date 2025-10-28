from googleapiclient.errors import HttpError
from nttgw.nttgw_create_file_service import get_drive_service


# ------------------------------------------------------------------------
# GoogleDrive ゴミ箱を空にする
# ------------------------------------------------------------------------
def main_empty_trash():
    service = get_drive_service()
    empty_trash_result = []

    try:
        file_cnt = sub_empty_trash(service)
        empty_trash_result.append({"exe_cat": "ゴミ箱を空にする・成功", "file_cnt": f"{file_cnt} 件"})
    except Exception as error:
        empty_trash_result.append(
            {
                "exe_cat": "ゴミ箱を空にする・エラー",
                "file_cnt": f"ゴミ箱を空にする処理中にエラーが発生しました: {error}",
            }
        )

    return empty_trash_result


# 実行する
def sub_empty_trash(service):
    file_cnt = 0
    try:
        query = "trashed = true"
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
                service.files().delete(fileId=file_id, supportsAllDrives=True).execute()
                file_cnt += 1
            except HttpError as error:
                print(f"ファイル削除エラー : {error}")
                raise

    except HttpError as error:
        print(f"ゴミ箱を空にする際にエラーが発生しました: {error}")
        raise

    return file_cnt
