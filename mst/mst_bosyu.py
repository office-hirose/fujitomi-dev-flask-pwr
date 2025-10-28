import sys
from flask import request
from _mod import mod_base, sql_config
from _mod_fis import mod_cat, mod_bosyu


def mst_bosyu():
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
            "cat_data_all": [],
            "coltd_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "cat_data_all": mod_cat.mz_cat_data_all(),
            "bosyu_data_all": mod_bosyu.mz_bosyu_data_find(),
        }
    return dic


def mst_bosyu_modal_exe():
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
            "bosyu_data_all": mod_bosyu.mz_bosyu_data_find(),
        }
    else:
        # sql write
        mst_bosyu_modal_exe_sql(dic_modal, google_account_email, jwtg)

        dic = {
            "level_error": level_error,
            "bosyu_data_all": mod_bosyu.mz_bosyu_data_find(),
        }
    return dic


def mst_bosyu_modal_exe_sql(dic_modal, google_account_email, jwtg):
    # get
    mode = dic_modal["mode"]
    id = int(dic_modal["id"])
    update_email = google_account_email

    # edit
    if mode == "edit":
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = (
                "UPDATE sql_bosyu SET "
                + " cat_cd = %s,"
                + " bosyu_cd = %s,"
                + " name_simple = %s,"
                + " staff_cd = %s,"
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
                    dic_modal["cat_cd"],
                    dic_modal["bosyu_cd"],
                    dic_modal["name_simple"],
                    dic_modal["staff_cd"],
                    dic_modal["memo"],
                    update_email,
                ),
            )
            sql_con.commit()

    # add
    if mode == "add":
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = """
            INSERT INTO sql_bosyu (
                cat_cd,
                bosyu_cd,
                name_simple,
                staff_cd,
                memo,
                update_email
            ) VALUES (
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
                    dic_modal["cat_cd"],
                    dic_modal["bosyu_cd"],
                    dic_modal["name_simple"],
                    dic_modal["staff_cd"],
                    dic_modal["memo"],
                    update_email,
                ),
            )
            sql_con.commit()

    # del
    if mode == "del":
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = "DELETE FROM sql_bosyu WHERE id = %s"
            cur = sql_con.cursor()
            cur.execute(sql, (id,))
            sql_con.commit()

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name + "_" + mode
    mod_base.mz_base(9, jwtg, acc_page_name)

    return
