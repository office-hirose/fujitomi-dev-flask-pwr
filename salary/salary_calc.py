# ------------------------------------------------------------------------
#  salary_calc.py
#  |--salary_calc_start      - 画面作成
#  |--salary_calc_exe  - 実行する、タスクオブジェクトを渡す
#  |--salary_calc_task - タスク処理、計算、MySQLを更新、メール送信
#  salary_calc_mod.py - 計算、MySQLを更新
#  salary_calc_sql.py - 計算、MySQLを更新、modを実行するときのsql
# ------------------------------------------------------------------------
import sys
import json
import base64
from email.mime.text import MIMEText
from flask import request

from _mod import fs_config, mod_base, mod_que, mod_datetime, mod_gmail_api
from _mod_fis import mod_kei_nyu_pay, mod_staff

from salary import salary_calc_month


def salary_calc_start():
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
            "salary_date_data": [],
            "staff_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "login_level": login_level,
            "user_email": user_email,
            "salary_date_data": mod_kei_nyu_pay.mz_common_kei_sel(202504),
            "staff_data_all": mod_staff.mz_staff_data_all(),
        }
    return dic


def salary_calc_exe():
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
        que_url = fs_dic["que_site"] + "/salary/salary_calc_task"
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


def salary_calc_task():
    # obj
    obj = request.get_json()
    js_obj = obj["js_obj"]
    jwtg = js_obj["jwtg"]

    # value
    start_time = mod_datetime.mz_tnow("for_datetime")

    send_email_title = js_obj["send_email_title"]

    salary_date_int = js_obj["salary_date_int"]
    salary_date_str = js_obj["salary_date_str"]
    to_email = js_obj["send_email"]

    # project_name = obj["project_name"]
    from_email = obj["sender_email"]
    service = obj["service"]

    # calc ----------------------------------------------------------------------------------------

    salary_calc_month.mz_update(salary_date_int)

    # send email ----------------------------------------------------------------------------------

    # subject/body
    end_time = mod_datetime.mz_tnow("for_datetime")
    subject_data = send_email_title
    body_data = ""
    body_data += "\n"
    body_data += "処理　　：" + send_email_title + "\n"
    body_data += "計算月　：" + salary_date_str + "\n"
    body_data += "\n"
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
            print(f"salary_calc メール送信成功: {result}")
        except Exception as e:
            print(f"salary_calc メール送信エラー: {e}")
            import traceback

            print(f"salary_calc 詳細エラー: {traceback.format_exc()}")

    # base - level 2 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(2, jwtg, acc_page_name)

    # dic
    dic = {}
    return dic
