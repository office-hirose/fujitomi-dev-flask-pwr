# -------------------------------------------------------------------
#  fee_cre_month.py
#  |--fee_cre_month           - 画面作成
#  |--fee_cre_month_exe       - 実行する、タスクオブジェクトを渡す
#  |--fee_cre_month_task      - タスク処理、作成構築、作成終了後のメール送信
#  fee_cre_month_keiri_mod.py - 作成実行
#  fee_cre_month_keiri_sql.py       - 実行sql
# -------------------------------------------------------------------
import sys
import json
import base64
from email.mime.text import MIMEText
from flask import request
from _mod import fs_config, mod_base, mod_que, mod_datetime, mod_gmail_api
from _mod_fis import mod_kei_nyu_pay, mod_staff, mod_task_sta

from fee import fee_cre_month_keiri_mod


def fee_cre_month():
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
            "nyu_data": [],
            "staff_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "login_level": login_level,
            "user_email": user_email,
            "nyu_data": mod_kei_nyu_pay.mz_common_nyu_sel(201904),
            "staff_data_all": mod_staff.mz_staff_data_all(),
        }
    return dic


def fee_cre_month_exe():
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
            "send_file_name_datetime": "",
            "task_sta": "",
            "task_start_time": "",
            "task_exe_user": "",
        }
    else:
        # send_file_name_datetime
        send_file_name_datetime = mod_datetime.mz_tnow("for_filename_yyyy_mmdd_hhmm")

        # 処理実行中かチェックする
        task_sta, task_start_time, task_exe_user = mod_task_sta.mz_task_sta_chk("fee_cre_keiri")
        # task que
        if task_sta == "end":
            que_project = fs_dic["project_name"]
            que_location = fs_dic["que_location"]
            que_id = fs_dic["que_id"]
            que_url = fs_dic["que_site"] + "/fee/cre_month_keiri_task"

            que_body = {
                "js_obj": json.loads(request.data.decode("utf-8")),
                "project_name": fs_dic["project_name"],
                "bucket_name": fs_dic["upload_gcs_bucket"],
                "sender_email": fs_dic["sender_email"],
                "service": fs_dic["project_name"],
                "send_file_name_datetime": send_file_name_datetime,
            }
            mod_que.mz_que(que_project, que_location, que_id, que_url, que_body)

        dic = {
            "level_error": level_error,
            "send_file_name_datetime": send_file_name_datetime,
            "task_sta": task_sta,
            "task_start_time": mod_datetime.mz_dt2str_yymmddhhmm_hyphen(task_start_time),
            "task_exe_user": task_exe_user,
        }
    return dic


def fee_cre_month_task():
    # obj
    obj = request.get_json()
    js_obj = obj["js_obj"]
    jwtg = js_obj["jwtg"]

    # value
    start_time = mod_datetime.mz_tnow("for_datetime")
    user_email = js_obj["send_email"]

    # send_file_name = (
    #     js_obj["send_file_name"] + "-" + obj["send_file_name_datetime"] + ".xlsx"
    # )
    send_file_title_header = js_obj["send_file_title_header"]

    nyu_date_int = js_obj["nyu_date_int"]
    nyu_date_str = js_obj["nyu_date_str"]
    # project_name = obj["project_name"]
    # bucket_name = obj["bucket_name"]
    from_email = obj["sender_email"]
    to_email = js_obj["send_email"]
    service = obj["service"]

    # title_name = send_file_title_header + "-" + nyu_date_str + "-全社"

    # create data

    # task_sta set
    task_sta = "working"
    task_name = "fee_cre_keiri"
    task_exe_user = user_email
    mod_task_sta.mz_task_sta_write(task_sta, task_name, task_exe_user)

    # delete
    fee_cre_month_keiri_mod.mz_del(nyu_date_int)

    # create, insert
    exe_cnt = fee_cre_month_keiri_mod.mz_cre(nyu_date_int)

    # 回目を修正する
    fee_cre_month_keiri_mod.mz_update_kaime(nyu_date_int)

    # send email

    # subject, body
    end_time = mod_datetime.mz_tnow("for_datetime")
    subject = send_file_title_header + "-" + nyu_date_str
    body = ""
    body += "\n"
    body += "処理　　：" + send_file_title_header + "\n"
    body += "入金月　：" + nyu_date_str + "\n"
    body += "件数　　：" + str(exe_cnt) + "\n"
    body += "\n"
    body += "処理開始時刻：" + start_time + "\n"
    body += "処理終了時刻：" + end_time + "\n"
    body += "service : " + service + "\n"
    body += "\n"

    # Gmail APIでメール送信
    service_gmail = mod_gmail_api.get_gmail_service()
    if service_gmail is not None:
        # メールメッセージを作成
        message_obj = MIMEText(body, "plain", "utf-8")
        message_obj["to"] = to_email
        message_obj["from"] = from_email
        message_obj["subject"] = subject

        # Base64エンコード
        raw_message = base64.urlsafe_b64encode(message_obj.as_bytes()).decode("utf-8")

        # メール送信
        try:
            result = service_gmail.users().messages().send(userId="me", body={"raw": raw_message}).execute()
            print(f"fee_cre_month_keiri メール送信成功: {result}")
        except Exception as e:
            print(f"fee_cre_month_keiri メール送信エラー: {e}")
            import traceback

            print(f"fee_cre_month_keiri 詳細エラー: {traceback.format_exc()}")

    # task_sta update
    task_sta = "end"
    task_name = "fee_cre_keiri"
    task_exe_user = user_email
    mod_task_sta.mz_task_sta_write(task_sta, task_name, task_exe_user)

    # base - level 2 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(2, jwtg, acc_page_name)

    # dic
    dic = {}
    return dic
