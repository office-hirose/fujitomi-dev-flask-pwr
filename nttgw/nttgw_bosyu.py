# ------------------------------------------------------------------------
#  nttgw_bosyu.py
#  |--nttgw_bosyu        - 画面作成
#  |--nttgw_bosyu_update - set, update
# ------------------------------------------------------------------------
import sys
from flask import request
from _mod import mod_base, sql_config
from _mod_fis import mod_nttgw_common


def nttgw_bosyu():
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
            "sel_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "user_email": user_email,
            "sel_data": mod_nttgw_common.mz_sel_imp_file_name(),
        }
    return dic


def nttgw_bosyu_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    sel_id = int(obj["sel_id"])

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "bosyu_data_all": [],
        }
    else:
        # sql
        imp_file_name = mod_nttgw_common.mz_find_imp_file_name(sel_id)
        bosyu_data_all = mz_bosyu_data_all(imp_file_name)

        dic = {
            "level_error": level_error,
            "bosyu_data_all": bosyu_data_all,
        }
    return dic


# 1 record update
def nttgw_bosyu_update():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    id = int(obj["id"])
    cat_cd = int(obj["cat_cd"])
    sel_id = int(obj["sel_id"])

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "bosyu_data_all": [],
        }
    else:
        # 対象のidで検索して、募集人CDが含まれているか確認、結果 no_hit or hit, 開始位置
        bosyu_cd_hit, bosyu_cd_start = mz_bosyu_cd_search(id, cat_cd)

        # bosyu_cd_start update
        mz_bosyu_cd_start_update(id, bosyu_cd_start)

        # hit, bosyu_cd update
        if bosyu_cd_hit == "hit":
            mz_bosyu_cd_update(id)

        # sql
        imp_file_name = mod_nttgw_common.mz_find_imp_file_name(sel_id)
        bosyu_data_all = mz_bosyu_data_all(imp_file_name)

        dic = {
            "level_error": level_error,
            "bosyu_data_all": bosyu_data_all,
        }
    return dic


# all records update
def nttgw_bosyu_update_all():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    sel_id = int(obj["sel_id"])

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "bosyu_data_all": [],
        }
    else:
        # sql, select records
        imp_file_name = mod_nttgw_common.mz_find_imp_file_name(sel_id)
        sql = "SELECT * " + "FROM sql_nttgw_dat " + "WHERE imp_file_name = " + "'" + imp_file_name + "'" + ";"
        print(sql)
        sql_data = sql_config.mz_sql(sql)
        print(sql_data)

        # 選択したファイル名のレコードを全て確認
        for dt in sql_data:

            # 対象のidで検索して、募集人CDが含まれているか確認、結果 no_hit or hit, 開始位置
            bosyu_cd_hit, bosyu_cd_start = mz_bosyu_cd_search(dt["id"], dt["cat_cd"])

            # bosyu_cd_start update
            mz_bosyu_cd_start_update(dt["id"], bosyu_cd_start)

            # hit, bosyu_cd update
            if bosyu_cd_hit == "hit":
                mz_bosyu_cd_update(dt["id"])

        # sql, list
        imp_file_name = mod_nttgw_common.mz_find_imp_file_name(sel_id)
        bosyu_data_all = mz_bosyu_data_all(imp_file_name)

        dic = {
            "level_error": level_error,
            "bosyu_data_all": bosyu_data_all,
        }
    return dic


# インポートファイル名からリスト全件取得
def mz_bosyu_data_all(imp_file_name):
    sql1 = """
        SELECT
            nttgw.id,
            nttgw.cat_cd,
            nttgw.coltd_cd,
            nttgw.syoken_cd_main,
            nttgw.bosyu_cd,
            nttgw.bosyu_cd_start,
            nttgw.bosyu_cd_len,
            SUBSTR(nttgw.temp_text, nttgw.bosyu_cd_start, nttgw.bosyu_cd_len) AS bosyu_cd_temp,
            CASE WHEN bosyu.name_simple IS NULL THEN 'empty' ELSE bosyu.name_simple END AS bosyu_name
        FROM sql_nttgw_dat AS nttgw
        LEFT JOIN sql_bosyu AS bosyu ON nttgw.bosyu_cd = bosyu.bosyu_cd
        """
    sql2 = " WHERE nttgw.imp_file_name = " + "'" + imp_file_name + "'"
    sql3 = " ORDER BY nttgw.bosyu_cd, nttgw.bosyu_cd_start, bosyu_cd_temp;"
    sql = sql1 + sql2 + sql3
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# temp_textの中に募集人コードが含まれているか検索する
def mz_bosyu_cd_search(id, cat_cd):
    # temp_text
    temp_text = ""
    sql = "SELECT temp_text FROM sql_nttgw_dat WHERE id = " + str(id) + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        temp_text = dt["temp_text"]

    # 募集人CD
    sql = "SELECT bosyu_cd FROM sql_bosyu WHERE cat_cd = " + '"' + str(cat_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)

    # like 検索、開始位置を検索
    bosyu_cd_hit = "no_hit"
    bosyu_cd_start = 9999

    for dt in sql_data:
        if dt["bosyu_cd"] in temp_text:
            bosyu_cd_hit = "hit"
            bosyu_cd_start = temp_text.find(dt["bosyu_cd"]) + 1
            break

    return bosyu_cd_hit, bosyu_cd_start


# bosyu_cd_start_update
def mz_bosyu_cd_start_update(id, bosyu_cd_start):
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = "UPDATE sql_nttgw_dat SET" + " bosyu_cd_start = " + str(bosyu_cd_start) + " WHERE id = " + str(id) + ";"
        cur = sql_con.cursor()
        cur.execute(
            sql,
        )
        sql_con.commit()
    return


# bosyu_cd_update
def mz_bosyu_cd_update(id):
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = (
            "UPDATE sql_nttgw_dat SET"
            + " bosyu_cd = SUBSTR(temp_text, bosyu_cd_start, bosyu_cd_len)"
            + " WHERE id = "
            + str(id)
            + ";"
        )
        cur = sql_con.cursor()
        cur.execute(
            sql,
        )
        sql_con.commit()
    return
