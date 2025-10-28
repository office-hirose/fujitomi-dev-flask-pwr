# ------------------------------------------------------------------------
#  manki_list.py
#  |--manki_list      - 画面作成
#  |--manki_list_exe  - 実行する、タスクオブジェクトを渡す
#  |--manki_list_task - タスク処理、sheetを作成、メール送信
#  manki_list_mod.py - sheetを作成
#  manki_list_sql.py - modを実行するときのsql
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
from _mod_fis import mod_kei_nyu_pay, mod_section, mod_staff, mod_xlsxwriter
from manki import manki_list_mod


def manki_list():
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
            "manki_data": mod_kei_nyu_pay.mz_common_man_sel(202004),
            "section_data_all": mod_section.mz_section_data_on(),
            "staff_data_all": mod_staff.mz_staff_data_all(),
        }
    return dic


def manki_list_exe():
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
        que_url = fs_dic["que_site"] + "/manki/list_task"
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


def manki_list_task():
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

    manki_date_int = js_obj["manki_date_int"]
    section_cd = js_obj["section_cd"]
    staff_cd = js_obj["staff_cd"]

    manki_date_str = js_obj["manki_date_str"]
    section_name = js_obj["section_name"]
    staff_name = js_obj["staff_name"]
    to_email = js_obj["send_email"]

    project_name = obj["project_name"]
    bucket_name = obj["bucket_name"]
    from_email = obj["sender_email"]
    service = obj["service"]

    # file create ---------------------------------------------------------------------------------

    # Create an in-memory output file for the new workbook.
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
        sheet, row = manki_list_mod.mz_title(sheet, row, cf_dic)

        # sheet data
        sheet, row, sql_data_cnt = manki_list_mod.mz_data(
            manki_date_int, section_cd, staff_cd, stf_key, sheet, row, cf_dic
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

    # sendgrid subject/body
    end_time = mod_datetime.mz_tnow("for_datetime")
    subject_data = send_file_name
    body_data = ""
    body_data += "\n"
    body_data += "処理　　：" + send_file_title_header + "\n"
    body_data += "満期月　：" + manki_date_str + "\n"
    body_data += "営業所　：" + section_name + "\n"
    body_data += "担当者　：" + staff_name + "\n"
    body_data += "件数　　：" + str(sql_data_cnt_total) + "\n"
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
