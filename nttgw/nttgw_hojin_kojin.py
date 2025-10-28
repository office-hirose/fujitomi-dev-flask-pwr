# ------------------------------------------------------------------------
#  nttgw_hojin_kojin.py
#  |--nttgw_hojin_kojin              - 画面作成
#  |--nttgw_hojin_kojin_list         - list
# ------------------------------------------------------------------------
import sys
import datetime
from flask import request
from _mod import mod_base, mod_datetime, mod_onoff, sql_config
from _mod_fis import mod_hojin_kojin


def nttgw_hojin_kojin():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "sel_create_data": [],
            "sel_create_date": "",
            "sel_hojin_kojin_data": [],
        }
    else:
        # create_date
        datetime_now = datetime.datetime.now()
        datetime_today = datetime_now + datetime.timedelta(hours=9, days=0)
        sel_create_date = mod_datetime.mz_dt2str_yymmdd_hyphen(datetime_today)

        dic = {
            "level_error": level_error,
            "sel_create_data": mod_onoff.onoff_data(),
            "sel_create_date": sel_create_date,
            "sel_hojin_kojin_data": mod_hojin_kojin.mz_hojin_kojin_data_all(),
        }
    return dic


# list
def nttgw_hojin_kojin_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    sel_hojin_kojin_cd = obj["sel_hojin_kojin_cd"]
    sel_create_date_onoff = int(obj["sel_create_date_onoff"])
    sel_create_date = mod_datetime.mz_str2num_hyphen_zero_ari(obj["sel_create_date"])

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "hojin_kojin_data": [],
        }
    else:
        # sql
        hojin_kojin_data = mz_list(sel_hojin_kojin_cd, sel_create_date_onoff, sel_create_date)

        dic = {
            "level_error": level_error,
            "hojin_kojin_data": hojin_kojin_data,
        }
    return dic


# update
def nttgw_hojin_kojin_update():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    fis_cd = obj["fis_cd"]
    exe_hojin_kojin_cd = obj["exe_hojin_kojin_cd"]

    sel_hojin_kojin_cd = obj["sel_hojin_kojin_cd"]
    sel_create_date_onoff = int(obj["sel_create_date_onoff"])
    sel_create_date = mod_datetime.mz_str2num_hyphen_zero_ari(obj["sel_create_date"])

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "hojin_kojin_data": [],
        }
    else:
        # sql update
        mz_update(fis_cd, exe_hojin_kojin_cd)

        # sql list
        hojin_kojin_data = mz_list(sel_hojin_kojin_cd, sel_create_date_onoff, sel_create_date)

        dic = {
            "level_error": level_error,
            "hojin_kojin_data": hojin_kojin_data,
        }
    return dic


# list sql
def mz_list(sel_hojin_kojin_cd, sel_create_date_onoff, sel_create_date):
    sql1 = """
        SELECT
            os.fis_cd,
            os.create_date,
            os.syoken_cd_main,
            os.syoken_cd_sub,
            os.kei_name,
            os.kei_name_nospace,
            os.hojin_kojin_cd
        FROM
            sql_order_store AS os
    """
    if sel_create_date_onoff == 1:
        sql2 = (
            " WHERE os.create_date = "
            + str(sel_create_date)
            + " AND os.hojin_kojin_cd = "
            + '"'
            + str(sel_hojin_kojin_cd)
            + '"'
        )
    if sel_create_date_onoff == 2:
        sql2 = " WHERE os.hojin_kojin_cd = " + '"' + str(sel_hojin_kojin_cd) + '"'
    sql3 = " ORDER BY os.kei_name_nospace, os.syoken_cd_main, os.syoken_cd_sub"
    sql4 = " LIMIT 0, 100;"
    sql = sql1 + sql2 + sql3 + sql4
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# sql update
def mz_update(fis_cd, exe_hojin_kojin_cd):
    sql = (
        "UPDATE sql_order_store SET hojin_kojin_cd = "
        + '"'
        + str(exe_hojin_kojin_cd)
        + '"'
        + " WHERE fis_cd = "
        + '"'
        + str(fis_cd)
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

    return
