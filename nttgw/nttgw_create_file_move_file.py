import sys
import base64
from email.mime.text import MIMEText
from flask import request
from _mod import fs_config, mod_base, mod_datetime, mod_gmail_api

from googleapiclient.errors import HttpError
from nttgw.nttgw_create_file_service import get_drive_service


# ------------------------------------------------------------------------
# move file
# ------------------------------------------------------------------------
def move_file_task():
    # obj
    obj = request.get_json()
    js_obj = obj["js_obj"]
    jwtg = js_obj["jwtg"]

    # value
    # user_email = obj["user_email"]
    start_time = mod_datetime.mz_tnow("for_datetime")
    from_email = obj["sender_email"]
    to_email = obj["user_email"]
    service = obj["service"]

    # 結果
    move_file_result = move_file_main()

    # subject/body
    end_time = mod_datetime.mz_tnow("for_datetime")
    subject_data = "nttgw create file - move file"
    body_data = ""
    body_data += "\n"
    body_data += "結果：" + "\n"
    body_data += move_file_result + "\n\n"
    body_data += "処理開始時刻：" + start_time + "\n"
    body_data += "処理終了時刻：" + end_time + "\n"
    body_data += "service : " + service + "\n"
    body_data += "\n"

    # Gmail APIでメール送信
    service_gmail = mod_gmail_api.get_gmail_service()
    if service_gmail is not None:
        # メールメッセージを作成
        message_obj = MIMEText(body_data, "plain", "utf-8")
        message_obj["to"] = to_email
        message_obj["from"] = from_email
        message_obj["subject"] = subject_data

        # Base64エンコード
        raw_message = base64.urlsafe_b64encode(message_obj.as_bytes()).decode("utf-8")

        # メール送信
        try:
            result = service_gmail.users().messages().send(userId="me", body={"raw": raw_message}).execute()
            print(f"nttgw_move_file メール送信成功: {result}")
        except Exception as e:
            print(f"nttgw_move_file メール送信エラー: {e}")
            import traceback

            print(f"nttgw_move_file 詳細エラー: {traceback.format_exc()}")

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(9, jwtg, acc_page_name)

    # dic
    dic = {}
    return dic


def move_file_main():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # folder id
    UPLOAD_FOLDER_ID = fs_dic["upload_folder_id"]
    DAT_FOLDER_ID = fs_dic["dat_folder_id"]
    FEE_FOLDER_ID = fs_dic["fee_folder_id"]

    service = get_drive_service()
    move_file_result = ""
    file_name = ""
    dat_cnt = 0
    fee_cnt = 0

    # ファイルIDを取得
    query = f"'{UPLOAD_FOLDER_ID}' in parents and mimeType!='application/vnd.google-apps.folder'"
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

        # items list
        if not items:
            move_file_result = "ファイルが見つかりませんでした."
        else:
            for item in items:
                try:
                    file_id = item["id"]
                    file_name = item["name"]

                    if file_name.startswith(("561040060", "562040060")):
                        move_file_sub(service, file_id, DAT_FOLDER_ID)
                        dat_cnt += 1

                    elif file_name.startswith(("56104061", "56204061", "56104001", "56204001")):
                        move_file_sub(service, file_id, FEE_FOLDER_ID)
                        fee_cnt += 1

                except HttpError as error:
                    move_file_result = f"ファイルの移動でエラー発生: {file_name} {error}"

            # 結果OK
            move_file_result = f"ファイルの移動が成功しました." f" dat: {dat_cnt}件 fee: {fee_cnt}件"

    except HttpError as error:
        move_file_result = f"ファイルの移動でエラー発生: {file_name} {error}"

    return move_file_result


def move_file_sub(service, file_id, new_folder_id):
    try:
        # get file information
        file = (
            service.files()
            .get(
                fileId=file_id,
                fields="parents",
                supportsAllDrives=True,
            )
            .execute()
        )

        # move file
        previous_parents = ",".join(file.get("parents"))
        service.files().update(
            fileId=file_id,
            addParents=new_folder_id,
            removeParents=previous_parents,
            fields="id, parents",
            supportsAllDrives=True,
        ).execute()
    except HttpError as error:
        print(f"ERROR - move_file: {error}")
        raise
    return
