# -------------------------------------------------------------------
#  fee_sheet_import.py - Spread Sheetからインポート実行する
# -------------------------------------------------------------------
import sys
from flask import request
from _mod import mod_base, sql_config
from fee_import import (
    fee_hikaku_sql_list,
    fee_mod,
    fee_hikaku_sql_modal_fk,
    fee_hikaku_sql_modal_fs,
    fee_hikaku_sql_modal_bal,
    fee_hikaku_sql_modal_sai,
)


def fee_sheet_import():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    sheet_url = obj["sheet_url"]
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
        # get sheet data
        sheet_data = fee_mod.get_sheet_data(sheet_url)

        # insert sheet data to [sql_fee_temp]
        success_cnt, fee_notax_total = insert_sheet_data(sheet_data)

        # grouping, export, truncate
        grouping_export_truncate()

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
            # result
            "success_cnt": success_cnt,
            "fee_notax_total": fee_notax_total,
            # list
            "fee_data": fee_data,
            "fee_data_cnt": fee_data_cnt,
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


# インサート実行 sql_fee_temp
def insert_sheet_data(sheet_data):
    # init
    success_cnt = 0
    fee_notax_total = 0

    # SQL接続
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = """
        INSERT INTO sql_fee_temp (
            nyu_nendo,
            nyu_date,
            cat_cd,
            coltd_cd,
            kind_cd,
            syoken_cd_main,
            syoken_cd_sub,
            fee_withtax,
            fee_notax,
            fee_tax_num,
            fee_tax_per,
            kaime,
            first_next_year
        ) VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        );
        """
        cur = sql_con.cursor()

        # SpreadSheetから取得したデータを使ってSQLインサートを行う
        for dt in sheet_data:
            cur.execute(sql, tuple(dt))  # 行データをそのままタプルに変換して渡す

            # result
            success_cnt += 1
            fee_notax = int(dt[8])
            fee_notax_total += fee_notax

        sql_con.commit()

    return success_cnt, fee_notax_total


# grouping, export, truncate
def grouping_export_truncate():
    sql = """
    INSERT INTO
        sql_fee_store
        (
            nyu_nendo,
            nyu_date,
            cat_cd,
            coltd_cd,
            kind_cd,
            syoken_cd_main,
            syoken_cd_sub,
            fee_withtax,
            fee_notax,
            fee_tax_num,
            fee_tax_per,
            kaime,
            first_next_year
        )

        SELECT
            min(nyu_nendo) AS nyu_nendo,
            min(nyu_date) AS nyu_date,
            min(cat_cd) AS cat_cd,
            min(coltd_cd) AS coltd_cd,
            min(kind_cd) AS kind_cd,
            min(syoken_cd_main) AS syoken_cd_main,
            min(syoken_cd_sub) AS syoken_cd_sub,
            sum(fee_withtax) AS fee_withtax,
            sum(fee_notax) AS fee_notax,
            sum(fee_tax_num) AS fee_tax_num,
            min(fee_tax_per) AS fee_tax_per,
            min(kaime) AS kaime,
            min(first_next_year) AS first_next_year

        FROM
            sql_fee_temp

        GROUP BY
            nyu_date,
            coltd_cd,
            kind_cd,
            syoken_cd_main,
            syoken_cd_sub,
            fee_tax_per,
            kaime,
            first_next_year;
    """
    sql_con = sql_config.mz_sql_con()
    cur = sql_con.cursor()
    cur.execute(sql)
    sql_con.commit()
    # cur.close()

    sql = "TRUNCATE sql_fee_temp;"
    sql_con = sql_config.mz_sql_con()
    cur = sql_con.cursor()
    cur.execute(sql)
    sql_con.commit()
    # cur.close()

    return
