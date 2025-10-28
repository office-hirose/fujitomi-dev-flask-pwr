import sys
import io
from flask import request
import xlsxwriter
import urllib.parse
from _mod import mod_base, sql_config
from _mod_fis import mod_sta, mod_section, mod_staff, mod_gyotei, mod_xlsxwriter
from mst import mst_gyotei_xlsx


def list():
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
            "sta_data_all": [],
            "section_data_all": [],
            "staff_data_all": [],
            "gyotei_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "sta_data_all": mod_sta.mz_sta_all(),
            "section_data_all": mod_section.mz_section_data_all(),
            "staff_data_all": mod_staff.mz_staff_data_all(),
            "gyotei_data_all": mod_gyotei.mz_gyotei_data_all(),
        }
    return dic


# xlsx download
def xlsx_download():
    # jwtg
    jwtg = eval(request.form["jwtg"])

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error != "error":
        # file create

        # create in memory
        output = io.BytesIO()

        # workbook
        book = xlsxwriter.Workbook(output, {"in_memory": True})

        # cell format dic
        cf_dic = mod_xlsxwriter.mz_cf(book)

        # sql sta
        sta_data = mod_sta.mz_gyotei_xlsx()

        for dt in sta_data:
            # init
            sta_cd = dt["sta_cd"]
            sta_name = dt["sta_name"]

            # sheet create
            sheet = book.add_worksheet(sta_name)

            # title
            sheet = mst_gyotei_xlsx.mz_title(sheet, cf_dic)

            # data
            sheet = mst_gyotei_xlsx.mz_data(sheet, sta_cd, cf_dic)

        # file close

        # close workbook
        book.close()

        # rewind the buffer
        output.seek(0)

    # create xlsx
    create_file = output.getvalue()
    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    file_name_temp = "業務提携リスト.xlsx"
    file_name = urllib.parse.quote(file_name_temp)
    return create_file, mime_type, file_name


def modal_exe():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    dic_modal = obj["dic_modal"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    google_account_email = base_data["google_account_email"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "gyotei_data_all": [],
        }
    else:
        # sql write
        modal_exe_sql(dic_modal, google_account_email, jwtg)

        dic = {
            "level_error": level_error,
            "gyotei_data_all": mod_gyotei.mz_gyotei_data_find(),
        }
    return dic


def modal_exe_sql(dic_modal, google_account_email, jwtg):
    # get
    mode = dic_modal["mode"]
    id = int(dic_modal["id"])
    update_email = google_account_email

    # edit
    if mode == "edit":
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = (
                "UPDATE sql_gyotei SET "
                + " sort = %s,"
                + " onoff_cd = %s,"
                + " gyotei_cd = %s,"
                + " kanri_cd = %s,"
                + " section_cd = %s,"
                + " staff_cd = %s,"
                + " name = %s,"
                + " name_kana = %s,"
                + " name_simple = %s,"
                + " name_simple_len = %s,"
                + " kana1moji = %s,"
                + " fee_gyotei = %s,"
                + " fee_staff1 = %s,"
                + " fee_staff2 = %s,"
                + " fee_staff3 = %s,"
                + " gensen_cd = %s,"
                + " pay_kikan = %s,"
                + " kojo_fee = %s,"
                + " com_per_sta = %s,"
                + " keiri_list_onoff = %s,"
                + " invoice_sta = %s,"
                + " bank_name = %s,"
                + " bank_branch = %s,"
                + " bank_kind = %s,"
                + " bank_account = %s,"
                + " bank_account_name = %s,"
                + " memo = %s,"
                + " update_email = %s"
                + " WHERE"
                + " id = "
                + str(id)
                + ";"
            )
            cur = sql_con.cursor()
            cur.execute(
                sql,
                (
                    int(dic_modal["sort"]),
                    dic_modal["onoff_cd"],
                    dic_modal["gyotei_cd"],
                    int(dic_modal["kanri_cd"]),
                    dic_modal["section_cd"],
                    dic_modal["staff_cd"],
                    dic_modal["name"],
                    dic_modal["name_kana"],
                    dic_modal["name_simple"],
                    int(dic_modal["name_simple_len"]),
                    dic_modal["kana1moji"],
                    int(dic_modal["fee_gyotei"]),
                    int(dic_modal["fee_staff1"]),
                    int(dic_modal["fee_staff2"]),
                    int(dic_modal["fee_staff3"]),
                    dic_modal["gensen_cd"],
                    int(dic_modal["pay_kikan"]),
                    int(dic_modal["kojo_fee"]),
                    dic_modal["com_per_sta"],
                    dic_modal["keiri_list_onoff"],
                    dic_modal["invoice_sta"],
                    dic_modal["bank_name"],
                    dic_modal["bank_branch"],
                    dic_modal["bank_kind"],
                    dic_modal["bank_account"],
                    dic_modal["bank_account_name"],
                    dic_modal["memo"],
                    update_email,
                ),
            )
            sql_con.commit()

    # add
    if mode == "add":
        # 最初に下記にあるサブルーチンを実行
        gyotei_cd, kanri_cd = mst_gyotei_modal_exe_add_cd_create(dic_modal["section_cd"])

        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = """
            INSERT INTO sql_gyotei (
                sort,
                onoff_cd,
                gyotei_cd,
                kanri_cd,
                section_cd,
                staff_cd,
                name,
                name_kana,
                name_simple,
                name_simple_len,
                kana1moji,
                fee_gyotei,
                fee_staff1,
                fee_staff2,
                fee_staff3,
                gensen_cd,
                pay_kikan,
                kojo_fee,
                com_per_sta,
                keiri_list_onoff,
                invoice_sta,
                bank_name,
                bank_branch,
                bank_kind,
                bank_account,
                bank_account_name,
                memo,
                update_email
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            );
            """
            cur = sql_con.cursor()
            cur.execute(
                sql,
                (
                    int(dic_modal["sort"]),
                    dic_modal["onoff_cd"],
                    gyotei_cd,
                    kanri_cd,
                    dic_modal["section_cd"],
                    dic_modal["staff_cd"],
                    dic_modal["name"],
                    dic_modal["name_kana"],
                    dic_modal["name_simple"],
                    int(dic_modal["name_simple_len"]),
                    dic_modal["kana1moji"],
                    int(dic_modal["fee_gyotei"]),
                    int(dic_modal["fee_staff1"]),
                    int(dic_modal["fee_staff2"]),
                    int(dic_modal["fee_staff3"]),
                    dic_modal["gensen_cd"],
                    int(dic_modal["pay_kikan"]),
                    int(dic_modal["kojo_fee"]),
                    dic_modal["com_per_sta"],
                    dic_modal["keiri_list_onoff"],
                    dic_modal["invoice_sta"],
                    dic_modal["bank_name"],
                    dic_modal["bank_branch"],
                    dic_modal["bank_kind"],
                    dic_modal["bank_account"],
                    dic_modal["bank_account_name"],
                    dic_modal["memo"],
                    update_email,
                ),
            )
            sql_con.commit()

    # del
    if mode == "del":
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = "DELETE FROM sql_gyotei WHERE id = %s"
            cur = sql_con.cursor()
            cur.execute(sql, (id,))
            sql_con.commit()

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name + "_" + mode
    mod_base.mz_base(9, jwtg, acc_page_name)

    return


# 新規作成時に gyotei_cd, kanri_cd 作成する
def mst_gyotei_modal_exe_add_cd_create(section_cd):
    # gyotei_cd 作成
    sql = "SELECT * FROM sql_gyotei ORDER BY id DESC LIMIT 0, 1;"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        gyotei_cd = int(dt["gyotei_cd"]) + 1

    # kanri_cd 作成

    # 東京
    if section_cd == "1":
        sql = "SELECT * FROM sql_gyotei WHERE section_cd = '1' AND kanri_cd != 9999 ORDER BY kanri_cd DESC LIMIT 0, 1;"
        sql_data = sql_config.mz_sql(sql)
        for dt in sql_data:
            kanri_cd = int(dt["kanri_cd"]) + 1

    # 福岡
    if section_cd == "2":
        sql = "SELECT * FROM sql_gyotei WHERE section_cd = '2' AND kanri_cd != 9999 ORDER BY kanri_cd DESC LIMIT 0, 1;"
        sql_data = sql_config.mz_sql(sql)
        for dt in sql_data:
            kanri_cd = int(dt["kanri_cd"]) + 1

    # 熊本1
    if section_cd == "3":
        sql = "SELECT * FROM sql_gyotei WHERE section_cd = '3' AND kanri_cd != 9999 ORDER BY kanri_cd DESC LIMIT 0, 1;"
        sql_data = sql_config.mz_sql(sql)
        for dt in sql_data:
            kanri_cd = int(dt["kanri_cd"]) + 1

    # 熊本2
    if section_cd == "4":
        sql = "SELECT * FROM sql_gyotei WHERE section_cd = '4' AND kanri_cd != 9999 ORDER BY kanri_cd DESC LIMIT 0, 1;"
        sql_data = sql_config.mz_sql(sql)
        for dt in sql_data:
            kanri_cd = int(dt["kanri_cd"]) + 1

    # 九州統括 - ここが特殊
    if section_cd == "5":
        select_from1 = "SELECT * FROM sql_gyotei"
        where1 = "WHERE kanri_cd >= 2001 AND kanri_cd <= 2999 AND kanri_cd != 9999 ORDER BY kanri_cd DESC LIMIT 0, 1;"
        sql = select_from1 + where1
        sql_data = sql_config.mz_sql(sql)
        for dt in sql_data:
            kanri_cd = int(dt["kanri_cd"]) + 1

    return gyotei_cd, kanri_cd
