import sys
from flask import request
from _mod import mod_base, sql_config


def fee_store_sch():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    sch_syoken_cd_main = obj["sch_syoken_cd_main"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "fee_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "fee_data": fee_data_res(sch_syoken_cd_main),
        }
    return dic


def fee_data_res(sch_syoken_cd_main):
    sql = """
        SELECT * FROM sql_fee_store
        WHERE syoken_cd_main = '{sch_syoken_cd_main}' ORDER BY nyu_date, coltd_cd, syoken_cd_main;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def fee_store_modal_exe():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    dic_modal = obj["dic_modal"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
        }
    else:
        # sql write
        fee_store_modal_exe_sql(dic_modal, jwtg)

        dic = {
            "level_error": level_error,
        }
    return dic


def fee_store_modal_exe_sql(dic_modal, jwtg):
    # get
    mode = dic_modal["mode"]
    id = int(dic_modal["id"])

    # edit
    if mode == "edit":
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = (
                "UPDATE sql_fee_store SET "
                + " nyu_nendo = %s,"
                + " nyu_date = %s,"
                + " cat_cd = %s,"
                + " coltd_cd = %s,"
                + " syoken_cd_main = %s,"
                + " syoken_cd_sub = %s,"
                + " fee_withtax = %s,"
                + " fee_notax = %s,"
                + " fee_tax_num = %s,"
                + " fee_tax_per = %s,"
                + " kaime = %s,"
                + " first_next_year = %s"
                + " WHERE"
                + " id = "
                + str(id)
                + ";"
            )
            cur = sql_con.cursor()
            cur.execute(
                sql,
                (
                    int(dic_modal["nyu_nendo"]),
                    int(dic_modal["nyu_date"]),
                    int(dic_modal["cat_cd"]),
                    dic_modal["coltd_cd"],
                    dic_modal["syoken_cd_main"],
                    dic_modal["syoken_cd_sub"],
                    int(dic_modal["fee_withtax"]),
                    int(dic_modal["fee_notax"]),
                    int(dic_modal["fee_tax_num"]),
                    int(dic_modal["fee_tax_per"]),
                    dic_modal["kaime"],
                    int(dic_modal["first_next_year"]),
                ),
            )
            sql_con.commit()

    # del
    if mode == "del":
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = "DELETE FROM sql_fee_store WHERE id = %s"
            cur = sql_con.cursor()
            cur.execute(sql, (id,))
            sql_con.commit()

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name + "_" + mode
    mod_base.mz_base(9, jwtg, acc_page_name)

    return
