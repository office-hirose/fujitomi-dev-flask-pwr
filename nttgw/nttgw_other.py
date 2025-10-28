# ------------------------------------------------------------------------
#  nttgw_other.py
#  |--nttgw_other              - 画面作成
#  |--nttgw_other_list         - list
# ------------------------------------------------------------------------
import sys
import datetime
from flask import request
from _mod import mod_base, mod_datetime, sql_config


def nttgw_other():
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
            "create_date": 0,
        }
    else:
        # create_date
        datetime_now = datetime.datetime.now()
        datetime_today = datetime_now + datetime.timedelta(hours=9, days=0)
        create_date = mod_datetime.mz_dt2str_yymmdd_slash(datetime_today)

        dic = {
            "level_error": level_error,
            "user_email": user_email,
            "create_date": create_date,
        }
    return dic


# list
def nttgw_other_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    list_type = obj["list_type"]
    create_date = mod_datetime.mz_str2num_hyphen_zero_ari(obj["create_date"])

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "other_data": [],
        }
    else:
        # sql
        other_data = []

        if list_type == "list_kind_null":
            other_data = mz_list_kind_null(create_date)

        if list_type == "list_sub_null":
            other_data = mz_list_sub_null()

        if list_type == "list_pay_null":
            other_data = mz_list_pay_null()

    dic = {
        "level_error": base_data.get("level_error"),
        "other_data": other_data,
    }
    return dic


# 保険種類SUBがNULLのレコードを検索
def mz_list_kind_null(create_date):
    sql1 = """
        SELECT
            os.fis_cd,
            os.keijyo_date,
            os.coltd_cd,
            os.syoken_cd_main,
            os.syoken_cd_sub,
            os.kind_cd_main,
            os.kind_cd_sub,
            ks.kind_name_sub
        FROM
            sql_order_store AS os
            LEFT JOIN sql_kind_sub AS ks ON os.kind_cd_main = ks.kind_cd_main AND os.kind_cd_sub = ks.kind_cd_sub
    """
    sql2 = " WHERE os.create_date = " + str(create_date) + ' AND (os.kind_cd_sub = "" OR ks.kind_name_sub IS NULL)'
    sql3 = " ORDER BY os.kind_cd_main, os.kind_cd_sub;"
    sql = sql1 + sql2 + sql3
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 生保で証券番号の枝番が0000以外を検索
def mz_list_sub_null():
    sql = """
        SELECT
            fis_cd,
            keijyo_date,
            coltd_cd,
            syoken_cd_main,
            syoken_cd_sub,
            kind_cd_main,
            kind_cd_sub,
            '省略' AS kind_name_sub
        FROM
            sql_order_store
        WHERE
            cat_cd = "1" AND syoken_cd_sub != "0000"
        ORDER BY
            coltd_cd, syoken_cd_main;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# pay_num_cd = '' list
def mz_list_pay_null():
    sql = """
        SELECT
            fis_cd,
            keijyo_date,
            coltd_cd,
            syoken_cd_main,
            syoken_cd_sub,
            kind_cd_main,
            kind_cd_sub,
            '省略' AS kind_name_sub
        FROM
            sql_order_store
        WHERE
            pay_num_cd = ""
        ORDER BY
            coltd_cd, syoken_cd_main;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# kind modal open
def nttgw_other_kind_modal_open():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    fis_cd = obj["fis_cd"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "sql_data": [],
            "modal_order_data": [],
        }
    else:
        # sql modal_main_data
        sql1 = """
            SELECT
            os.fis_cd AS fis_cd,
            os.coltd_cd AS coltd_cd,
            col.name_simple AS coltd_name,
            os.syoken_cd_main AS syoken_cd_main,
            os.syoken_cd_sub AS syoken_cd_sub,
            os.kind_cd_main AS kind_cd_main,
            os.kind_cd_sub AS kind_cd_sub,
            km.kind_name_main AS kind_name_main
            FROM sql_order_store AS os
            LEFT JOIN sql_coltd AS col ON col.coltd_cd = os.coltd_cd
            LEFT JOIN sql_kind_main AS km ON km.coltd_cd = os.coltd_cd AND km.kind_cd_main = os.kind_cd_main
        """
        sql2 = " WHERE os.fis_cd = " + "'" + fis_cd + "'" + ";"
        sql = sql1 + sql2
        modal_main_data = sql_config.mz_sql(sql)

        for dt in modal_main_data:
            syoken_cd_main = dt["syoken_cd_main"]
            coltd_cd = dt["coltd_cd"]
            kind_cd_main = dt["kind_cd_main"]

        # sql modal_order_data
        sql1 = """
            SELECT
            os.syoken_cd_main AS syoken_cd_main,
            os.syoken_cd_sub AS syoken_cd_sub,
            os.kind_cd_main AS kind_cd_main,
            os.kind_cd_sub AS kind_cd_sub,
            ks.kind_name_main AS kind_name_main,
            ks.kind_name_sub AS kind_name_sub
            FROM sql_order_store AS os
            LEFT JOIN sql_kind_sub AS ks ON
            ks.coltd_cd = os.coltd_cd AND
            ks.kind_cd_main = os.kind_cd_main AND
            ks.kind_cd_sub = os.kind_cd_sub
        """
        sql2 = " WHERE os.syoken_cd_main = " + "'" + syoken_cd_main + "'"
        sql3 = " ORDER BY os.syoken_cd_sub;"
        sql = sql1 + sql2 + sql3
        modal_order_data = sql_config.mz_sql(sql)

        # sql modal_kind_sub_data
        sql1 = """
            SELECT
            kind_cd_main,
            kind_cd_sub,
            kind_name_sub
            FROM sql_kind_sub
        """
        sql2 = " WHERE coltd_cd = " + "'" + coltd_cd + "'"
        sql3 = " AND onoff_cd = " + "'on'"
        sql4 = " AND coltd_cd = " + "'" + coltd_cd + "'"
        sql5 = " AND kind_cd_main = " + "'" + kind_cd_main + "'"
        sql6 = " ORDER BY sort;"
        sql = sql1 + sql2 + sql3 + sql4 + sql5 + sql6
        modal_kind_sub_data = sql_config.mz_sql(sql)

        # dic
        dic = {
            "level_error": level_error,
            "modal_main_data": modal_main_data,
            "modal_order_data": modal_order_data,
            "modal_kind_sub_data": modal_kind_sub_data,
        }
    return dic


# other_kind_modal_update


# modal update
def nttgw_other_kind_modal_update():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    fis_cd = obj["fis_cd"]
    kind_cd_sub = obj["kind_cd_sub"]
    create_date = mod_datetime.mz_str2num_hyphen_zero_ari(obj["create_date"])

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "other_data": [],
        }
    else:
        # sql update
        sql = (
            "UPDATE sql_order_store SET"
            + " kind_cd_sub = "
            + "'"
            + kind_cd_sub
            + "'"
            + " WHERE fis_cd = "
            + "'"
            + fis_cd
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

        # sql list
        other_data = []
        other_data = mz_list_kind_null(create_date)

        dic = {
            "level_error": level_error,
            "other_data": other_data,
        }
    return dic
