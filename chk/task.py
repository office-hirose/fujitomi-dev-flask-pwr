import sys
from flask import request
from _mod import mod_base, sql_config


def task():
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
            "task_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "task_data": mz_task_data(),
        }
    return dic


def task_del():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    key_dict = obj["key_array"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "task_data": [],
        }
    else:
        # delete
        mz_task_del(key_dict)

        dic = {
            "level_error": level_error,
            "task_data": mz_task_data(),
        }
    return dic


def mz_task_data():
    sql = "SELECT * FROM sql_task_sta ORDER BY id DESC;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_task_del(key_dict):
    sql = "DELETE FROM sql_task_sta WHERE id = %s"
    con = sql_config.mz_sql_con()
    cur = con.cursor()
    for id in key_dict:
        cur.execute(sql, (id,))
        con.commit()
    return
