# -------------------------------------------------------------------
#  fee_nyu_hikaku.py - 画面作成
#  |--fee_nyu_hikaku_list - 比較リスト作成
#  fee_nyu_hikaku_sql.py  - sql
# -------------------------------------------------------------------
import sys
from flask import request

from _mod import mod_base
from _mod_fis import mod_kei_nyu_pay
from fee import fee_nyu_hikaku_sql


def fee_nyu_hikaku():
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
            "login_level": 0,
            "user_email": "",
            "nyu_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "login_level": login_level,
            "user_email": user_email,
            "nyu_data": mod_kei_nyu_pay.mz_common_nyu_sel(201904),
        }
    return dic


def fee_nyu_hikaku_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    nyu_date_int = obj["nyu_date_int"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "fee_data": [],
            "fee_data_cnt": 0,
            "kakutei_total": 0,
            "store_total": 0,
            "sai_total": 0,
        }
    else:
        # sql data
        fee_data = fee_nyu_hikaku_sql.mz_sql_fee_nyu_hikaku(nyu_date_int)
        fee_data_cnt = len(fee_data)

        # fee_kakutei total
        kakutei_total = fee_nyu_hikaku_sql.mz_sql_fee_kakutei_total(nyu_date_int)

        # fee_order_store total
        store_total = fee_nyu_hikaku_sql.mz_sql_fee_order_store_total(nyu_date_int)

        # sai total
        sai_total = kakutei_total - store_total

        dic = {
            "level_error": level_error,
            "fee_data": fee_data,
            "fee_data_cnt": fee_data_cnt,
            "kakutei_total": kakutei_total,
            "store_total": store_total,
            "sai_total": sai_total,
        }
    return dic


def fee_nyu_hikaku_sai():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    nyu_date_int = obj["nyu_date_int"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "sai_data": [],
            "sai_data_cnt": 0,
        }
    else:
        # sql data
        sai_data = fee_nyu_hikaku_sql.mz_sql_sai(nyu_date_int)
        sai_data_cnt = len(sai_data)

        dic = {
            "level_error": level_error,
            "sai_data": sai_data,
            "sai_data_cnt": sai_data_cnt,
        }
    return dic
