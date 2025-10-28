# -------------------------------------------------------------------
#  modal_nyukin, update, calc, create
# -------------------------------------------------------------------
import sys
from flask import request

from _mod import mod_base
from fee_import import (
    fee_nyukin_sql_modal_update,
    fee_nyukin_sql_modal_create,
    fee_hikaku_sql_modal_nk,
)


# 入金金額を更新
def modal_nyukin_update():
    # json
    obj = request.get_json()

    jwtg = obj["jwtg"]
    modal_nk_data = obj["modal_nk_data"]

    # base - level 2
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "nk_data": [],
            "bonus_data": [],
        }
    else:
        # update
        fee_nyukin_sql_modal_update.mz_update(modal_nk_data)

        # calc
        fee_nyukin_sql_modal_update.mz_calc(modal_nk_data)

        # 結果
        for dt in modal_nk_data:
            nyu_date = dt["nyu_date"]
            coltd_cd = dt["coltd_cd"]
            break

        # 入金データ
        nk_data = fee_hikaku_sql_modal_nk.mz_nk(nyu_date, coltd_cd)

        # 選択した年月のボーナスデータ
        bonus_data = fee_hikaku_sql_modal_nk.mz_bonus(nyu_date)

        # dic
        dic = {
            "level_error": level_error,
            "nk_data": nk_data,
            "bonus_data": bonus_data,
        }
    return dic


# 入金金額用のフィールドを作成
def modal_nyukin_create():
    # json
    obj = request.get_json()

    jwtg = obj["jwtg"]
    nyu_date = obj["modal_nyu_date_int"]
    coltd_cd = obj["modal_coltd_cd"]

    # base - level 2
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "nk_data": [],
            "bonus_data": [],
        }
    else:
        # create
        fee_nyukin_sql_modal_create.mz_create(nyu_date, coltd_cd)
        nk_data = fee_hikaku_sql_modal_nk.mz_nk(nyu_date, coltd_cd)

        # 選択した年月のボーナスデータ
        bonus_data = fee_hikaku_sql_modal_nk.mz_bonus(nyu_date)

        # dic
        dic = {
            "level_error": level_error,
            "nk_data": nk_data,
            "bonus_data": bonus_data,
        }
    return dic
