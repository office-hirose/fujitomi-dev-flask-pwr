# ------------------------------------------------------------------------
#  nttgw_email.py
#  |--nttgw_email      - 画面作成
#  |--nttgw_email_exe  - 実行する、タスクオブジェクトを渡す
#  |--nttgw_email_task - タスク処理、メール送信
# ------------------------------------------------------------------------
import sys
import json
import datetime
from flask import request
from _mod import fs_config, mod_base, mod_que, mod_datetime, sql_config
from _mod_fis import mod_staff
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, To
import time


def nttgw_email():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "staff_data_all": [],
            "subject_data": [],
            "body_data": [],
            "subject_body_html": "",
        }
    else:
        # data
        staff_data_all = mod_staff.mz_staff_data_all()
        subject_data, body_data, subject_body_html = mz_nttgw_email_subject_body()

        dic = {
            "level_error": level_error,
            "staff_data_all": staff_data_all,
            "subject_data": subject_data,
            "body_data": body_data,
            "subject_body_html": subject_body_html,
        }
    return dic


def nttgw_email_exe():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    user_email = base_data["google_account_email"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "send_email": "",
        }
    else:
        # task que
        que_project = fs_dic["project_name"]
        que_location = fs_dic["que_location"]
        que_id = fs_dic["que_id"]
        que_url = fs_dic["que_site"] + "/nttgw/email_task"
        que_body = {
            "js_obj": json.loads(request.data.decode("utf-8")),
            "project_name": fs_dic["project_name"],
            "sender_email": fs_dic["sender_email"],
            "service": fs_dic["project_name"],
            "user_email": user_email,
        }
        mod_que.mz_que(que_project, que_location, que_id, que_url, que_body)

        dic = {
            "level_error": level_error,
            "send_email": user_email,
        }
    return dic


def nttgw_email_task():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # obj
    obj = request.get_json()
    js_obj = obj["js_obj"]
    jwtg = js_obj["jwtg"]

    # value
    from_email = obj["sender_email"]
    to_email = obj["user_email"]

    # subject, subject_body_html, email address data
    subject_data, body_data, subject_body_html = mz_nttgw_email_subject_body()
    address_data = mz_nttgw_email_address_data()

    # send contents
    from_email = Email(from_email)
    subject = subject_data
    content = Content("text/plain", body_data)

    # send email
    for v in address_data:
        to_email = To(v)
        mail_con = Mail(from_email, to_email, subject, content)
        sg = sendgrid.SendGridAPIClient(fs_dic["sendgrid_api_key"])
        sg.send(mail_con)
        time.sleep(3.0)  # pause xx seconds

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(9, jwtg, acc_page_name)

    # dic
    dic = {}
    return dic


# subject, body
def mz_nttgw_email_subject_body():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # today
    now_yyyy_mm_dd_str = mod_datetime.mz_dt2str_yymmdd_hyphen_jst(datetime.datetime.now() + datetime.timedelta(hours=0))

    # import data cnt
    today_num = mod_datetime.mz_now_date_num()
    # today_num = 20211229
    sql = "SELECT * FROM sql_order_store WHERE create_date = " + str(today_num) + ' AND exe_sta = "nttgw";'
    sql_data = sql_config.mz_sql(sql)
    import_cnt = len(sql_data)

    # service name
    service = fs_dic["project_name"]

    # subject
    subject_data = now_yyyy_mm_dd_str + "・NTTGWインポート完了"

    # body
    body_data = "関係者各位"
    body_data += "\n"
    body_data += "\n"
    body_data += now_yyyy_mm_dd_str
    body_data += "\n"
    body_data += "\n"
    body_data += "明細含め" + str(import_cnt) + "件"
    body_data += "\n"
    body_data += "\n"
    body_data += "NTTGWインポート完了"
    body_data += "\n"
    body_data += "\n"
    body_data += "admin@fujitomi.jp"
    body_data += "\n"
    body_data += "\n"
    body_data += "service : " + service + "\n"
    body_data += "\n"

    # body
    subject_body_html = ""

    subject_body_html += "<div>"
    subject_body_html += '<font color="red">'
    subject_body_html += now_yyyy_mm_dd_str + "・NTTGWインポート完了"
    subject_body_html += "</font>"
    subject_body_html += "</div>"

    subject_body_html += "<br>"

    subject_body_html += "<div>" + "関係者各位" + "</div>"

    subject_body_html += "<br>"

    subject_body_html += "<div>" + now_yyyy_mm_dd_str + "</div>"

    subject_body_html += "<div>" + "明細含め" + str(import_cnt) + "件" + "</div>"

    subject_body_html += "<div>" + "NTTGWインポート完了" + "</div>"

    subject_body_html += "<br>"

    subject_body_html += "<div>" + "admin@fujitomi.jp" + "</div>"

    subject_body_html += "<div>" + "service : " + service + "</div>"

    return subject_data, body_data, subject_body_html


# send email address data
def mz_nttgw_email_address_data():
    address_data = []
    sql = 'SELECT * FROM sql_staff WHERE nttgw_send_email_onoff = "on" ORDER BY sort;'

    # debug
    # sql = '''
    #     SELECT * FROM sql_staff
    #     WHERE nttgw_send_email_onoff = "on" AND (staff_cd = 'admin@tokyo' OR staff_cd = 'hirose.t@tokyo');
    # '''

    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        address_data.append(str(dt["send_email"]))
    return address_data
