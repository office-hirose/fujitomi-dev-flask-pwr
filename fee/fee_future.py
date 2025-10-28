# -------------------------------------------------------------------
#  fee_future.py
#  |--fee_future      - 画面作成
#  |--fee_future_exe  - 実行する、タスクオブジェクトを渡す
#  |--fee_future_task - タスク処理、sheetを作成、メール送信
#  fee_future_mod.py - sheetを作成
#  fee_future_sql.py - modを実行するときのsql
# -------------------------------------------------------------------
import io
import sys
import json
from flask import request

from google.cloud import storage
import xlsxwriter
import base64
import sendgrid
from sendgrid.helpers.mail import (
    Email,
    Content,
    Mail,
    To,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)

from _mod import fs_config, mod_base, mod_que, mod_datetime
from _mod_fis import mod_kei_nyu_pay, mod_staff, mod_task_sta, mod_xlsxwriter

from fee import (
    fee_future_mod_coltd,
    fee_future_mod_stf,
    fee_future_mod_email,
    fee_future_mod_list,
)
from sum import sum_common_mod


def fee_future():
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


def fee_future_exe():
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
        task_sta, task_start_time, task_exe_user = mod_task_sta.mz_task_sta_chk("fee_future_cre")
        if task_sta == "end":
            # task que
            que_project = fs_dic["project_name"]
            que_location = fs_dic["que_location"]
            que_id = fs_dic["que_id"]
            que_url = fs_dic["que_site"] + "/fee/future_task"

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


def fee_future_task():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # obj
    obj = request.get_json()
    js_obj = obj["js_obj"]
    jwtg = js_obj["jwtg"]

    # value
    start_time = mod_datetime.mz_tnow("for_datetime")
    user_email = js_obj["send_email"]

    send_file_name = js_obj["send_file_name"] + "-" + obj["send_file_name_datetime"] + ".xlsx"
    send_file_title_header = js_obj["send_file_title_header"]

    nyu_date_int = js_obj["nyu_date_int"]
    nyu_date_str = js_obj["nyu_date_str"]
    nyu_nendo_int = js_obj["nyu_nendo_int"]
    nyu_nendo_str = js_obj["nyu_nendo_str"]

    project_name = obj["project_name"]
    bucket_name = obj["bucket_name"]
    from_email = obj["sender_email"]
    to_email = js_obj["send_email"]
    service = obj["service"]

    title_name = send_file_title_header + "-" + nyu_date_str + "-全社"

    # file create

    # create in memory
    output = io.BytesIO()

    # workbook
    book = xlsxwriter.Workbook(output, {"in_memory": True})

    # cell format dic
    cf_dic = mod_xlsxwriter.mz_cf(book)

    # 1 会社別
    row = 0
    sheet = book.add_worksheet("想定実収手数料_保険会社別")
    sheet = fee_future_mod_coltd.mz_setting_sum(sheet)
    sheet, row = fee_future_mod_coltd.mz_title_sum(sheet, cf_dic, row, title_name, nyu_nendo_str)
    sheet, row = fee_future_mod_coltd.mz_data_sum(sheet, cf_dic, row, nyu_date_int, nyu_nendo_int)
    row = row - 2
    sheet, row = sum_common_mod.mz_datetime_user(sheet, row, 16, cf_dic, user_email)

    # 2 担当別（Email別）
    row = 0
    sheet = book.add_worksheet("想定実収手数料_担当別")
    sheet = fee_future_mod_email.mz_setting_sum(sheet)
    sheet, row = fee_future_mod_email.mz_title_sum(sheet, cf_dic, row, title_name, nyu_nendo_str)
    sheet, row = fee_future_mod_email.mz_data_sum(sheet, cf_dic, row, nyu_date_int, nyu_nendo_int)
    row = row - 2
    sheet, row = sum_common_mod.mz_datetime_user(sheet, row, 20, cf_dic, user_email)

    # 3 担当別（staff_cdで分けているのでセクションに複数の担当が表示される）
    row = 0
    sheet = book.add_worksheet("想定実収手数料_担当別_複数拠点")
    sheet = fee_future_mod_stf.mz_setting_sum(sheet)
    sheet, row = fee_future_mod_stf.mz_title_sum(sheet, cf_dic, row, title_name, nyu_nendo_str)
    sheet, row = fee_future_mod_stf.mz_data_sum(sheet, cf_dic, row, nyu_date_int, nyu_nendo_int)
    row = row - 2
    sheet, row = sum_common_mod.mz_datetime_user(sheet, row, 20, cf_dic, user_email)

    # 4 リスト
    row = 0
    sheet = book.add_worksheet("想定実収手数料リスト")
    sheet = fee_future_mod_list.mz_title_list(sheet, cf_dic)
    sheet, sql_data_cnt = fee_future_mod_list.mz_data_list_stf(sheet, row, cf_dic, nyu_date_int)

    # file close

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

    # send email

    # sendgrid subject/body
    end_time = mod_datetime.mz_tnow("for_datetime")
    subject = send_file_name
    body_data = ""
    body_data += "\n"
    body_data += "処理　　：" + send_file_title_header + "\n"
    body_data += "入金月　：" + nyu_date_str + "\n"
    body_data += "件数　　：" + str(sql_data_cnt) + "\n"
    body_data += "\n"
    body_data += "処理開始時刻：" + start_time + "\n"
    body_data += "処理終了時刻：" + end_time + "\n"
    body_data += "service : " + service + "\n"
    body_data += "\n"

    # sendgrid
    from_email = Email(from_email)
    to_email = To(to_email)
    content = Content("text/plain", body_data)
    mail_con = Mail(from_email, to_email, subject, content)

    # file from GCS
    blob = storage.Blob(file_name, bucket)
    content = blob.download_as_string()
    gcs_file = base64.b64encode(content).decode()

    # attach file
    attach_file = Attachment(
        FileContent(gcs_file),
        FileName(send_file_name),
        FileType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        Disposition("attachment"),
    )
    mail_con.attachment = attach_file

    # send
    sg = sendgrid.SendGridAPIClient(fs_dic["sendgrid_api_key"])
    sg.send(mail_con)

    # base - level 2 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(2, jwtg, acc_page_name)

    # dic
    dic = {}
    return dic
