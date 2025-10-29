# -------------------------------------------------------------------
#  fee_gyotei_list.py
#  |--fee_gyotei_list      - 画面作成
#  |--fee_gyotei_list_exe  - 実行する、タスクオブジェクトを渡す
#  |--fee_gyotei_list_task - タスク処理、sheetを作成、メール送信
#  fee_gyotei_list_mod.py - sheetを作成
#  fee_gyotei_list_sql.py - modを実行するときのsql
# -------------------------------------------------------------------
import io
import sys
import json
from flask import request

from google.cloud import storage
import xlsxwriter

# from openpyxl import load_workbook
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from _mod import fs_config, mod_base, mod_que, mod_datetime, mod_gmail_api
from _mod_fis import (
    mod_kei_nyu_pay,
    mod_section,
    mod_staff,
    mod_gyotei,
    mod_task_sta,
    mod_xlsxwriter,
)
from fee import fee_gyotei_list_mod


def fee_gyotei_list():
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
            "gyotei_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "login_level": login_level,
            "user_email": user_email,
            "nyu_data": mod_kei_nyu_pay.mz_common_nyu_sel(201904),
            "section_data_all": mod_section.mz_section_data_on(),
            "staff_data_all": mod_staff.mz_staff_data_all(),
            "gyotei_data_all": mod_gyotei.mz_gyotei_data_all(),
        }
    return dic


def fee_gyotei_list_exe():
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
            que_url = fs_dic["que_site"] + "/fee/gyotei_list_task"
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


def fee_gyotei_list_task():
    # obj
    obj = request.get_json()
    js_obj = obj["js_obj"]
    jwtg = js_obj["jwtg"]

    # value
    start_time = mod_datetime.mz_tnow("for_datetime")
    # user_email = js_obj["send_email"]

    send_file_name = js_obj["send_file_name"]

    nyu_date_int = js_obj["nyu_date_int"]
    pay_date_str = js_obj["pay_date_str"]

    section_name = js_obj["section_name"]
    gyotei_cd = js_obj["gyotei_cd"]

    project_name = obj["project_name"]
    bucket_name = obj["bucket_name"]
    from_email = obj["sender_email"]
    to_email = js_obj["send_email"]
    service = obj["service"]

    sql_data = mod_gyotei.mz_gyotei_data_sel(gyotei_cd)
    for dt in sql_data:
        kanri_cd = dt["kanri_cd"]
        gyotei_name = dt["name"]
        gyotei_name_simple = dt["name_simple"]
        bank_account_all = (
            dt["bank_name"] + "　" + dt["bank_branch"] + "　" + dt["bank_kind"] + "　" + dt["bank_account"]
        )
        bank_account_name = dt["bank_account_name"]
        gensen_cd = dt["gensen_cd"]
        kojo_fee = dt["kojo_fee"]

    # file create

    # init
    all_list = []
    all_list_cnt = 0
    row = 0
    pagebreak_list = []
    pagebreak_cnt = 0

    # create in memory
    output = io.BytesIO()

    # workbook
    book = xlsxwriter.Workbook(output, {"in_memory": True})
    sheet = book.add_worksheet("支払明細_" + gyotei_name_simple)

    # cell format dic
    cf_dic = mod_xlsxwriter.mz_cf(book)

    # setting
    sheet = fee_gyotei_list_mod.mz_setting(sheet)

    # data create
    (
        all_list,
        fee_agt_yen_total,
        fee_gyotei_yen_total,
    ) = fee_gyotei_list_mod.mz_data_create(nyu_date_int, gyotei_cd)
    all_list_cnt = len(all_list)

    # header
    header_dic = {
        "gyotei_name": gyotei_name,
        "pay_date_str": pay_date_str,
        "section_name": section_name,
        "kanri_cd": kanri_cd,
    }
    row += 1
    sheet, row = fee_gyotei_list_mod.mz_header(sheet, row, cf_dic, header_dic)

    # bank
    bank_dic = {
        "bank_account_all": bank_account_all,
        "bank_account_name": bank_account_name,
    }
    row += 7  # 空白部分
    sheet, row = fee_gyotei_list_mod.mz_bank(sheet, row, cf_dic, bank_dic)

    # total
    total_dic = {"gensen_cd": gensen_cd, "kojo_fee": kojo_fee}
    row += -12  # 空白部分もどし
    sheet, row = fee_gyotei_list_mod.mz_total(sheet, row, cf_dic, total_dic)

    # sign
    row += 4  # 空白部分
    sheet, row = fee_gyotei_list_mod.mz_sign(sheet, row, cf_dic)

    # pagebreak
    row += 4  # 空白部分
    pagebreak_cnt = row - 1
    pagebreak_list.append(pagebreak_cnt)

    # header list
    header_list_dic = {
        "gyotei_name": gyotei_name,
        "pay_date_str": pay_date_str,
        "section_name": section_name,
        "kanri_cd": kanri_cd,
    }
    sheet, row = fee_gyotei_list_mod.mz_header_list(sheet, row, cf_dic, header_list_dic)

    # list title
    sheet, row = fee_gyotei_list_mod.mz_title_list(sheet, row, cf_dic)

    # list data
    data_write_dic = {
        "pagebreak_cnt": pagebreak_cnt,
        "pagebreak_list": pagebreak_list,
        "all_list": all_list,
        "gyotei_name": gyotei_name,
        "pay_date_str": pay_date_str,
        "section_name": section_name,
        "kanri_cd": kanri_cd,
    }
    row += 1
    sheet, row = fee_gyotei_list_mod.mz_data_write(sheet, row, cf_dic, data_write_dic)

    # define
    sheet.set_paper(9)  # A4 size paper
    sheet.set_portrait()  # yoko
    sheet.print_area(0, 0, row + 1, 13)  # area
    sheet.fit_to_pages(1, 0)  # Fit to page, width, height
    sheet.set_h_pagebreaks(pagebreak_list)  # page breaks

    # file close ----------------------------------------------------------------------------------

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
    body_data += "処理　　：" + "提携者の支払リスト" + "\n"
    body_data += "提携者　：" + gyotei_name_simple + "\n"
    body_data += "件数　　：" + str(all_list_cnt) + "\n"
    body_data += "\n"
    body_data += "処理開始時刻：" + start_time + "\n"
    body_data += "処理終了時刻：" + end_time + "\n"
    body_data += "service : " + service + "\n"
    body_data += "\n"

    # 支払金額小計(税抜)fee_gyotei_yen_totalの数字により、ファイル名を変更する
    if fee_gyotei_yen_total < 0:
        res_send_file_name = "マイナス-" + send_file_name
    elif fee_gyotei_yen_total == 0:
        res_send_file_name = "0円-" + send_file_name
    else:
        res_send_file_name = send_file_name

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
        attachment.add_header("Content-Disposition", "attachment", filename=("utf-8", "", res_send_file_name))
        message_obj.attach(attachment)

        # Base64エンコード
        raw_message = base64.urlsafe_b64encode(message_obj.as_bytes()).decode("utf-8")

        # メール送信
        try:
            result = service_gmail.users().messages().send(userId="me", body={"raw": raw_message}).execute()
            print(f"fee_gyotei_list メール送信成功: {result}")
        except Exception as e:
            print(f"fee_gyotei_list メール送信エラー: {e}")
            import traceback

            print(f"fee_gyotei_list 詳細エラー: {traceback.format_exc()}")

    # base - level 2 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(2, jwtg, acc_page_name)

    # dic
    dic = {}
    return dic
