import sys
from flask import request
from _mod import mod_base, sql_config
from _mod_fis import mod_sta, mod_cat, mod_coltd


def mst_coltd():
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
            "cat_data_all": [],
            "coltd_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "sta_data_all": mod_sta.mz_sta_all(),
            "cat_data_all": mod_cat.mz_cat_data_all(),
            "coltd_data_all": mod_coltd.mz_coltd_data_find(),
        }
    return dic


def mst_coltd_modal_exe():
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
            "coltd_data_all": [],
        }
    else:
        # sql write
        mst_coltd_modal_exe_sql(dic_modal, google_account_email, jwtg)

        dic = {
            "level_error": level_error,
            "coltd_data_all": mod_coltd.mz_coltd_data_find(),
        }
    return dic


def mst_coltd_modal_exe_sql(dic_modal, google_account_email, jwtg):
    # get
    mode = dic_modal["mode"]
    id = int(dic_modal["id"])
    update_email = google_account_email

    # edit
    if mode == "edit":
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = (
                "UPDATE sql_coltd SET "
                + " onoff_cd = %s,"
                + " nttgw_data = %s,"
                + " sort = %s,"
                + " cat_cd = %s,"
                + " coltd_cd = %s,"
                + " name = %s,"
                + " name_simple = %s,"
                + " name_simple_len = %s,"
                + " kaime = %s,"
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
                    dic_modal["onoff_cd"],
                    int(dic_modal["nttgw_data"]),
                    int(dic_modal["sort"]),
                    dic_modal["cat_cd"],
                    dic_modal["coltd_cd"],
                    dic_modal["name"],
                    dic_modal["name_simple"],
                    int(dic_modal["name_simple_len"]),
                    dic_modal["kaime"],
                    dic_modal["memo"],
                    update_email,
                ),
            )
            sql_con.commit()

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name + "_" + mode
    mod_base.mz_base(9, jwtg, acc_page_name)

    return
