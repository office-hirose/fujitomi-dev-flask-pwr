# -------------------------------------------------------------------
#  fee_hikaku.py - 画面作成
#  |--fee_hikaku_list      - リスト作成
#  |--modal_open           - 入金モーダル画面open
#  |--modal_update         - 入金モーダル変更update
#  fee_hikaku_sql_list.py  - sql list
# -------------------------------------------------------------------
import sys
from flask import request
from _mod import mod_base
from _mod_fis import mod_kei_nyu_pay, mod_coltd
from fee_import import (
    fee_hikaku_sql_list,
    fee_hikaku_sql_modal_update,
    fee_hikaku_sql_modal_nk,
    fee_hikaku_sql_modal_fk,
    fee_hikaku_sql_modal_fs,
    fee_hikaku_sql_modal_bal,
    fee_hikaku_sql_modal_sai,
    fee_hikaku_sql_ruikei,
)


def fee_hikaku():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    login_level = base_data["login_level_cd"]
    user_email = base_data["google_account_email"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "login_level": 0,
            "user_email": "",
            #
            "nyu_data": [],
            "coltd_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "login_level": login_level,
            "user_email": user_email,
            #
            "nyu_data": mod_kei_nyu_pay.mz_common_nyu_sel(201904),
            "coltd_data_all": mod_coltd.mz_coltd_data_all(),
        }
    return dic


def fee_hikaku_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    nyu_date_int = obj["nyu_date_int"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            #
            "fee_data": [],
            "fee_data_cnt": 0,
            #
            "rui_data": [],
            "rui_data_cnt": 0,
            #
            "bonus_data": [],
        }
    else:
        # 選択した年月のデータ
        fee_data = fee_hikaku_sql_list.mz_list(nyu_date_int)
        fee_data_cnt = len(fee_data)

        # 累計データ
        rui_data = fee_hikaku_sql_ruikei.mz_ruikei(nyu_date_int)
        rui_data_cnt = len(rui_data)

        # 選択した年月のボーナスデータ
        bonus_data = fee_hikaku_sql_modal_nk.mz_bonus(nyu_date_int)

        dic = {
            "level_error": level_error,
            #
            "fee_data": fee_data,
            "fee_data_cnt": fee_data_cnt,
            #
            "rui_data": rui_data,
            "rui_data_cnt": rui_data_cnt,
            #
            "bonus_data": bonus_data,
        }
    return dic


def modal_open():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    nyu_date_int = obj["nyu_date_int"]
    coltd_cd = obj["coltd_cd"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            #
            "nk_data": [],
            "nk_kind_data": [],
            "nk_section_data": [],
            #
            "fk_data": {},
            "fs_data": {},
            "bal_data": {},
            "sai_data": {},
        }
    else:
        # modal
        nk_data = fee_hikaku_sql_modal_nk.mz_nk(nyu_date_int, coltd_cd)
        nk_kind_data = fee_hikaku_sql_modal_nk.mz_nk_kind()
        nk_section_data = fee_hikaku_sql_modal_nk.mz_nk_section()

        fk_data = fee_hikaku_sql_modal_fk.mz_fk(nyu_date_int, coltd_cd)
        fs_data = fee_hikaku_sql_modal_fs.mz_fs(nyu_date_int, coltd_cd)
        bal_data = fee_hikaku_sql_modal_bal.mz_bal(nyu_date_int, coltd_cd)
        sai_data = fee_hikaku_sql_modal_sai.mz_sai(nyu_date_int, coltd_cd, fk_data, fs_data, bal_data)

        # dic
        dic = {
            "level_error": level_error,
            #
            "nk_data": nk_data,
            "nk_kind_data": nk_kind_data,
            "nk_section_data": nk_section_data,
            #
            "fk_data": fk_data,
            "fs_data": fs_data,
            "bal_data": bal_data,
            "sai_data": sai_data,
        }
    return dic


def modal_update():
    # json
    obj = request.get_json()

    jwtg = obj["jwtg"]
    nyu_date_int = obj["nyu_date_int"]
    coltd_cd = obj["coltd_cd"]

    fk_data_form = obj["fk_data"]
    bal_data_form = obj["bal_data"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            #
            "fk_data": {},
            "fs_data": {},
            "bal_data": {},
            "sai_data": {},
            #
            "fee_data": [],
            "fee_data_cnt": 0,
            #
            "rui_data": [],
            "rui_data_cnt": 0,
        }
    else:
        # update
        fee_hikaku_sql_modal_update.mz_update(nyu_date_int, coltd_cd, fk_data_form, bal_data_form)

        # modal
        fk_data = fee_hikaku_sql_modal_fk.mz_fk(nyu_date_int, coltd_cd)
        fs_data = fee_hikaku_sql_modal_fs.mz_fs(nyu_date_int, coltd_cd)
        bal_data = fee_hikaku_sql_modal_bal.mz_bal(nyu_date_int, coltd_cd)
        sai_data = fee_hikaku_sql_modal_sai.mz_sai(nyu_date_int, coltd_cd, fk_data, fs_data, bal_data)

        # 選択した年月のデータ
        fee_data = fee_hikaku_sql_list.mz_list(nyu_date_int)
        fee_data_cnt = len(fee_data)

        # 累計データ
        rui_data = fee_hikaku_sql_ruikei.mz_ruikei(nyu_date_int)
        rui_data_cnt = len(rui_data)

        # dic
        dic = {
            "level_error": level_error,
            #
            "fk_data": fk_data,
            "fs_data": fs_data,
            "bal_data": bal_data,
            "sai_data": sai_data,
            #
            "fee_data": fee_data,
            "fee_data_cnt": fee_data_cnt,
            #
            "rui_data": rui_data,
            "rui_data_cnt": rui_data_cnt,
        }
    return dic
