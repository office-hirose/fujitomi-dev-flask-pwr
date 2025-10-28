import sys
from flask import request
from _mod import mod_base, sql_config


def retiree():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "retiree_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "retiree_data_all": retiree_data_sql(),
        }
    return dic


def retiree_data_sql():
    sql = """
        SELECT
        stf.*,
        os.*
        FROM
        sql_staff as stf

        LEFT JOIN
        (SELECT * FROM sql_order_store) AS os
        ON stf.staff_cd = os.staff1_cd

        WHERE
        stf.onoff_cd = 'off'
        AND
        stf.sales_cd = 'off';
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data
