# ------------------------------------------------------------------------
#  nttgw_not_store.py
#  |--nttgw_not_store      - 画面作成
#  |--nttgw_not_store_cnt  - カウント表示
#  |--nttgw_not_store_exe  - 実行する
# ------------------------------------------------------------------------
import sys
from flask import request
from _mod import mod_base, sql_config


def nttgw_not_store():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    dic = {
        "level_error": level_error,
    }
    return dic


def nttgw_not_store_cnt():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "import_cnt": 0,
            "update_cnt": 0,
            "store_cnt": 0,
            "not_store_cnt": 0,
            "all_cnt": 0,
        }
    else:
        # init
        sql_data = []
        import_cnt = 0
        update_cnt = 0
        store_cnt = 0
        not_store_cnt = 0
        all_cnt = 0

        # sql
        sql = "SELECT min(exe_sta) AS exe_sta, count(*) AS count FROM sql_nttgw_dat GROUP BY exe_sta;"
        sql_data = sql_config.mz_sql(sql)

        for dt in sql_data:
            if dt["exe_sta"] == "import":
                import_cnt = dt["count"]

            if dt["exe_sta"] == "update":
                update_cnt = dt["count"]

            if dt["exe_sta"] == "store":
                store_cnt = dt["count"]

            if dt["exe_sta"] == "not_store":
                not_store_cnt = dt["count"]

        # all cnt
        all_cnt = import_cnt + update_cnt + store_cnt + not_store_cnt

        # dic
        dic = {
            "level_error": level_error,
            "import_cnt": import_cnt,
            "update_cnt": update_cnt,
            "store_cnt": store_cnt,
            "not_store_cnt": not_store_cnt,
            "all_cnt": all_cnt,
        }
    return dic


def nttgw_not_store_exe():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "import_cnt": 0,
            "update_cnt": 0,
            "store_cnt": 0,
            "not_store_cnt": 0,
            "all_cnt": 0,
        }
    else:
        # update exe_sta
        sql = (
            "UPDATE sql_nttgw_dat SET"
            + " exe_sta = "
            + '"'
            + "not_store"
            + '"'
            + " WHERE"
            + " exe_sta = "
            + '"'
            + "update"
            + '"'
            + ";"
        )
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            cur = sql_con.cursor()
            cur.execute(
                sql,
            )
            sql_con.commit()

    # count再計算

    # init
    sql_data = []
    import_cnt = 0
    update_cnt = 0
    store_cnt = 0
    not_store_cnt = 0
    all_cnt = 0

    # sql
    sql = "SELECT min(exe_sta) AS exe_sta, count(*) AS count FROM sql_nttgw_dat GROUP BY exe_sta;"
    sql_data = sql_config.mz_sql(sql)

    for dt in sql_data:
        if dt["exe_sta"] == "import":
            import_cnt = dt["count"]

        if dt["exe_sta"] == "update":
            update_cnt = dt["count"]

        if dt["exe_sta"] == "store":
            store_cnt = dt["count"]

        if dt["exe_sta"] == "not_store":
            not_store_cnt = dt["count"]

    # all cnt
    all_cnt = import_cnt + update_cnt + store_cnt + not_store_cnt

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(9, jwtg, acc_page_name)

    dic = {
        "level_error": level_error,
        "import_cnt": import_cnt,
        "update_cnt": update_cnt,
        "store_cnt": store_cnt,
        "not_store_cnt": not_store_cnt,
        "all_cnt": all_cnt,
    }
    return dic
