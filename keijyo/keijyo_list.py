# ------------------------------------------------------------------------
#  keijyo_list.py
#  |--keijyo_list      - 画面作成
#  |--keijyo_list_exe  - 実行する、タスクオブジェクトを渡す
#  |--keijyo_list_task - タスク処理、sheetを作成、メール送信
#  keijyo_list_mod.py - sheetを作成
#  keijyo_list_sql.py - modを実行するときのsql
# ------------------------------------------------------------------------
import io
import sys
import json
from flask import request

from google.cloud import storage
import xlsxwriter
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from _mod import fs_config, mod_base, mod_que, mod_datetime, mod_gmail_api
from _mod_fis import mod_kei_nyu_pay, mod_section, mod_staff, mod_xlsxwriter
from keijyo import keijyo_list_mod


def keijyo_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    login_level = base_data["login_level_cd"]
    user_email = base_data["google_account_email"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "login_level": 0,
            "user_email": "",
            "keijyo_data": [],
            "section_data_all": [],
            "staff_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "login_level": login_level,
            "user_email": user_email,
            "keijyo_data": mod_kei_nyu_pay.mz_common_kei_sel(201904),
            "section_data_all": mod_section.mz_section_data_on(),
            "staff_data_all": mod_staff.mz_staff_data_all(),
        }
    return dic


def keijyo_list_exe():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
        }
    else:
        # task que
        que_project = fs_dic["project_name"]
        que_location = fs_dic["que_location"]
        que_id = fs_dic["que_id"]
        que_url = fs_dic["que_site"] + "/keijyo/list_task"
        que_body = {
            "js_obj": json.loads(request.data.decode("utf-8")),
            "project_name": fs_dic["project_name"],
            "bucket_name": fs_dic["upload_gcs_bucket"],
            "sender_email": fs_dic["sender_email"],
            "service": fs_dic["project_name"],
        }
        mod_que.mz_que(que_project, que_location, que_id, que_url, que_body)

        dic = {
            "level_error": level_error,
        }
    return dic


def keijyo_list_task():
    # obj
    obj = request.get_json()
    js_obj = obj["js_obj"]
    jwtg = js_obj["jwtg"]

    # value
    start_time = mod_datetime.mz_tnow("for_datetime")

    send_file_name = js_obj["send_file_name"]
    send_file_title_header = js_obj["send_file_title_header"]

    keijyo_date_int = js_obj["keijyo_date_int"]
    section_cd = js_obj["section_cd"]
    staff_cd = js_obj["staff_cd"]

    keijyo_date_str = js_obj["keijyo_date_str"]
    section_name = js_obj["section_name"]
    staff_name = js_obj["staff_name"]
    to_email = js_obj["send_email"]

    project_name = obj["project_name"]
    bucket_name = obj["bucket_name"]
    from_email = obj["sender_email"]
    service = obj["service"]

    # file create ---------------------------------------------------------------------------------

    # create in memory
    output = io.BytesIO()

    # workbook
    book = xlsxwriter.Workbook(output, {"in_memory": True})

    # staff1_cd, staff2_cd, staff3_cd
    sql_data_cnt_total = 0
    stf_kind = {
        "staff1": "担当1",
        "staff2": "担当2",
        "staff3": "担当3",
    }
    for stf_key, stf_value in stf_kind.items():
        sheet = book.add_worksheet(send_file_title_header + "_" + section_name + "_" + staff_name + "_" + stf_value)

        # cell format dic
        cf_dic = mod_xlsxwriter.mz_cf(book)

        # sheet title
        row = 0
        sheet, row = keijyo_list_mod.mz_title(sheet, row, cf_dic)

        # sheet data
        sheet, row, sql_data_cnt = keijyo_list_mod.mz_data(
            keijyo_date_int, section_cd, staff_cd, stf_key, sheet, row, cf_dic
        )
        sql_data_cnt_total += sql_data_cnt

    # close workbook
    book.close()

    # rewind the buffer
    output.seek(0)

    # gcs save file
    create_file = io.BytesIO(output.getvalue())
    file_name = "files/" + mod_datetime.mz_tnow("for_filename") + ".xlsx"
    client = storage.Client(project_name)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_file(create_file)

    # send email ----------------------------------------------------------------------------------

    # subject/body
    end_time = mod_datetime.mz_tnow("for_datetime")
    subject_data = send_file_name
    body_data = ""
    body_data += "\n"
    body_data += "処理　　：" + send_file_title_header + "\n"
    body_data += "計上月　：" + keijyo_date_str + "\n"
    body_data += "営業所　：" + section_name + "\n"
    body_data += "担当者　：" + staff_name + "\n"
    body_data += "件数　　：" + str(sql_data_cnt_total) + "\n"
    body_data += "\n"
    body_data += "処理開始時刻：" + start_time + "\n"
    body_data += "処理終了時刻：" + end_time + "\n"
    body_data += "service : " + service + "\n"
    body_data += "\n"

    # Gmail APIでメール送信
    service_gmail = mod_gmail_api.get_gmail_service()
    if service_gmail is not None:
        # マルチパートメッセージを作成
        message_obj = MIMEMultipart()
        message_obj["to"] = to_email
        message_obj["from"] = from_email
        message_obj["subject"] = subject_data

        # テキスト部分を追加
        text_part = MIMEText(body_data, "plain", "utf-8")
        message_obj.attach(text_part)

        # file from GCS
        blob = storage.Blob(file_name, bucket)
        content = blob.download_as_string()

        # 添付ファイルを追加
        attachment = MIMEBase("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        attachment.set_payload(content)
        encoders.encode_base64(attachment)
        # 日本語ファイル名対応：RFC 2231形式でエンコード
        attachment.add_header("Content-Disposition", "attachment", filename=("utf-8", "", send_file_name))
        message_obj.attach(attachment)

        # Base64エンコード
        raw_message = base64.urlsafe_b64encode(message_obj.as_bytes()).decode("utf-8")

        # メール送信
        try:
            result = service_gmail.users().messages().send(userId="me", body={"raw": raw_message}).execute()
            print(f"keijyo_list メール送信成功: {result}")
        except Exception as e:
            print(f"keijyo_list メール送信エラー: {e}")
            import traceback

            print(f"keijyo_list 詳細エラー: {traceback.format_exc()}")

    # base - level 2 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(2, jwtg, acc_page_name)

    # dic
    dic = {}
    return dic
