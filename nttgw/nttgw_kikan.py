# ------------------------------------------------------------------------
#  nttgw_kikan.py
#  |--nttgw_kikan              - 画面作成
#  |--nttgw_kikan_list         - list
#  |--nttgw_kikan_update       - list update
#  |--nttgw_kikan_modal        - modal
#  |--nttgw_kikan_modal_update - modal update
# ------------------------------------------------------------------------
import sys
from flask import request
from _mod import mod_base, sql_config
from _mod_fis import mod_hoken_kikan

# from decimal import Decimal


def nttgw_kikan():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    user_email = base_data["google_account_email"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "user_email": "",
            "modal_hoken_kikan_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "user_email": user_email,
            "modal_hoken_kikan_data": mod_hoken_kikan.mz_hoken_kikan_data(),
        }
    return dic


# list, update
def nttgw_kikan_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    list_type = obj["list_type"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "kikan_data": [],
        }
    else:
        # sql, if list_type = 'list' is pass
        if list_type == "update":
            mz_kikan_data_update()

        dic = {
            "level_error": level_error,
            "kikan_data": mz_kikan_data_list(),
        }
    return dic


# modal hoken kikan keiyaku list
def nttgw_modal_hoken_kikan_keiyaku_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    syoken_cd_main = obj["syoken_cd_main"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "modal_hoken_kikan_keiyaku_list": [],
        }
    else:
        # sql
        sql1 = """
            SELECT
            os.syoken_cd_main,
            os.syoken_cd_sub,
            os.hoken_kikan_year,
            hk.hoken_kikan_cd,
            hk.hoken_kikan_name
            FROM
            sql_order_store AS os
            LEFT JOIN sql_hoken_kikan AS hk ON hk.hoken_kikan_cd = os.hoken_kikan_cd
        """
        sql2 = " WHERE os.syoken_cd_main = " + "'" + syoken_cd_main + "'" + ";"
        sql = sql1 + sql2
        sql_data = sql_config.mz_sql(sql)

        dic = {
            "level_error": level_error,
            "modal_hoken_kikan_keiyaku_list": sql_data,
        }

    return dic


# modal hoken kikan update
def nttgw_modal_kikan_update():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    fis_cd = obj["fis_cd"]
    hoken_kikan_cd = obj["hoken_kikan_cd"]
    hoken_kikan_year = int(obj["hoken_kikan_year"])

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "kikan_data": [],
        }
    else:
        # sql
        sql = (
            "UPDATE sql_order_store SET"
            + " hoken_kikan_cd = "
            + str(hoken_kikan_cd)
            + ","
            + " hoken_kikan_year = "
            + str(hoken_kikan_year)
            + " WHERE fis_cd = "
            + str(fis_cd)
            + ";"
        )
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            cur = sql_con.cursor()
            cur.execute(
                sql,
            )
            sql_con.commit()

        # dic
        dic = {
            "level_error": level_error,
            "kikan_data": mz_kikan_data_list(),
        }
    return dic


# 保険期間＝0(未設定)
def mz_kikan_data_list():
    # -- 保険期間[未設定]を確認[1年など]
    # -- 0=未設定
    # -- 1=1年
    # -- 10=10年
    # -- 2=2年
    # -- 3=3年
    # -- 5=5年
    # -- 99=終身
    # -- 999=短期(旅行保険等)
    # -- 9999=その他/年入力

    sql = """
        SELECT
            fis_cd,
            cat_cd,
            coltd_cd,
            syoken_cd_main,
            syoken_cd_sub,
            siki_date,
            manki_date,
            kei_name,
            hoken_kikan_cd,
            hoken_kikan_year,
            (manki_date - siki_date) / 10000 AS kikan
        FROM
            sql_order_store
        WHERE
            hoken_kikan_cd = '0'
            AND siki_date != 0
            AND manki_date != 0
        ORDER BY
            kikan,
            cat_cd,
            coltd_cd,
            siki_date,
            manki_date
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 保険期間 一括更新
def mz_kikan_data_update():
    # -- 保険期間[未設定]を全て更新
    # -- 0=未設定
    # -- 1=1年
    # -- 2=2年
    # -- 3=3年
    # -- 5=5年
    # -- 10=10年
    # -- 99=終身
    # -- 999=短期(旅行保険等)
    # -- 9999=その他/年入力

    # -- 1年
    sql1 = """
        UPDATE sql_order_store SET hoken_kikan_cd = "1"
        WHERE hoken_kikan_cd = "0" AND siki_date != 0 AND manki_date != 0 AND (manki_date - siki_date) = 10000;
    """
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        cur.execute(
            sql1,
        )
        sql_con.commit()

    # -- 2年
    sql2 = """
        UPDATE sql_order_store SET hoken_kikan_cd = "2"
        WHERE hoken_kikan_cd = "0" AND siki_date != 0 AND manki_date != 0 AND (manki_date - siki_date) = 20000;
    """
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        cur.execute(
            sql2,
        )
        sql_con.commit()

    # -- 3年
    sql3 = """
        UPDATE sql_order_store SET hoken_kikan_cd = "3"
        WHERE hoken_kikan_cd = "0" AND siki_date != 0 AND manki_date != 0 AND (manki_date - siki_date) = 30000;
    """
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        cur.execute(
            sql3,
        )
        sql_con.commit()

    # -- 5年
    sql5 = """
        UPDATE sql_order_store SET hoken_kikan_cd = "5"
        WHERE hoken_kikan_cd = "0" AND siki_date != 0 AND manki_date != 0 AND (manki_date - siki_date) = 50000;
    """
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        cur.execute(
            sql5,
        )
        sql_con.commit()

    # -- 10年
    sql10 = """
        UPDATE sql_order_store SET hoken_kikan_cd = "10"
        WHERE hoken_kikan_cd = "0" AND siki_date != 0 AND manki_date != 0 AND (manki_date - siki_date) = 100000;
    """
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        cur.execute(
            sql10,
        )
        sql_con.commit()

    # -- 終身
    sql99 = """
        UPDATE sql_order_store SET hoken_kikan_cd = "99"
        WHERE hoken_kikan_cd = "0" AND siki_date != 0 AND manki_date = 0;
    """
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        cur.execute(
            sql99,
        )
        sql_con.commit()

    return


# hoken kikan modal
# def mz_kikan_modal(fis_cd):
#     temp = 0
#     kikan = 0
#     sql = 'SELECT * FROM sql_order_store WHERE fis_cd = ' + '\"' + str(fis_cd) + '\"' + ';'
#     sql_data = sql_config.mz_sql(sql)
#     for dt in sql_data:
#         temp = Decimal(str(dt['manki_date'] - dt['siki_date']))
#     kikan = Decimal(str(temp / 10000))
#     return sql_data, kikan
