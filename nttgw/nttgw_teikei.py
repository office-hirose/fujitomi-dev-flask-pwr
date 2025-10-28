# ------------------------------------------------------------------------
#  nttgw_teikei.py
#  |--nttgw_teikei              - 画面作成
#  |--nttgw_teikei_list         - list
#  |--nttgw_teikei_update       - list update
# ------------------------------------------------------------------------
import sys
from flask import request
from _mod import mod_base, sql_config


def nttgw_teikei():
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
        }
    else:
        dic = {
            "level_error": level_error,
            "user_email": user_email,
        }
    return dic


# list, update
def nttgw_teikei_list():
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
            "teikei_data": [],
        }
    else:
        # sql, if list_type = 'list' is pass
        if list_type == "update":
            mz_teikei_list_update()

        dic = {
            "level_error": base_data.get("level_error"),
            "teikei_data": mz_teikei_list(),
        }
    return dic


# 内部提携の提携確認
def mz_teikei_list():
    sql1 = "SELECT * FROM sql_order_store WHERE "

    sql2 = 'staff1_cd = "xxx@tokyo"'

    # 清田・嶋田
    # sql2 = 'staff1_cd = "kiyota.s@kumamoto2" AND staff2_cd != "shimada.y@kumamoto2"'

    # 嶋田・嶋田
    # sql2 = '(staff1_cd = "shimada.y@kumamoto2" AND gyotei1_cd != "9009") OR '

    # 清田・嶋田
    # sql3 = '(staff1_cd = "kiyota.s@kumamoto2" AND gyotei1_cd != "9009") OR '

    # 濱田
    # sql4 = '(staff1_cd = "hamada.t@tokyo" AND gyotei1_cd != "9024") OR '

    # 小林
    # sql5 = '(staff1_cd = "kobayashi.y@tokyo" AND gyotei1_cd != "9005") OR '

    # 野村
    # sql6 = (
    #     '(staff1_cd = "nomura.m@tokyo" AND gyotei1_cd != "9014" AND cat_cd = "2") OR '
    # )

    # 猪狩
    # sql7 = '(staff1_cd = "igari.y@tokyo" AND gyotei1_cd != "9030") OR '

    # 西山
    # sql8 = '(staff1_cd = "nishiyama.t@kumamoto1" AND gyotei1_cd != "3014") OR '

    # 前田
    # sql9 = '(staff1_cd = "maeda.s@kumamoto1" AND gyotei1_cd != "3015") OR '

    # 眞村
    # sql10 = '(staff1_cd = "mamura.s@kumamoto1" AND gyotei1_cd != "100018") OR '

    # 日野
    # sql11 = '(staff1_cd = "hino.t@kumamoto1" AND gyotei1_cd != "100019")'

    # order by
    sql12 = " ORDER BY staff1_cd, coltd_cd;"

    # sql = sql1 + sql2 + sql3 + sql5 + sql6 + sql7 + sql8 + sql9 + sql10 + sql11 + sql12
    sql = sql1 + sql2 + sql12
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 内部提携の提携・更新
def mz_teikei_list_update():
    # 清田・嶋田
    # sql_kiyota = """
    #     UPDATE sql_order_store
    #     SET
    #     staff2_cd = "shimada.y@kumamoto2",
    #     fee_staff1 = 35,
    #     fee_staff2 = 65
    #     WHERE
    #     staff1_cd = "kiyota.s@kumamoto2" AND staff2_cd != "shimada.y@kumamoto2";
    # """
    # sql_con = sql_config.mz_sql_con()
    # with sql_con:
    #     cur = sql_con.cursor()
    #     cur.execute(
    #         sql_kiyota,
    #     )
    #     sql_con.commit()

    # 嶋田・嶋田
    # sql_shimada = """
    #     UPDATE sql_order_store
    #     SET
    #     gyotei1_cd = "9009",
    #     fee_staff1 = 35,
    #     fee_gyotei1 = 65
    #     WHERE
    #     staff1_cd = "shimada.y@kumamoto2"
    #     AND gyotei1_cd != "9009";
    # """
    # sql_con = sql_config.mz_sql_con()
    # with sql_con:
    #     cur = sql_con.cursor()
    #     cur.execute(
    #         sql_shimada,
    #     )
    #     sql_con.commit()

    # 清田・嶋田
    # sql_kiyota = """
    #     UPDATE sql_order_store
    #     SET
    #     gyotei1_cd = "9009",
    #     fee_staff1 = 35,
    #     fee_gyotei1 = 65
    #     WHERE
    #     staff1_cd = "kiyota.s@kumamoto2"
    #     AND gyotei1_cd != "9009";
    # """
    # sql_con = sql_config.mz_sql_con()
    # with sql_con:
    #     cur = sql_con.cursor()
    #     cur.execute(
    #         sql_kiyota,
    #     )
    #     sql_con.commit()

    # 小林
    # sql_kobayashi = """
    #     UPDATE sql_order_store
    #     SET
    #     gyotei1_cd = "9005",
    #     fee_staff1 = 50,
    #     fee_gyotei1 = 50
    #     WHERE
    #     staff1_cd = "kobayashi.y@tokyo"
    #     AND gyotei1_cd != "9005";
    # """
    # sql_con = sql_config.mz_sql_con()
    # with sql_con:
    #     cur = sql_con.cursor()
    #     cur.execute(
    #         sql_kobayashi,
    #     )
    #     sql_con.commit()

    # 野村
    # sql_nomura = """
    #     UPDATE sql_order_store
    #     SET
    #     gyotei1_cd = "9014",
    #     fee_staff1 = 50,
    #     fee_gyotei1 = 50
    #     WHERE
    #     staff1_cd = "nomura.m@tokyo"
    #     AND gyotei1_cd != "9014"
    #     AND cat_cd = "2";
    # """
    # sql_con = sql_config.mz_sql_con()
    # with sql_con:
    #     cur = sql_con.cursor()
    #     cur.execute(
    #         sql_nomura,
    #     )
    #     sql_con.commit()

    # 猪狩
    # sql_igari = """
    #     UPDATE sql_order_store
    #     SET
    #     gyotei1_cd = "9030",
    #     fee_staff1 = 50,
    #     fee_gyotei1 = 50
    #     WHERE
    #     staff1_cd = "igari.y@tokyo"
    #     AND gyotei1_cd != "9030";
    # """
    # sql_con = sql_config.mz_sql_con()
    # with sql_con:
    #     cur = sql_con.cursor()
    #     cur.execute(
    #         sql_igari,
    #     )
    #     sql_con.commit()

    # 西山
    # sql_nishiyama = """
    #     UPDATE sql_order_store
    #     SET
    #     gyotei1_cd = "3014",
    #     fee_staff1 = 36,
    #     fee_gyotei1 = 64
    #     WHERE
    #     staff1_cd = "nishiyama.t@kumamoto1"
    #     AND gyotei1_cd != "3014";
    # """
    # sql_con = sql_config.mz_sql_con()
    # with sql_con:
    #     cur = sql_con.cursor()
    #     cur.execute(
    #         sql_nishiyama,
    #     )
    #     sql_con.commit()

    # 前田
    # sql_maeda = """
    #     UPDATE sql_order_store
    #     SET
    #     gyotei1_cd = "3015",
    #     fee_staff1 = 38,
    #     fee_gyotei1 = 62
    #     WHERE
    #     staff1_cd = "maeda.s@kumamoto1"
    #     AND gyotei1_cd != "3015";
    # """
    # sql_con = sql_config.mz_sql_con()
    # with sql_con:
    #     cur = sql_con.cursor()
    #     cur.execute(
    #         sql_maeda,
    #     )
    #     sql_con.commit()

    # 眞村
    # sql_mamura = """
    #     UPDATE sql_order_store
    #     SET
    #     gyotei1_cd = "100018",
    #     fee_staff1 = 36,
    #     fee_gyotei1 = 64
    #     WHERE
    #     staff1_cd = "mamura.s@kumamoto1"
    #     AND gyotei1_cd != "100018";
    # """
    # sql_con = sql_config.mz_sql_con()
    # with sql_con:
    #     cur = sql_con.cursor()
    #     cur.execute(
    #         sql_mamura,
    #     )
    #     sql_con.commit()

    # 日野
    # sql_hino = """
    #     UPDATE sql_order_store
    #     SET
    #     gyotei1_cd = "100019",
    #     fee_staff1 = 38,
    #     fee_gyotei1 = 62
    #     WHERE
    #     staff1_cd = "hino.t@kumamoto1"
    #     AND gyotei1_cd != "100019";
    # """
    # sql_con = sql_config.mz_sql_con()
    # with sql_con:
    #     cur = sql_con.cursor()
    #     cur.execute(
    #         sql_hino,
    #     )
    #     sql_con.commit()

    return
