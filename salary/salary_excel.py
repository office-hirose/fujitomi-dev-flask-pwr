# ------------------------------------------------------------------------
#  salary_excel.py
#  |--salary_excel_start      - 画面作成
#  |--salary_excel_exe  - 実行する、タスクオブジェクトを渡す
#  |--salary_excel_task - タスク処理、計算、MySQLを更新、メール送信
#  salary_excel_mod.py - 計算、MySQLを更新
#  salary_excel_sql.py - 計算、MySQLを更新、modを実行するときのsql
# ------------------------------------------------------------------------
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
from _mod_fis import mod_kei_nyu_pay, mod_staff, mod_xlsxwriter
from salary import (
    salary_excel_month_title,
    salary_excel_month_section,
    salary_excel_month_staff,
    salary_excel_sql_nendo_nendo,
    salary_excel_nendo_title,
    salary_excel_nendo_section,
    salary_excel_nendo_staff,
)


def salary_excel_start():
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


def salary_excel_exe():
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
        que_url = fs_dic["que_site"] + "/salary/salary_excel_task"
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


def salary_excel_task():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # obj
    obj = request.get_json()
    js_obj = obj["js_obj"]
    jwtg = js_obj["jwtg"]

    # value
    start_time = mod_datetime.mz_tnow("for_datetime")

    send_file_name = js_obj["send_file_name"]
    send_file_title_header = js_obj["send_file_title_header"]

    salary_date_int = js_obj["salary_date_int"]
    salary_date_str = js_obj["salary_date_str"]
    to_email = js_obj["send_email"]

    project_name = obj["project_name"]
    bucket_name = obj["bucket_name"]
    from_email = obj["sender_email"]
    service = obj["service"]

    # file create ------------------------------------------------------------------------------------------------------

    # Create an in-memory output file for the new workbook.
    output = io.BytesIO()

    # workbook
    book = xlsxwriter.Workbook(output, {"in_memory": True})

    # 選択した年月 シート名 A4サイズ セルの高さ ------------------------------------------------------------------------------
    sheet = book.add_worksheet(salary_date_str)
    sheet.set_paper(9)  # A4 size paper
    sheet.set_default_row(25)  # height

    # cell format dic
    cf_dic = mod_xlsxwriter.mz_cf(book)

    # メインタイトル
    row = 0
    sheet, row = salary_excel_month_title.mz_title(sheet, row, cf_dic, send_file_title_header, salary_date_str)

    # セクション別
    row += 2
    sheet, row = salary_excel_month_section.mz_title(sheet, row, cf_dic)
    sheet, row, sql_data_cnt = salary_excel_month_section.mz_data(
        sheet,
        row,
        cf_dic,
        salary_date_int,
    )

    # 担当別
    row += 2
    sheet, row = salary_excel_month_staff.mz_title(sheet, row, cf_dic)
    sheet, row, sql_data_cnt = salary_excel_month_staff.mz_data(
        sheet,
        row,
        cf_dic,
        salary_date_int,
    )

    # 年度累計 シート名 A4サイズ セルの高さ ---------------------------------------------------------------------------------
    nendo = salary_excel_sql_nendo_nendo.mz_nendo(salary_date_int)
    sheet = book.add_worksheet(str(nendo) + "年度累計")
    sheet.set_paper(9)  # A4 size paper
    sheet.set_default_row(25)  # height

    # メインタイトル
    row = 0
    sheet, row = salary_excel_nendo_title.mz_title(sheet, row, cf_dic, send_file_title_header, nendo)

    # セクション別
    row += 2
    sheet, row = salary_excel_nendo_section.mz_title(sheet, row, cf_dic)
    sheet, row, sql_data_cnt = salary_excel_nendo_section.mz_data(
        sheet,
        row,
        cf_dic,
        salary_date_int,
        nendo,
    )

    # 担当別
    row += 2
    sheet, row = salary_excel_nendo_staff.mz_title(sheet, row, cf_dic)
    sheet, row, sql_data_cnt = salary_excel_nendo_staff.mz_data(
        sheet,
        row,
        cf_dic,
        salary_date_int,
        nendo,
    )

    # close workbook ---------------------------------------------------------------------------------------------------
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

    # sendgrid subject/body
    end_time = mod_datetime.mz_tnow("for_datetime")
    subject_data = send_file_name
    body_data = ""
    body_data += "\n"
    body_data += "処理　　：" + send_file_title_header + "\n"
    body_data += "計上月　：" + salary_date_str + "\n"
    body_data += "件数　　：" + str(sql_data_cnt) + "\n"
    body_data += "\n"
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
