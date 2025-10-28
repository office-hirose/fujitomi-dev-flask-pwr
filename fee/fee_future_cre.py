# -------------------------------------------------------------------
#  fee_future_cre.py
#  |--fee_future_cre      - 画面作成
#  |--fee_future_cre_exe  - 実行する、タスクオブジェクトを渡す
#  |--fee_future_cre_task - タスク処理、作成構築、作成終了後のメール送信
#  fee_future_cre_sql.py - 実行sql
# -------------------------------------------------------------------
import sys
import json
from flask import request
from _mod import fs_config, mod_base, mod_que, mod_datetime
from _mod_fis import mod_kei_nyu_pay, mod_staff, mod_task_sta

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from fee import fee_future_cre_sql


def fee_future_cre():
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


def fee_future_cre_exe():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    # user_email = base_data["google_account_email"]

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
        task_sta, task_start_time, task_exe_user = mod_task_sta.mz_task_sta_chk("fee_cre")
        # task que
        if task_sta == "end":
            que_project = fs_dic["project_name"]
            que_location = fs_dic["que_location"]
            que_id = fs_dic["que_id"]
            que_url = fs_dic["que_site"] + "/fee/future_cre_task"

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


def fee_future_cre_task():
    # init, firestore
    fs_dic = fs_config.fs_dic()

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
    task_name = "fee_future_cre"
    task_exe_user = user_email
    mod_task_sta.mz_task_sta_write(task_sta, task_name, task_exe_user)

    # delete
    # fee_future_cre_sql.mz_del_fee_future(nyu_date_int)
    fee_future_cre_sql.mz_del_fee_future()
    fee_future_cre_sql.mz_del_fee_future_cnt()

    # 前年度年月int, 前月年月int
    last_month, last_year, last2_year = fee_future_cre_sql.mz_last_year_month(nyu_date_int)

    # insert sql_fee_future_cnt
    fee_future_cre_sql.mz_cnt_tbl_cre(last2_year)

    # ---------------------------------------------------------------------------------
    # 損保
    # ---------------------------------------------------------------------------------

    # 月払い/前月の月払いをそのままコピー
    sql_data = fee_future_cre_sql.mz_sonpo_last_month_01_06(last_month)
    fee_future_cre_sql.mz_insert(sql_data)

    # 年払い/1年前の年払いをそのままコピー
    sql_data = fee_future_cre_sql.mz_sonpo_last_year_15(last_year)
    fee_future_cre_sql.mz_insert(sql_data)

    # 一時払い/1年前の一括払いをそのままコピー（これをどうするかが問題）
    sql_data = fee_future_cre_sql.mz_sonpo_last_year_00(last_year)
    fee_future_cre_sql.mz_insert(sql_data)

    # 損保・その他の払い方法は無視。

    # ---------------------------------------------------------------------------------
    # 生保
    # ---------------------------------------------------------------------------------

    # 前月が月払い/次年度/前月の月払いをそのままコピー
    sql_data = fee_future_cre_sql.mz_seiho_last_month_01_06(last_month)
    fee_future_cre_sql.mz_insert(sql_data)

    # 前月が月払い/初年度で既に支払が11回以下/前月の月払いをそのままコピー
    sql_data = fee_future_cre_sql.mz_seiho_last_month_01_06_11under(last_month)
    fee_future_cre_sql.mz_insert(sql_data)

    # 前月が月払い/初年度/既に支払が12回/契約データから次年度以降を出して算出する。5Lなどの場合で6年目は0円になる処理はされていない。
    sql_data = fee_future_cre_sql.mz_seiho_last_month_01_06_12equal(last_month)
    fee_future_cre_sql.mz_insert(sql_data)

    # 年払い/初年度/1年前の年払いを出して、契約データから次年度以降を出して算出する。
    sql_data = fee_future_cre_sql.mz_seiho_last_year_15(last_year)
    fee_future_cre_sql.mz_insert(sql_data)

    # 一括払い/1年前の一括払いをそのままコピー => 実行しない

    # 生保・その他の払い方法は無視。

    # 入金日を変更, count
    fee_future_cre_sql.mz_date_update(last_year, last_month, nyu_date_int)
    exe_cnt = fee_future_cre_sql.mz_cnt(nyu_date_int)

    # send email

    # subject, body
    end_time = mod_datetime.mz_tnow("for_datetime")
    subject = send_file_title_header + "-" + nyu_date_str
    body = ""
    body += "\n"
    body += "処理　　：" + send_file_title_header + "\n"
    body += "想定入金月　：" + nyu_date_str + "\n"
    body += "件数　　：" + str(exe_cnt) + "\n"
    body += "\n"
    body += "処理開始時刻：" + start_time + "\n"
    body += "処理終了時刻：" + end_time + "\n"
    body += "service : " + service + "\n"
    body += "\n"

    # from, to
    mail_con = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body,
    )

    # send
    sg = SendGridAPIClient(fs_dic["sendgrid_api_key"])
    sg.send(mail_con)

    # task_sta update
    task_sta = "end"
    task_name = "fee_future_cre"
    task_exe_user = user_email
    mod_task_sta.mz_task_sta_write(task_sta, task_name, task_exe_user)

    # base - level 2 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(2, jwtg, acc_page_name)

    # dic
    dic = {}
    return dic
