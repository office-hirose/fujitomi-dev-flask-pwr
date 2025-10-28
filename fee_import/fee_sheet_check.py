# -------------------------------------------------------------------
#  fee_sheet_check.py - Spread Sheet チェックする
# -------------------------------------------------------------------
# import io
import sys
from flask import request
from _mod import mod_base
from fee_import import fee_mod


def fee_sheet_check():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    sheet_url = obj["sheet_url"]

    # base - level 2
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            # error check
            "error_list": [],
            "success_cnt": 0,
            "fee_notax_total": 0,
        }
    else:
        # get sheet data
        sheet_data = fee_mod.get_sheet_data(sheet_url)

        # insert sheet data check
        error_list, success_cnt, fee_notax_total = check_sheet_data(sheet_data)

        dic = {
            "level_error": level_error,
            # error check
            "error_list": error_list,
            "success_cnt": success_cnt,
            "fee_notax_total": fee_notax_total,
        }
    return dic


# インサート実行前にチェックする
def check_sheet_data(sheet_data):
    # init
    error_list = []
    error_row = 0
    success_cnt = 0
    fee_notax_total = 0

    nyu_nendo = 0
    nyu_date = 0
    cat_cd = ""
    coltd_cd = ""
    kind_cd = 0
    syoken_cd_main = ""
    syoken_cd_sub = ""
    fee_withtax = 0
    fee_notax = 0
    fee_tax_per = 0
    fee_tax_num = 0
    kaime = ""
    first_next_year = 0

    # check
    # noqa: F841 コメントは、その行に対する Flake8 の特定のエラーチェック（この場合は F841）を無効にします。
    for dt in sheet_data:
        try:
            error_row += 1

            nyu_nendo = int(dt[0])  # noqa: F841
            nyu_date = int(dt[1])  # noqa: F841
            cat_cd = dt[2]  # noqa: F841
            coltd_cd = dt[3]  # noqa: F841
            kind_cd = int(dt[4])  # noqa: F841
            syoken_cd_main = dt[5]  # noqa: F841
            syoken_cd_sub = dt[6]  # noqa: F841
            fee_withtax = int(dt[7])  # noqa: F841
            fee_notax = int(dt[8])  # noqa: F841
            fee_tax_num = int(dt[10])  # noqa: F841
            fee_tax_per = int(dt[9])  # noqa: F841
            kaime = dt[11]  # noqa: F841
            first_next_year = int(dt[12])  # noqa: F841

            success_cnt += 1
            fee_notax_total += fee_notax
        except:  # noqa: E722
            error_list.append(str(error_row) + "行目エラー")

    return error_list, success_cnt, fee_notax_total
