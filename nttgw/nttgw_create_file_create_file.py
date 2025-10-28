import os
import sys
from flask import request
from _mod import fs_config, mod_base, mod_datetime
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, To

import io
import tempfile
import csv
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from nttgw.nttgw_create_file_service import get_drive_service


# ------------------------------------------------------------------------
# create file
# ------------------------------------------------------------------------
def create_file_task():
    # init, firestore
    fs_dic = fs_config.fs_dic()

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
    create_file_result = create_file_main()

    # sendgrid subject/body
    end_time = mod_datetime.mz_tnow("for_datetime")
    subject_data = "nttgw create file - create file"
    body_data = ""
    body_data += "\n"
    body_data += "結果：" + "\n"
    body_data += create_file_result + "\n\n"
    body_data += "処理開始時刻：" + start_time + "\n"
    body_data += "処理終了時刻：" + end_time + "\n"
    body_data += "service : " + service + "\n"
    body_data += "\n"

    # sendgrid
    from_email = Email(from_email)
    to_email = To(to_email)
    subject = subject_data
    content = Content("text/plain", body_data)
    mail_con = Mail(from_email, to_email, subject, content)

    # send
    sg = sendgrid.SendGridAPIClient(fs_dic["sendgrid_api_key"])
    sg.send(mail_con)

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(9, jwtg, acc_page_name)

    # dic
    dic = {}
    return dic


def create_file_main():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # folder id
    # UPLOAD_FOLDER_ID = fs_dic["upload_folder_id"]
    DAT_FOLDER_ID = fs_dic["dat_folder_id"]
    # FEE_FOLDER_ID = fs_dic["fee_folder_id"]
    PROCESSED_FOLDER_ID = fs_dic["processed_folder_id"]
    RESULT_FOLDER_ID = fs_dic["result_folder_id"]
    # BACKUP_FOLDER_ID = fs_dic["backup_folder_id"]

    service = get_drive_service()
    create_file_result = ""
    file_name = ""
    all_data = []

    # ファイルIDを取得
    items = []
    query = f"'{DAT_FOLDER_ID}' in parents and mimeType!='application/vnd.google-apps.folder'"
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
        create_file_result = f"ファイルID取得エラー: {error}"

    # items list
    if not items:
        create_file_result = "ファイルが見つかりませんでした."
    else:
        for item in items:
            try:
                file_id = item["id"]
                file_name = item["name"]

                # convert and move
                if file_name.endswith(".dat"):
                    # convert file
                    content, error_message = convert_file(service, file_id, file_name)

                    if error_message != "":
                        return error_message

                    all_data.extend(content)

                    # move to proceed folder
                    move_to_processed_folder(service, file_id, PROCESSED_FOLDER_ID)

            except HttpError as error:
                create_file_result = f"エンコードエラー: {file_name} {error}"

        # 現在の日付を含むファイル名を作成
        today = mod_datetime.mz_tnow("for_date")
        file_name = f"nttgw-{today}.csv"

        # 結果csv作成
        create_all_csv(service, all_data, RESULT_FOLDER_ID, file_name)

        create_file_result = "ファイル作成が成功しました : " + file_name

    return create_file_result


# shift-jisからutf-8へエンコード
def convert_file(service, file_id, file_name):
    try:
        content = service.files().get_media(fileId=file_id).execute()

        # Shift_JISからUTF-8に変換
        decoded_content = content.decode("Shift_JIS", errors="ignore")
        utf8_content = decoded_content.encode("utf-8", errors="ignore")

        # StringIOオブジェクトを作成してCSVリーダーに渡す
        utf8_content_io = io.StringIO(utf8_content.decode("utf-8"))
        reader = csv.reader(utf8_content_io)
        data = [row for row in reader]
        return data, ""

    except HttpError as error1:
        return [], f"Google Drive APIでエラーが発生しました: {file_name} - {error1}"
    except UnicodeDecodeError as error2:
        return [], f"デコードエラーが発生しました: {file_name} - {error2}"
    except Exception as error3:
        return [], f"エラーが発生しました: {file_name} - {error3}"


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


# all csvを作成
def create_all_csv(service, all_data, folder_id, file_name):
    new_file_id = ""
    try:
        file_metadata = {
            "name": file_name,
            "mimeType": "text/csv",
            "parents": [folder_id],
        }

        # Create a new file
        file = service.files().create(body=file_metadata, supportsAllDrives=True).execute()
        new_file_id = file.get("id")

        # Convert data to CSV format
        csv_data = "\n".join([",".join(row) for row in all_data]).encode("utf-8")

        # Create a temporary file with the CSV data
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(csv_data)
            temp_file.flush()

        # Create MediaFileUpload object using the temporary file
        media = MediaFileUpload(
            temp_file.name,
            mimetype="text/csv",
            resumable=True,
        )

        # update the CSV data
        service.files().update(
            fileId=new_file_id,
            media_body=media,
            supportsAllDrives=True,
        ).execute()

        # Clean up the temporary file
        os.unlink(temp_file.name)

    except HttpError as error:
        print(f"all csv 作成エラー: {error}")
        raise
    return
