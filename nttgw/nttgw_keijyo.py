# ------------------------------------------------------------------------
#  nttgw_keijyo.py
#  |--nttgw_keijyo              - 画面作成
#  |--nttgw_keijyo_list         - list
#  |--nttgw_keijyo_update       - list update
# ------------------------------------------------------------------------
import sys
import datetime
from flask import request
from _mod import mod_base, mod_datetime, sql_config
from _mod_fis import mod_kei_nyu_pay


def nttgw_keijyo():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    user_email = base_data["google_account_email"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "user_email": "",
            "knp_data": [],
            "create_date": "",
        }
    else:
        knp_data = mod_kei_nyu_pay.mz_common_kei_sel(201904)
        create_date = mod_datetime.mz_dt2str_yymmdd_hyphen_jst(datetime.datetime.now())

        dic = {
            "level_error": level_error,
            "user_email": user_email,
            "knp_data": knp_data,
            "create_date": create_date,
        }
    return dic


# list
def nttgw_keijyo_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    create_date = obj["create_date"]
    kei_date_int = obj["kei_date_int"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "keijyo_data": [],
        }
    else:
        # sql, create_date, kei_date_int
        create_date = mod_datetime.mz_str2num_hyphen_zero_ari(create_date)
        keijyo_data = mz_keijyo_list(create_date, kei_date_int)

        dic = {
            "level_error": level_error,
            "keijyo_data": keijyo_data,
        }
    return dic


# update
def nttgw_keijyo_update():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    fis_cd = obj["fis_cd"]
    create_date = obj["create_date"]
    kei_date_int = int(obj["kei_date_int"])

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "keijyo_data": [],
        }
    else:
        # sql
        sql = (
            "UPDATE sql_order_store"
            + " SET keijyo_date = "
            + str(kei_date_int)
            + " WHERE fis_cd = "
            + '"'
            + fis_cd
            + '"'
            + ";"
        )
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            cur = sql_con.cursor()
            cur.execute(
                sql,
            )
            sql_con.commit()

        # sql, create_date, kei_date_int
        create_date = mod_datetime.mz_str2num_hyphen_zero_ari(create_date)
        keijyo_data = mz_keijyo_list(create_date, kei_date_int)

        dic = {
            "level_error": level_error,
            "keijyo_data": keijyo_data,
        }
    return dic


# sql list
def mz_keijyo_list(create_date, kei_date_int):
    sql1 = "SELECT * FROM sql_order_store"
    sql2 = (
        " WHERE exe_sta = "
        + '"'
        + "nttgw"
        + '"'
        + " AND create_date = "
        + str(create_date)
        + " AND keijyo_date != "
        + str(kei_date_int)
    )
    sql3 = " ORDER BY keijyo_date, coltd_cd, syoken_cd_main, syoken_cd_sub;"
    sql = sql1 + sql2 + sql3
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# # keijyo_date 変換するフィルター 202104 --> 2021-04
# def mz_keijyo_date_ft(keijyo_date):
#     if keijyo_date == 0:
#         dt_str = '0000-00'
#     else:
#         str_date = str(keijyo_date)
#         yy = str_date[0:4]
#         mm = str_date[4:6]
#         dt_str = yy + '-' + mm
#     return dt_str
