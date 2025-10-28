import sys
from flask import request
from _mod import mod_base
from _mod_fis import mod_kei_name_sch


def kei_name_sch():
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
            "kei_name_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "kei_name_data": mod_kei_name_sch.mz_kei_name_sch(),
        }
    return dic


def kei_name_sch_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    kei_name_nospace = obj["kei_name_nospace"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "list_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "list_data_all": mod_kei_name_sch.mz_kei_name_sch_list(kei_name_nospace),
        }
    return dic
