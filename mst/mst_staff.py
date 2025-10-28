import sys
from flask import request
from _mod import mod_base, sql_config, mod_lm, mod_lm_level
from _mod_fis import mod_sta, mod_section, mod_staff, mod_salary


def mst_staff():
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
            "salary_kind_data_all": [],
            "lm_data": [],
            "level_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "sta_data_all": mod_sta.mz_sta_all(),
            "section_data_all": mod_section.mz_section_data_on(),
            "staff_data_all": mod_staff.mz_staff_data_all(),
            "salary_kind_data_all": mod_salary.mz_salary_kind_data_all(),
            "lm_data": mod_lm.fs_lm_data(),
            "level_data": mod_lm_level.fs_lm_level_data(),
        }
    return dic


def mst_staff_modal_exe():
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
            "staff_data_all": [],
        }
    else:
        # sql write
        mst_staff_modal_exe_sql(dic_modal, google_account_email, jwtg)

        dic = {
            "level_error": level_error,
            "staff_data_all": mod_staff.mz_staff_data_find(),
        }
    return dic


def mst_staff_modal_exe_sql(dic_modal, google_account_email, jwtg):
    # get
    mode = dic_modal["mode"]
    id = int(dic_modal["id"])
    update_email = google_account_email

    # edit
    if mode == "edit":
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = (
                "UPDATE sql_staff SET "
                + " onoff_cd = %s,"
                + " sales_cd = %s,"
                + " sort = %s,"
                + " staff_email = %s,"
                + " staff_cd = %s,"
                + " section_cd = %s,"
                + " section_cd_email = %s,"
                + " name = %s,"
                + " name_kana = %s,"
                + " name_simple = %s,"
                + " name_simple_len = %s,"
                + " kana1moji = %s,"
                + " nttgw_send_email_onoff = %s,"
                + " send_email_onoff = %s,"
                + " send_email = %s,"
                + " pay_rate = %s,"
                + " kojo_fee = %s,"
                + " memo = %s,"
                + " memo_pass = %s,"
                + " w3_text_color = %s,"
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
                    dic_modal["onoff_cd"],
                    dic_modal["sales_cd"],
                    int(dic_modal["sort"]),
                    dic_modal["staff_email"],
                    dic_modal["staff_cd"],
                    dic_modal["section_cd"],
                    dic_modal["section_cd_email"],
                    dic_modal["name"],
                    dic_modal["name_kana"],
                    dic_modal["name_simple"],
                    int(dic_modal["name_simple_len"]),
                    dic_modal["kana1moji"],
                    dic_modal["nttgw_send_email_onoff"],
                    dic_modal["send_email_onoff"],
                    dic_modal["send_email"],
                    int(dic_modal["pay_rate"]),
                    int(dic_modal["kojo_fee"]),
                    dic_modal["memo"],
                    dic_modal["memo_pass"],
                    dic_modal["w3_text_color"],
                    update_email,
                ),
            )
            sql_con.commit()

    # add
    if mode == "add":
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = """
            INSERT INTO sql_staff (
                onoff_cd,
                sales_cd,
                sort,
                staff_email,
                staff_cd,
                section_cd,
                section_cd_email,
                name,
                name_kana,
                name_simple,
                name_simple_len,
                kana1moji,
                nttgw_send_email_onoff,
                send_email_onoff,
                send_email,
                pay_rate,
                kojo_fee,
                memo,
                memo_pass,
                w3_text_color,
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
                %s
            );
            """
            cur = sql_con.cursor()
            cur.execute(
                sql,
                (
                    dic_modal["onoff_cd"],
                    dic_modal["sales_cd"],
                    int(dic_modal["sort"]),
                    dic_modal["staff_email"],
                    dic_modal["staff_cd"],
                    dic_modal["section_cd"],
                    dic_modal["section_cd_email"],
                    dic_modal["name"],
                    dic_modal["name_kana"],
                    dic_modal["name_simple"],
                    int(dic_modal["name_simple_len"]),
                    dic_modal["kana1moji"],
                    dic_modal["nttgw_send_email_onoff"],
                    dic_modal["send_email_onoff"],
                    dic_modal["send_email"],
                    int(dic_modal["pay_rate"]),
                    int(dic_modal["kojo_fee"]),
                    dic_modal["memo"],
                    dic_modal["memo_pass"],
                    dic_modal["w3_text_color"],
                    update_email,
                ),
            )
            sql_con.commit()

    # del
    if mode == "del":
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = "DELETE FROM sql_staff WHERE id = %s"
            cur = sql_con.cursor()
            cur.execute(sql, (id,))
            sql_con.commit()

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name + "_" + mode
    mod_base.mz_base(9, jwtg, acc_page_name)

    return
