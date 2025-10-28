from _mod import sql_config


def mz_nayose_knid_list(knid_find):
    cnt = 0
    kei_name_nospace = ""
    sql1 = """
        SELECT
        COUNT(*) AS cnt,
        MIN(dmy.kei_name_nospace) AS kei_name_nospace
        FROM
        (
        SELECT
        kei_name_nospace
        FROM
        sql_order_store
        """
    sql2 = "" + " WHERE" + " kei_name_nospace like " + '"' + "%" + knid_find + "%" + '"' + " ) AS dmy"
    sql3 = " GROUP BY dmy.kei_name_nospace"
    sql4 = " ORDER BY cnt DESC"
    sql5 = " LIMIT 0, 1;"
    sql = sql1 + sql2 + sql3 + sql4 + sql5
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        cnt = dt["cnt"]
        kei_name_nospace = dt["kei_name_nospace"]
    return cnt, kei_name_nospace


def mz_nayose_knid_update(knid_moto, knid_update):
    sql = (
        "UPDATE sql_order_store"
        + " SET"
        + " kei_name_nospace = "
        + "'"
        + knid_update
        + "'"
        + " WHERE"
        + " kei_name_nospace = "
        + "'"
        + knid_moto
        + "'"
        + ";"
    )
    con = sql_config.mz_sql_con()
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    return
