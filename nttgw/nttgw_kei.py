# ------------------------------------------------------------------------
#  nttgw_kei.py
#  |--nttgw_kei       - 画面作成
#  |--nttgw_kei_list  - list
#  |--nttgw_kei_modal - modal, update
# ------------------------------------------------------------------------
import sys
from flask import request
from _mod import mod_base, sql_config
from _mod_fis import mod_nttgw_common, mod_coltd


def nttgw_kei():
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
            "coltd_data": [],
            "sel_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "user_email": user_email,
            "coltd_data": mod_coltd.mz_coltd_data_all(),
            "sel_data": mod_nttgw_common.mz_sel_imp_file_name(),
        }
    return dic


# 選択したファイル名からリスト表示
def nttgw_kei_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    sel_id = int(obj["sel_id"])
    list_type = obj["list_type"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "imp_file_name": "",
            "kei_data": [],
        }
    else:
        # sql
        imp_file_name = mod_nttgw_common.mz_find_imp_file_name(sel_id)

        if list_type == "list":
            kei_data = mz_kei_data_list(imp_file_name)

        if list_type == "space_del":
            kei_data = mz_kei_data_space_del(imp_file_name)

        if list_type == "special_fnd":
            kei_data = mz_kei_data_special_fnd(imp_file_name)

        if list_type == "special_rep":
            kei_data = mz_kei_data_special_rep(imp_file_name)

        dic = {
            "level_error": level_error,
            "imp_file_name": imp_file_name,
            "kei_data": kei_data,
        }
    return dic


# list
def mz_kei_data_list(imp_file_name):
    sql = (
        "SELECT * FROM sql_nttgw_dat WHERE imp_file_name = "
        + "'"
        + imp_file_name
        + "'"
        + " ORDER BY coltd_cd, syoken_cd_main;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 末尾余白削除
def mz_kei_data_space_del(imp_file_name):
    sp1 = '"' + "　" + '"'
    sp2 = '"' + " " + '"'

    sql = (
        ""
        + "UPDATE sql_nttgw_dat"
        + " SET"
        + " kei_name = TRIM(TRAILING "
        + sp1
        + " FROM kei_name),"
        + " kei_name_hira = TRIM(TRAILING "
        + sp1
        + " FROM kei_name_hira),"
        + " kei_name_kata = TRIM(TRAILING "
        + sp1
        + " FROM kei_name_kata),"
        + " kei_address = TRIM(TRAILING "
        + sp1
        + " FROM kei_address)"
        + " WHERE"
        + " imp_file_name = "
        + "'"
        + imp_file_name
        + "'"
        + ";"
    )
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        cur.execute(
            sql,
        )
        sql_con.commit()

    sql = (
        ""
        + "UPDATE sql_nttgw_dat"
        + " SET"
        + " kei_name = TRIM(TRAILING "
        + sp2
        + " FROM kei_name),"
        + " kei_name_hira = TRIM(TRAILING "
        + sp2
        + " FROM kei_name_hira),"
        + " kei_name_kata = TRIM(TRAILING "
        + sp2
        + " FROM kei_name_kata),"
        + " kei_address = TRIM(TRAILING "
        + sp2
        + " FROM kei_address)"
        + " WHERE"
        + " imp_file_name = "
        + "'"
        + imp_file_name
        + "'"
        + ";"
    )
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        cur.execute(
            sql,
        )
        sql_con.commit()

    sql_data = mz_kei_data_list(imp_file_name)
    return sql_data


# 特殊文字検索　※現在はレコード全件を検索している
def mz_kei_data_special_fnd(imp_file_name):
    sql = """
    SELECT * FROM sql_nttgw_dat WHERE
    kei_name LIKE "%（株）%" or
    kei_name LIKE "%（有）%" or
    kei_name LIKE "%(株)%" or
    kei_name LIKE "%(有)%" or
    kei_name LIKE "%㈱%" or
    kei_name LIKE "%㈲%" or
    kei_name LIKE "%＊%" or
    kei_name LIKE "%？%" or
    kei_name LIKE "%＿%"
    ORDER BY coltd_cd, syoken_cd_main;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 特殊文字置換 ※現在はレコード全件を実行している
def mz_kei_data_special_rep(imp_file_name):
    sql = """
    UPDATE sql_nttgw_dat
    SET
    kei_name = REPLACE(kei_name, "＊", "　"),
    kei_name = REPLACE(kei_name, "（株）", "株式会社"),
    kei_name = REPLACE(kei_name, "（有）", "有限会社"),
    kei_name = REPLACE(kei_name, "(株)", "株式会社"),
    kei_name = REPLACE(kei_name, "(有)", "有限会社"),
    kei_name = REPLACE(kei_name, "㈱", "株式会社"),
    kei_name = REPLACE(kei_name, "㈲", "有限会社"),
    kei_name = REPLACE(kei_name, " ", "　");
    """
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        cur.execute(
            sql,
        )
        sql_con.commit()

    # sql_data = mz_kei_data_list(imp_file_name)
    sql_data = mz_kei_data_special_fnd(imp_file_name)

    return sql_data


# modal open
def nttgw_kei_modal_open():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    coltd_cd = obj["coltd_cd"]
    kei_name_hira = obj["kei_name_hira"]
    imp_file_name = obj["imp_file_name"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "start_kouho_data": [],
            "kei_name_start_int_kouho": 0,
        }
    else:
        # sql 候補データ
        sql = (
            "SELECT min(kei_name_start) AS kei_name_start FROM sql_nttgw_dat"
            + " WHERE coltd_cd = "
            + '"'
            + coltd_cd
            + '"'
            + " GROUP BY kei_name_start"
            + " ORDER BY kei_name_start;"
        )
        start_kouho_data = sql_config.mz_sql(sql)

        # 過去からの開始位置候補
        hira = (kei_name_hira.replace(" ", "")).replace("　", "")
        sql = (
            "SELECT kei_name_start, kei_name_hira FROM sql_nttgw_dat"
            + " WHERE kei_name_hira = "
            + "'"
            + hira
            + "'"
            + " AND coltd_cd = "
            + '"'
            + coltd_cd
            + '"'
            + " AND imp_file_name != "
            + "'"
            + imp_file_name
            + "'"
            + " ORDER BY id DESC"
            + ";"
        )
        sql_data = sql_config.mz_sql(sql)
        sql_data_len = len(sql_data)
        if sql_data_len <= 1:
            kei_name_start_int_kouho = 0
        else:
            cnt = 0
            for dt in sql_data:
                cnt += 1
                if cnt == 2:
                    kei_name_start_int_kouho = dt["kei_name_start"]
                    break

        dic = {
            "level_error": level_error,
            "start_kouho_data": start_kouho_data,
            "kei_name_start_int_kouho": kei_name_start_int_kouho,
        }
    return dic


# modal update
def nttgw_kei_modal_update():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    sel_id = int(obj["sel_id"])
    id = int(obj["id"])
    update_type = obj["update_type"]
    update_value = obj["update_value"]
    res_list_type = obj["res_list_type"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "kei_data": [],
        }
    else:
        if update_type == "kei_name_start_kouho":
            sql = (
                "UPDATE sql_nttgw_dat SET"
                + " kei_name_start = "
                + str(update_value)
                + ","
                + " kei_name = SUBSTR(temp_text, kei_name_start, 30)"
                + " WHERE id = "
                + str(id)
                + ";"
            )

        if update_type == "kei_name_start_value":
            sql = (
                "UPDATE sql_nttgw_dat SET"
                + " kei_name_start = "
                + str(update_value)
                + ","
                + " kei_name = SUBSTR(temp_text, kei_name_start, 30)"
                + " WHERE id = "
                + str(id)
                + ";"
            )

        if update_type == "kei_name_input_value":
            sql = (
                "UPDATE sql_nttgw_dat SET" + " kei_name = " + '"' + update_value + '"' + " WHERE id = " + str(id) + ";"
            )

        sql_con = sql_config.mz_sql_con()
        with sql_con:
            cur = sql_con.cursor()
            cur.execute(
                sql,
            )
            sql_con.commit()

        # 余白削除
        sp1 = '"' + "　" + '"'
        sp2 = '"' + " " + '"'

        sql = (
            ""
            + "UPDATE sql_nttgw_dat"
            + " SET kei_name = TRIM(TRAILING "
            + sp1
            + " FROM kei_name)"
            + " WHERE id = "
            + str(id)
            + ";"
        )
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            cur = sql_con.cursor()
            cur.execute(
                sql,
            )
            sql_con.commit()

        sql = (
            ""
            + "UPDATE sql_nttgw_dat"
            + " SET kei_name = TRIM(TRAILING "
            + sp2
            + " FROM kei_name)"
            + " WHERE id = "
            + str(id)
            + ";"
        )
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            cur = sql_con.cursor()
            cur.execute(
                sql,
            )
            sql_con.commit()

        # sql list
        imp_file_name = mod_nttgw_common.mz_find_imp_file_name(sel_id)

        if res_list_type == "normal":
            kei_data = mz_kei_data_list(imp_file_name)
        if res_list_type == "special":
            kei_data = mz_kei_data_special_fnd(imp_file_name)

        dic = {
            "level_error": level_error,
            "kei_data": kei_data,
        }
    return dic
