# -------------------------------------------------------------------
#  fee_delete_sql.py - sql delete実行する
# -------------------------------------------------------------------
import sys
from flask import request
import pymysql.cursors
from _mod import mod_base, sql_config
from fee_import import (
    fee_hikaku_sql_list,
    fee_hikaku_sql_modal_fk,
    fee_hikaku_sql_modal_fs,
    fee_hikaku_sql_modal_bal,
    fee_hikaku_sql_modal_sai,
)


def fee_delete_sql_exe():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    nyu_date_int = obj["nyu_date_int"]
    coltd_cd = obj["coltd_cd"]

    # base - level 2
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "new_sheet_url": "",
            "new_sheet_fee_total": 0,
        }
    else:
        # delete
        delete_sql(nyu_date_int, coltd_cd)

        # list
        fee_data = fee_hikaku_sql_list.mz_list(nyu_date_int)
        fee_data_cnt = len(fee_data)

        # list total
        # (
        #     fk_total,
        #     fs_total,
        #     bal_total,
        #     sai_total,
        #     fk_total_keiri_notax,
        #     fk_total_keiri_withtax,
        # ) = fee_hikaku_sql_list.mz_total(nyu_date_int)

        # modal
        fk_data = fee_hikaku_sql_modal_fk.mz_fk(nyu_date_int, coltd_cd)
        fs_data = fee_hikaku_sql_modal_fs.mz_fs(nyu_date_int, coltd_cd)
        bal_data = fee_hikaku_sql_modal_bal.mz_bal(nyu_date_int, coltd_cd)
        sai_data = fee_hikaku_sql_modal_sai.mz_sai(nyu_date_int, coltd_cd, fk_data, fs_data, bal_data)

        dic = {
            "level_error": level_error,
            # list
            "fee_data": fee_data,
            "fee_data_cnt": fee_data_cnt,
            # list total
            # "fk_total": fk_total,
            # "fs_total": fs_total,
            # "bal_total": bal_total,
            # "sai_total": sai_total,
            # "fk_total_keiri_notax": fk_total_keiri_notax,
            # "fk_total_keiri_withtax": fk_total_keiri_withtax,
            # modal
            "fk_data": fk_data,
            "fs_data": fs_data,
            "bal_data": bal_data,
            "sai_data": sai_data,
        }
    return dic


def delete_sql(nyu_date_int, coltd_cd):
    con = sql_config.mz_sql_con()
    try:
        with con.cursor() as cur:
            sql = "DELETE FROM sql_fee_store WHERE nyu_date = %s AND coltd_cd = %s AND syoken_cd_main != 'balance';"
            cur.execute(sql, (nyu_date_int, coltd_cd))
        con.commit()
    except pymysql.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()
    return
