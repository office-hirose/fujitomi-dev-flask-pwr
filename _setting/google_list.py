import sys
from flask import request
from _mod import mod_base, mod_lm, sql_config


def google_list():
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
            "google_list_data": [],
            "lm_data": [],
        }
    else:
        sql_data = sql_config.mz_sql("SELECT * FROM com_google_account ORDER BY id;")
        dic = {
            "level_error": level_error,
            "google_list_data": sql_data,
            "lm_data": mod_lm.lm_data(),
        }
    return dic
