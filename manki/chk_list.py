import sys
from flask import request
from _mod import mod_base
from manki import chk_sql


# list
def manki_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    cat_cd = obj["cat_cd"]
    manki_date = int(obj["manki_date"])
    section_cd = obj["section_cd"]
    staff_cd = obj["staff_cd"]
    manki_chk_cd = obj["manki_chk_cd"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "store_data": [],
        }
    else:
        # sql
        store_data = chk_sql.manki_list_sql(cat_cd, manki_date, section_cd, staff_cd, manki_chk_cd)
        dic = {
            "level_error": level_error,
            "store_data": store_data,
        }
    return dic
