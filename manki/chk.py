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
    mod_manki,
)
from manki import chk_sql


# start
def manki():
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
            "manki_data_all": [],
            "manki_date": 0,
            "section_data": [],
            "staff_data": [],
            "keiyaku_data": [],
            "cat_data": [],
            "cat_cd": "",
            "coltd_data": [],
            "pay_num_data": [],
            "hoken_kikan_data": [],
            "gyotei_data_all": [],
            "kind_main_data": [],
            "kind_sub_data": [],
            "fee_data": [],
            "bosyu_data": [],
            "manki_chk_data_all": [],
        }
    else:
        # manki date
        now_date_int = mod_datetime.mz_now_date_num()
        now_year_int = mod_datetime.mz_num2yy(now_date_int)
        now_month_int = mod_datetime.mz_num2mm(now_date_int)
        manki_date = int(str(now_year_int) + str(now_month_int).zfill(2))

        dic = {
            "level_error": level_error,
            "user_email": user_email,
            "login_level": login_level,
            "sta_data_all": mod_sta.mz_sta_all(),
            "manki_data_all": mod_kei_nyu_pay.mz_kei_nyu_pay_data(),
            "manki_date": manki_date,
            "section_data": mod_section.mz_section_data_on(),
            "staff_data": mod_staff.mz_staff_data_all(),
            "keiyaku_data": mod_keiyaku.mz_keiyaku_data_all(),
            "cat_data": mod_cat.mz_cat_data_all(),
            "cat_cd": cat_cd,
            "coltd_data": mod_coltd.mz_coltd_data_all(),
            "pay_num_data": mod_pay_num.mz_pay_num_data(),
            "hoken_kikan_data": mod_hoken_kikan.mz_hoken_kikan_data(),
            "gyotei_data_all": mod_gyotei.mz_gyotei_section_data_all(),
            "kind_main_data": mod_kind.mz_kind_main_data_all(),
            "kind_sub_data": mod_kind.mz_kind_sub_data_all(),
            "fee_data": mod_fee.mz_fee_data_all(),
            "bosyu_data": mod_bosyu.mz_bosyu_data_all(),
            "manki_chk_data_all": mod_manki.mz_manki_chk_data_all(),
        }
    return dic


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


# モーダル用チェックコメントデータ読み込み
def load_comment():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    coltd_cd = obj["coltd_cd"]
    syoken_cd_main = obj["syoken_cd_main"]
    syoken_cd_sub = obj["syoken_cd_sub"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "comment_data": [],
        }
    else:
        # sql
        comment_data = chk_sql.load_comment_sql(coltd_cd, syoken_cd_main, syoken_cd_sub)
        dic = {
            "level_error": level_error,
            "comment_data": comment_data,
        }
    return dic
