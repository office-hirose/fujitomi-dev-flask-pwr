# -------------------------------------------------------------------
#  sum_stf.py
#  |--sum_stf      - 画面作成
#  |--sum_stf_exe  - 実行する、タスクオブジェクトを渡す
#  |--sum_stf_task - タスク処理、sheetを作成、メール送信
#  sum_stf_mod.py - sheetを作成
#  sum_stf_sql.py - modを実行するときのsql
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
from _mod_fis import (
    mod_kei_nyu_pay,
    mod_section,
    mod_staff,
    mod_keiyaku_grp,
    mod_task_sta,
    mod_xlsxwriter,
)
from sum import sum_stf_mod, sum_common_mod


def sum_stf():
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
            "keiyaku_grp_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "login_level": login_level,
            "user_email": user_email,
            "keijyo_data": mod_kei_nyu_pay.mz_common_kei_sel(201904),
            "section_data_all": mod_section.mz_section_data_on(),
            "staff_data_all": mod_staff.mz_staff_data_all(),
            "keiyaku_grp_data_all": mod_keiyaku_grp.mz_keiyaku_grp_data_all(),
        }
    return dic


def sum_stf_exe():
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
        task_sta, task_start_time, task_exe_user = mod_task_sta.mz_task_sta_chk("sum_cre")
        if task_sta == "end":
            # task que
            que_project = fs_dic["project_name"]
            que_location = fs_dic["que_location"]
            que_id = fs_dic["que_id"]
            que_url = fs_dic["que_site"] + "/sum/stf_task"
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


def sum_stf_task():
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

    keijyo_date_int = js_obj["keijyo_date_int"]
    keijyo_date_str = js_obj["keijyo_date_str"]
    keijyo_nendo = js_obj["keijyo_nendo"]
    section_cd = js_obj["section_cd"]
    # staff_cd = js_obj['staff_cd')
    keiyaku_grp_cd = js_obj["keiyaku_grp_cd"]

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
    sheet = book.add_worksheet(section_name + "_" + staff_name)

    # cell format dic
    cf_dic = mod_xlsxwriter.mz_cf(book)

    # init

    kensu_cnt_sum_grand_tou = 0
    kensu_cnt_sum_grand_rui = 0

    keiko_cnt_sum_grand_tou = 0
    keiko_cnt_sum_grand_rui = 0

    res_hoken_ryo_year_sum_grand_tou = 0
    res_hoken_ryo_year_sum_grand_rui = 0

    res_fee_money_year_sum_grand_tou = 0
    res_fee_money_year_sum_grand_rui = 0

    res_fee_money_total_sum_grand_tou = 0
    res_fee_money_total_sum_grand_rui = 0

    row = 0

    # setting, header, title, cat
    sheet = sum_common_mod.mz_setting(sheet)
    sheet, row = sum_common_mod.mz_header(
        sheet,
        row,
        cf_dic,
        send_file_title_header + "-" + keijyo_date_str + "-" + section_name + "-" + staff_name,
    )
    sheet, row = sum_common_mod.mz_title(sheet, row, cf_dic)
    sheet, row = sum_common_mod.mz_cat(sheet, row, cf_dic)

    # 生保/損保/少短 create
    cat_list = ["1", "2", "3"]
    for cat_cd in cat_list:
        # data
        sheet, row, data_dic = sum_stf_mod.mz_data(
            sheet,
            row,
            cf_dic,
            keijyo_nendo,
            keijyo_date_int,
            keiyaku_grp_cd,
            cat_cd,
            section_cd,
            staff_email,
        )

        # grand calc
        kensu_cnt_sum_grand_tou += data_dic["kensu_cnt_sum_tou"]
        kensu_cnt_sum_grand_rui += data_dic["kensu_cnt_sum_rui"]

        keiko_cnt_sum_grand_tou += data_dic["keiko_cnt_sum_tou"]
        keiko_cnt_sum_grand_rui += data_dic["keiko_cnt_sum_rui"]

        res_hoken_ryo_year_sum_grand_tou += data_dic["res_hoken_ryo_year_sum_tou"]
        res_fee_money_year_sum_grand_tou += data_dic["res_fee_money_year_sum_tou"]
        res_fee_money_total_sum_grand_tou += data_dic["res_fee_money_total_sum_tou"]

        res_hoken_ryo_year_sum_grand_rui += data_dic["res_hoken_ryo_year_sum_rui"]
        res_fee_money_year_sum_grand_rui += data_dic["res_fee_money_year_sum_rui"]
        res_fee_money_total_sum_grand_rui += data_dic["res_fee_money_total_sum_rui"]

    # 総合計 grand
    grand_dic = {
        "kensu_cnt_sum_grand_tou": kensu_cnt_sum_grand_tou,
        "kensu_cnt_sum_grand_rui": kensu_cnt_sum_grand_rui,
        "res_hoken_ryo_year_sum_grand_tou": res_hoken_ryo_year_sum_grand_tou,
        "res_hoken_ryo_year_sum_grand_rui": res_hoken_ryo_year_sum_grand_rui,
        # "res_fee_money_year_sum_grand_tou": res_fee_money_year_sum_grand_tou,
        # "res_fee_money_year_sum_grand_rui": res_fee_money_year_sum_grand_rui,
        "res_fee_money_sum_grand_tou": res_fee_money_year_sum_grand_tou,
        "res_fee_money_sum_grand_rui": res_fee_money_year_sum_grand_rui,
        "res_fee_money_total_sum_grand_tou": res_fee_money_total_sum_grand_tou,
        "res_fee_money_total_sum_grand_rui": res_fee_money_total_sum_grand_rui,
        "keiko_cnt_sum_grand_tou": keiko_cnt_sum_grand_tou,
        "keiko_cnt_sum_grand_rui": keiko_cnt_sum_grand_rui,
    }

    sheet = sum_common_mod.mz_grand(sheet, cf_dic, grand_dic)

    # footer, datetime, user_email
    sheet, row = sum_common_mod.mz_datetime_user(sheet, row, 12, cf_dic, user_email)

    # print define
    sheet.set_paper(9)  # A4 size paper
    sheet.set_portrait()  # yoko
    sheet.print_area(0, 0, row + 1, 12)  # print area
    sheet.fit_to_pages(1, 0)  # Fit to page, width, height

    # 明細リスト作成処理 create sheet, setting, title, create list
    sheet = book.add_worksheet("リスト")
    sheet = sum_common_mod.mz_title_list(sheet, cf_dic)
    sheet = sum_common_mod.mz_data_stf_list(sheet, cf_dic, keijyo_date_int, keiyaku_grp_cd, staff_email)

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
    kensu_for_email = sum_common_mod.mz_data_stf_kensu_for_email(keijyo_date_int, keiyaku_grp_cd, staff_email)
    end_time = mod_datetime.mz_tnow("for_datetime")

    body_data = ""
    body_data += "\n"
    body_data += "処理　　：" + send_file_title_header + "\n"
    body_data += "計上月　：" + keijyo_date_str + "\n"
    body_data += "営業所　：" + section_name + "\n"
    body_data += "担当者　：" + staff_name + "\n"
    body_data += "件数　　：" + str(kensu_for_email) + "\n"
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
