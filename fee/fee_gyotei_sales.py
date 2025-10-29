# -------------------------------------------------------------------
#  fee_gyotei_sales.py
#  |--fee_gyotei_sales      - 画面作成
#  |--fee_gyotei_sales_exe  - 実行する、タスクオブジェクトを渡す
#  |--fee_gyotei_sales_task - タスク処理、sheetを作成、メール送信
#  fee_gyotei_sales_mod.py - sheetを作成
#  fee_gyotei_sales_sql.py - modを実行するときのsql
# -------------------------------------------------------------------
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
from _mod_fis import (
    mod_kei_nyu_pay,
    mod_section,
    mod_staff,
    mod_task_sta,
    mod_xlsxwriter,
)
from fee import fee_gyotei_sales_mod, fee_gyotei_sales_sql


def fee_gyotei_sales():
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


def fee_gyotei_sales_exe():
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
            "task_sta": "",
            "task_start_time": "",
            "task_exe_user": "",
        }
    else:
        # 処理実行中かチェックする
        task_sta, task_start_time, task_exe_user = mod_task_sta.mz_task_sta_chk("fee_cre")
        if task_sta == "end":
            # task que
            que_project = fs_dic["project_name"]
            que_location = fs_dic["que_location"]
            que_id = fs_dic["que_id"]
            que_url = fs_dic["que_site"] + "/fee/gyotei_sales_task"
            que_body = {
                "js_obj": json.loads(request.data.decode("utf-8")),
                "project_name": fs_dic["project_name"],
                "bucket_name": fs_dic["upload_gcs_bucket"],
                "sender_email": fs_dic["sender_email"],
                "service": fs_dic["project_name"],
            }
            mod_que.mz_que(que_project, que_location, que_id, que_url, que_body)

        # dic
        dic = {
            "level_error": level_error,
            "task_sta": task_sta,
            "task_start_time": mod_datetime.mz_dt2str_yymmddhhmm_hyphen(task_start_time),
            "task_exe_user": task_exe_user,
        }
    return dic


def fee_gyotei_sales_task():
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

    project_name = obj["project_name"]
    bucket_name = obj["bucket_name"]
    from_email = obj["sender_email"]
    to_email = js_obj["send_email"]
    service = obj["service"]

    # file create

    # init
    row_cnt = 0  # セルのタテ
    pagebreak_list = []

    # 総合計を初期化
    all_syokei_tax_nasi = 0  # 小計税抜(合計)
    all_syokei_tax = 0  # 消費税(合計)
    all_kojo = 0  # 控除額(合計)
    all_syokei_tax_ari = 0  # 小計税込(合計)
    all_gensen = 0  # 源泉徴収額(合計)
    all_total = 0  # 合計税込(合計)

    sp = " "
    data_cnt = 0  # メール送信用、該当する全件数

    # create in memory
    output = io.BytesIO()

    # create workbook
    book = xlsxwriter.Workbook(output, {"in_memory": True})
    sheet = book.add_worksheet(pay_date_str + "_支払分_事業部用")

    # cell format dic
    cf_dic = mod_xlsxwriter.mz_cf(book)

    # cell setting, head write
    sheet = fee_gyotei_sales_mod.mz_setting(sheet)
    sheet, row_cnt = fee_gyotei_sales_mod.mz_head_title(sheet, row_cnt, cf_dic, pay_date_str, start_time)
    row_cnt += 1

    # section data
    sec_data = mod_section.mz_section_data_fumei_nasi()

    for sdt in sec_data:
        # header
        sheet, row_cnt = fee_gyotei_sales_mod.mz_header_title_normal(sheet, row_cnt, cf_dic)
        row_cnt += 1

        # initial 小計
        sub_syokei_tax_nasi = 0  # 小計税抜(小計)
        sub_syokei_tax = 0  # 消費税(小計)
        sub_kojo = 0  # 控除額(小計)
        sub_syokei_tax_ari = 0  # 小計税込(小計)
        sub_gensen = 0  # 源泉徴収額(小計)
        sub_total = 0  # 合計税込(小計)

        # fee data
        fee_data = fee_gyotei_sales_sql.mz_sql_fee_order_store_sales(nyu_date_int, sdt["section_cd"])

        left_number = 0

        for fdt in fee_data:
            data_cnt += 1
            left_number += 1

            section_name = fdt["section_name"]
            kanri_cd = fdt["kanri_cd"]
            gyotei_name = fdt["gyotei_name"]
            bank_detail = (
                fdt["bank_name"]
                + sp
                + fdt["bank_branch"]
                + sp
                + fdt["bank_kind"]
                + sp
                + fdt["bank_account"]
                + "\n"
                + fdt["bank_account_name"]
            )
            pay_fee = fdt["pay_fee"]
            pay_fee_tax = int(float(pay_fee) * 0.1)  # 消費税 10%、小数点以下切り捨て
            kojo_fee = fdt["kojo_fee"]
            pay_fee_sub_total = (pay_fee + pay_fee_tax) - kojo_fee
            gensen_cd = fdt["gensen_cd"]

            # 源泉徴収の計算
            if gensen_cd == "on":
                if pay_fee > 1000000:
                    gensen_fee = (int(float(pay_fee_sub_total) * 0.2042) * (-1)) + 102100
                else:
                    gensen_fee = int(float(pay_fee_sub_total) * 0.1021) * (-1)
            else:
                gensen_fee = 0

            pay_fee_main_total = pay_fee_sub_total + gensen_fee

            # write
            sheet.set_row(row_cnt, 48)  # height
            sheet.write(row_cnt, 0, left_number, cf_dic["cf_c10_bor"])
            sheet.write(row_cnt, 1, section_name, cf_dic["cf_c10_bor"])
            sheet.write(row_cnt, 2, kanri_cd, cf_dic["cf_c10_bor"])

            if fdt["keiri_list_onoff"] == "on":
                if fdt["onoff_cd"] == "on":
                    sheet.write(row_cnt, 3, gyotei_name, cf_dic["cf_l10_bor"])
                if fdt["onoff_cd"] == "off":
                    sheet.write(row_cnt, 3, gyotei_name, cf_dic["cf_l10_bor_red"])

            if fdt["keiri_list_onoff"] == "off":
                if fdt["onoff_cd"] == "on":
                    sheet.write(row_cnt, 3, gyotei_name, cf_dic["cf_l10_bor_yellow"])
                if fdt["onoff_cd"] == "off":
                    sheet.write(row_cnt, 3, gyotei_name, cf_dic["cf_l10_bor_red"])

            sheet.write(row_cnt, 4, bank_detail, cf_dic["cf_l10_bor_wrap"])
            sheet.write(row_cnt, 5, pay_fee, cf_dic["cf_r12_comma_bor"])
            sheet.write(row_cnt, 6, pay_fee_tax, cf_dic["cf_r12_comma_bor"])
            sheet.write(row_cnt, 7, kojo_fee, cf_dic["cf_r12_comma_bor"])
            sheet.write(row_cnt, 8, pay_fee_sub_total, cf_dic["cf_r12_comma_bor"])
            sheet.write(row_cnt, 9, gensen_fee, cf_dic["cf_r12_comma_bor"])
            sheet.write(row_cnt, 10, pay_fee_main_total, cf_dic["cf_r12_comma_bor"])
            row_cnt += 1

            # 小計計算
            sub_syokei_tax_nasi += pay_fee
            sub_syokei_tax += pay_fee_tax
            sub_kojo += kojo_fee
            sub_syokei_tax_ari += pay_fee_sub_total
            sub_gensen += gensen_fee
            sub_total += pay_fee_main_total

        # 合計計算
        all_syokei_tax_nasi = all_syokei_tax_nasi + sub_syokei_tax_nasi
        all_syokei_tax = all_syokei_tax + sub_syokei_tax
        all_kojo = all_kojo + sub_kojo
        all_syokei_tax_ari = all_syokei_tax_ari + sub_syokei_tax_ari
        all_gensen = all_gensen + sub_gensen
        all_total = all_total + sub_total

        sub_section_name = sdt["section_name"] + "　小計"

        sheet.set_row(row_cnt, 48)  # height
        sheet.write(row_cnt, 4, sub_section_name, cf_dic["cf_c14"])
        sheet.write(row_cnt, 5, sub_syokei_tax_nasi, cf_dic["cf_r12_comma_bor"])
        sheet.write(row_cnt, 6, sub_syokei_tax, cf_dic["cf_r12_comma_bor"])
        sheet.write(row_cnt, 7, sub_kojo, cf_dic["cf_r12_comma_bor"])
        sheet.write(row_cnt, 8, sub_syokei_tax_ari, cf_dic["cf_r12_comma_bor"])
        sheet.write(row_cnt, 9, sub_gensen, cf_dic["cf_r12_comma_bor"])
        sheet.write(row_cnt, 10, sub_total, cf_dic["cf_r12_comma_bor"])
        row_cnt += 1
        sheet.merge_range(row_cnt, 0, row_cnt, 10, "")
        row_cnt += 1

    # header all total
    sheet, row_cnt = fee_gyotei_sales_mod.mz_header_title_all_total(sheet, row_cnt, cf_dic)
    row_cnt += 1

    # write all total 合計
    all_name = "合計"
    sheet.set_row(row_cnt, 48)  # height
    sheet.write(row_cnt, 4, all_name, cf_dic["cf_c14"])
    sheet.write(row_cnt, 5, all_syokei_tax_nasi, cf_dic["cf_r12_comma_bor"])
    sheet.write(row_cnt, 6, all_syokei_tax, cf_dic["cf_r12_comma_bor"])
    sheet.write(row_cnt, 7, all_kojo, cf_dic["cf_r12_comma_bor"])
    sheet.write(row_cnt, 8, all_syokei_tax_ari, cf_dic["cf_r12_comma_bor"])
    sheet.write(row_cnt, 9, all_gensen, cf_dic["cf_r12_comma_bor"])
    sheet.write(row_cnt, 10, all_total, cf_dic["cf_r12_comma_bor"])
    row_cnt += 1
    sheet.merge_range(row_cnt, 0, row_cnt, 10, "")
    row_cnt += 1

    # sign
    # sheet, row_cnt = fee_gyotei_sales_mod.mz_sign(sheet, row_cnt, cf_dic)
    # row_cnt += 4

    # define
    sheet.set_paper(9)  # A4 size paper
    sheet.set_portrait()  # yoko
    sheet.print_area(0, 0, row_cnt + 1, 11)  # area
    sheet.fit_to_pages(1, 0)  # Fit to page, width, height
    sheet.set_h_pagebreaks(pagebreak_list)  # page breaks

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

    # subject/body
    end_time = mod_datetime.mz_tnow("for_datetime")
    subject_data = send_file_name
    body_data = ""
    body_data += "\n"
    body_data += "処理　　：" + "業務提携料支払リスト(事業部用)" + "\n"
    body_data += "支払月　：" + pay_date_str + "\n"
    body_data += "件数　　：" + str(data_cnt) + "\n"
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
            print(f"fee_gyotei_sales メール送信成功: {result}")
        except Exception as e:
            print(f"fee_gyotei_sales メール送信エラー: {e}")
            import traceback

            print(f"fee_gyotei_sales 詳細エラー: {traceback.format_exc()}")

    # base - level 2 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(2, jwtg, acc_page_name)

    # dic
    dic = {}
    return dic
