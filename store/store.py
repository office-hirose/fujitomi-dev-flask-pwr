import sys
from flask import request
from _mod import mod_base, mod_datetime
from _mod_fis import (
    mod_sta,
    mod_kei_nyu_pay,
    mod_section,
    mod_staff,
    mod_keiyaku,
    mod_cat,
    mod_coltd,
    mod_pay_num,
    mod_hoken_kikan,
    mod_gyotei,
    mod_kind,
    mod_fee,
    mod_bosyu,
)
from store import store_sql


# start
def store():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    cat_cd = obj["cat_cd"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    login_level = base_data["login_level_cd"]
    user_email = base_data["google_account_email"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "user_email": "",
            "login_level": login_level,
            "sta_data_all": [],
            "keijyo_data": [],
            "keijyo_date": 0,
            "section_data": [],
            "staff_data_all": [],
            "keiyaku_data": [],
            "cat_data": [],
            "cat_cd": "",
            "coltd_data_all": [],
            "pay_num_data": [],
            "hoken_kikan_data": [],
            "gyotei_data": [],
            "aiueo_data": [],
            "kind_data_main_all": [],
            "kind_data_sub_all": [],
            "fee_data_all": [],
            "bosyu_data": [],
        }
    else:
        # keijyo
        keijyo_data = mod_kei_nyu_pay.mz_kei_nyu_pay_data()
        now_date_int = mod_datetime.mz_now_date_num()
        now_year_int = mod_datetime.mz_num2yy(now_date_int)
        now_month_int = mod_datetime.mz_num2mm(now_date_int)
        keijyo_date = int(str(now_year_int) + str(now_month_int).zfill(2))

        dic = {
            "level_error": level_error,
            "user_email": user_email,
            "login_level": login_level,
            "sta_data_all": mod_sta.mz_sta_all(),
            "keijyo_data": keijyo_data,
            "keijyo_date": keijyo_date,
            "section_data": mod_section.mz_section_data_on(),
            "staff_data_all": mod_staff.mz_staff_data_all(),
            "keiyaku_data": mod_keiyaku.mz_keiyaku_data_all(),
            "cat_data": mod_cat.mz_cat_data_all(),
            "cat_cd": cat_cd,
            "coltd_data_all": mod_coltd.mz_coltd_data_all(),
            "pay_num_data": mod_pay_num.mz_pay_num_data(),
            "hoken_kikan_data": mod_hoken_kikan.mz_hoken_kikan_data(),
            "gyotei_data": mod_gyotei.mz_gyotei_section_data_all(),
            "aiueo_data": mod_gyotei.mz_aiueo_view(),
            "kind_data_main_all": mod_kind.mz_kind_main_data_all(),
            "kind_data_sub_all": mod_kind.mz_kind_sub_data_all(),
            "fee_data_all": mod_fee.mz_fee_data_all(),
            "bosyu_data": mod_bosyu.mz_bosyu_data_all(),
        }
    return dic


# list
def store_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    cat_cd = obj["cat_cd"]
    keijyo_date = int(obj["keijyo_date"])
    section_cd = obj["section_cd"]
    staff_cd = obj["staff_cd"]
    keiyaku_cd = obj["keiyaku_cd"]
    coltd_cd = obj["coltd_cd"]

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
        store_data = store_sql.list_sql(cat_cd, keijyo_date, section_cd, staff_cd, keiyaku_cd, coltd_cd)
        dic = {
            "level_error": level_error,
            "store_data": store_data,
        }
    return dic


# search
def store_search():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    cat_cd = obj["cat_cd"]
    search_text = ((obj["search_text"]).replace("　", "")).replace(" ", "")

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
        if search_text == "":
            store_data = ""
        else:
            store_data = store_sql.search_sql(cat_cd, search_text)

        dic = {
            "level_error": level_error,
            "store_data": store_data,
        }
    return dic
