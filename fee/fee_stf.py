# -------------------------------------------------------------------
#  fee_stf.py
#  |--fee_stf      - 画面作成
#  |--fee_stf_exe  - 実行する、タスクオブジェクトを渡す
#  |--fee_stf_task - タスク処理、sheetを作成、メール送信
#  fee_stf_mod.py - sheetを作成
#  fee_stf_sql.py - modを実行するときのsql
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
    To,
    Content,
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)

from _mod import fs_config, mod_base, mod_que, mod_datetime
from _mod_fis import (
    mod_kei_nyu_pay,
    mod_section,
    mod_staff,
    mod_task_sta,
    mod_xlsxwriter,
)
from fee import (
    # fee_stf_mod_total,
    # fee_stf_mod_coltd,
    fee_stf_mod_list,
    fee_stf_mod_total_calc,
    fee_stf_mod_coltd_calc,
)
from sum import sum_common_mod


def fee_stf():
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
            "section_data_all": [],
            "staff_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "login_level": login_level,
            "user_email": user_email,
            "nyu_data": mod_kei_nyu_pay.mz_common_nyu_sel(201904),
            "section_data_all": mod_section.mz_section_data_on(),
            "staff_data_all": mod_staff.mz_staff_data_all(),
        }
    return dic


def fee_stf_exe():
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
        task_sta, task_start_time, task_exe_user = mod_task_sta.mz_task_sta_chk("fee_cre")
        if task_sta == "end":
            # task que
            que_project = fs_dic["project_name"]
            que_location = fs_dic["que_location"]
            que_id = fs_dic["que_id"]
            que_url = fs_dic["que_site"] + "/fee/stf_task"
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


def fee_stf_task():
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
    pay_date_str = js_obj["pay_date_str"]

    section_name = js_obj["section_name"]
    staff_email = js_obj["staff_email"]
    staff_name = js_obj["staff_name"]

    project_name = obj["project_name"]
    bucket_name = obj["bucket_name"]
    from_email = obj["sender_email"]
    to_email = js_obj["send_email"]
    service = obj["service"]

    # file create

    # create in memory
    output = io.BytesIO()

    # workbook
    book = xlsxwriter.Workbook(output, {"in_memory": True})

    # cell format dic
    cf_dic = mod_xlsxwriter.mz_cf(book)

    # 支払合計 計算式
    row = 0
    sheet = book.add_worksheet("合計")
    sheet = fee_stf_mod_total_calc.mz_total(
        sheet,
        cf_dic,
        row,
        pay_date_str,
        mod_datetime.mz_tnow("for_datetime"),
        nyu_date_int,
        staff_email,
    )

    # 保険会社別 計算式
    row = 0
    sheet = book.add_worksheet("保険会社別")
    sheet, row = fee_stf_mod_coltd_calc.mz_coltd(
        sheet,
        cf_dic,
        row,
        send_file_title_header + "-" + nyu_date_str + "-" + section_name + "-" + staff_name,
        nyu_date_int,
        staff_email,
    )

    # total, footer create datetime, user_email
    row = row - 2
    sheet, row = sum_common_mod.mz_datetime_user(sheet, row, 8, cf_dic, user_email)

    # リスト主担当
    row = 0
    sheet = book.add_worksheet("リスト主担当")
    sheet, sql_data_cnt = fee_stf_mod_list.mz_list(sheet, row, cf_dic, nyu_date_int, staff_email, "main")

    # リスト副担当
    row = 0
    sheet = book.add_worksheet("リスト副担当")
    sheet, sql_data_cnt = fee_stf_mod_list.mz_list(sheet, row, cf_dic, nyu_date_int, staff_email, "sub")

    # リスト提携
    row = 0
    sheet = book.add_worksheet("リスト提携")
    sheet, sql_data_cnt = fee_stf_mod_list.mz_list(sheet, row, cf_dic, nyu_date_int, staff_email, "gyotei")

    # リスト全て
    # row = 0
    # sheet = book.add_worksheet("リスト全て")
    # sheet, sql_data_cnt = fee_stf_mod_list.mz_list(
    #     sheet, row, cf_dic, nyu_date_int, staff_email, "all"
    # )

    # 支払合計 計算式なし
    # row = 0
    # sheet = book.add_worksheet(section_name + "_" + staff_name + "_合計_計算式なし")
    # sheet = fee_stf_mod_total.mz_total(
    #     sheet,
    #     cf_dic,
    #     row,
    #     pay_date_str,
    #     mod_datetime.mz_tnow("for_datetime"),
    #     nyu_date_int,
    #     staff_email,
    # )

    # 保険会社別 計算式なし
    # row = 0
    # sheet = book.add_worksheet(section_name + "_" + staff_name + "_保険会社別_計算式なし")
    # sheet, row = fee_stf_mod_coltd.mz_coltd(
    #     sheet,
    #     cf_dic,
    #     row,
    #     send_file_title_header
    #     + "-"
    #     + nyu_date_str
    #     + "-"
    #     + section_name
    #     + "-"
    #     + staff_name,
    #     nyu_date_int,
    #     staff_email,
    # )

    # total, footer create datetime, user_email
    # row = row - 2
    # sheet, row = sum_common_mod.mz_datetime_user(sheet, row, 8, cf_dic, user_email)

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
    body_data = ""
    body_data += "\n"
    body_data += "処理　　：" + send_file_title_header + "\n"
    body_data += "入金月　：" + nyu_date_str + "\n"
    body_data += "営業所　：" + section_name + "\n"
    body_data += "担当者　：" + staff_name + "\n"
    body_data += "件数　　：" + str(sql_data_cnt) + "\n"
    body_data += "\n"
    body_data += "処理開始時刻：" + start_time + "\n"
    body_data += "処理終了時刻：" + end_time + "\n"
    body_data += "service : " + service + "\n"
    body_data += "\n"

    # sendgrid
    from_email = Email(from_email)
    to_email = To(to_email)
    subject = send_file_name
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
