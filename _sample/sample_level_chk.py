import sys
from flask import request
from _mod import mod_base


def sample_level_chk():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # dic
    dic = {
        "level_error": level_error,
    }
    return dic
