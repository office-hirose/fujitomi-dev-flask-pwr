import sys
from flask import request
from _mod import mod_base, mod_datetime
from _mod_fis import (
    mod_kei_nyu_pay,
    mod_section,
    mod_staff,
    mod_cat,
    mod_coltd,
)
from fee import fee_find_sql


# start
def fee_find():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    login_level = base_data["login_level_cd"]
    user_email = base_data["google_account_email"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "login_level": login_level,
            "user_email": user_email,
            "nyu_data": [],
            "nyu_date": 0,
            "section_data": [],
            "staff_data_all": [],
            "coltd_data_all": [],
            "fee_data": [],
        }
    else:
        # nyu_date
        now_date_int = mod_datetime.mz_now_date_num()
        now_year_int = mod_datetime.mz_num2yy(now_date_int)
        now_month_int = mod_datetime.mz_num2mm(now_date_int)
        nyu_date = int(str(now_year_int) + str(now_month_int).zfill(2))

        dic = {
            "level_error": level_error,
            "login_level": login_level,
            "user_email": user_email,
            "nyu_data": mod_kei_nyu_pay.mz_common_nyu_sel(201904),
            "nyu_date": nyu_date,
            "section_data": mod_section.mz_section_data_on(),
            "staff_data_all": mod_staff.mz_staff_data_all(),
            "cat_data": mod_cat.mz_cat_data_all(),
            "coltd_data_all": mod_coltd.mz_coltd_data_all(),
            "fee_data": "",
        }
    return dic


# list
def fee_find_list():
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
            "fee_data": [],
        }
    else:
        nyu_date = int(obj["nyu_date"])
        section_cd = str(obj["section_cd"])
        staff_cd = str(obj["staff_cd"])
        coltd_cd = str(obj["coltd_cd"])

        # sql
        fee_data = fee_find_sql.list_sql(nyu_date, section_cd, staff_cd, coltd_cd)

        dic = {
            "level_error": level_error,
            "fee_data": fee_data,
        }
    return dic


# search
def fee_find_search():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    syoken_cd_main = obj["search_text"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "fee_data": [],
        }
    else:
        # sql
        if syoken_cd_main is None or syoken_cd_main == "":
            fee_data = []
        else:
            syoken_cd_main = (syoken_cd_main.replace("　", "")).replace(" ", "")
            fee_data = fee_find_sql.search_sql(syoken_cd_main)

        # dic
        dic = {
            "level_error": level_error,
            "fee_data": fee_data,
        }
    return dic
