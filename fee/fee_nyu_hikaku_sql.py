from _mod import sql_config


# sql_fee_kakutei, sql_fee_order_store
def mz_sql_fee_nyu_hikaku(nyu_date_int):
    sql1 = """
        SELECT
            fk.id,
            fk.nyu_date,
            fk.cat_cd,
            fk.coltd_cd,
            coltd.name_simple AS coltd_name,
            fk.fee_notax AS fk_fee_num,

            CASE
                WHEN fs.fee_num IS NULL THEN 0
                ELSE CAST(fs.fee_num AS DECIMAL)
            END AS fs_fee_num,

            fk.fee_notax - fs.fee_num AS sai

        FROM sql_fee_kakutei AS fk
        LEFT JOIN sql_coltd AS coltd ON fk.coltd_cd = coltd.coltd_cd
        """
    sql2 = (
        " LEFT JOIN"
        + " ("
        + " SELECT"
        + " min(coltd_cd) AS coltd_cd,"
        + " SUM(pay_fee_yen) AS fee_num"
        + " FROM sql_fee_order_store"
        + " WHERE nyu_date = "
        + str(nyu_date_int)
        + " GROUP BY sql_fee_order_store.coltd_cd"
        + " ) AS fs"
        + " ON fk.coltd_cd = fs.coltd_cd"
    )
    sql3 = " WHERE fk.nyu_date = " + str(nyu_date_int)
    sql4 = " ORDER BY fk.cat_cd, fk.coltd_cd;"
    sql = sql1 + sql2 + sql3 + sql4
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# sql_fee_kakutei 確定金額合計
def mz_sql_fee_kakutei_total(nyu_date_int):
    kakutei_total = 0
    sql1 = """
        SELECT
            CASE
                WHEN sum(fee_notax) IS NULL THEN 0
                ELSE sum(fee_notax)
            END AS total_fee_num
        FROM
            sql_fee_kakutei
        """
    sql2 = "WHERE nyu_date = " + str(nyu_date_int) + ";"
    sql = sql1 + sql2
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        kakutei_total = dt["total_fee_num"]
    return int(kakutei_total)


# sql_fee_order_store 実収金額合計
def mz_sql_fee_order_store_total(nyu_date_int):
    store_total = 0
    sql1 = """
        SELECT
            CASE
                WHEN sum(pay_fee_yen) IS NULL THEN 0
                ELSE sum(pay_fee_yen)
            END AS total_fee_num
        FROM
            sql_fee_order_store
        """
    sql2 = "WHERE nyu_date = " + str(nyu_date_int) + ";"
    sql = sql1 + sql2
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        store_total = dt["total_fee_num"]
    return int(store_total)


# 入金金額と実収手数料エクセルの合計が不一致の場合の検証用2
def mz_sql_sai(nyu_date_int):
    sql = (
        "SELECT * FROM"
        + " ("
        + "SELECT"
        + "	min( coltd_cd ) AS coltd_cd,"
        + " min( syoken_cd_main ) AS syoken_cd_main,"
        + " sum( fee_num ) AS fee_num"
        + " FROM"
        + " ("
        + "SELECT"
        + " min( coltd_cd ) AS coltd_cd,"
        + " min( syoken_cd_main ) AS syoken_cd_main,"
        + " sum( fee_notax ) AS fee_num"
        + " FROM sql_fee_store"
        + " WHERE"
        + " nyu_date = "
        + str(nyu_date_int)
        + " GROUP BY coltd_cd, syoken_cd_main"
        + " UNION ALL"
        + " SELECT"
        + " min( coltd_cd ) AS coltd_cd,"
        + " min( syoken_cd_main ) AS syoken_cd_main,"
        + " sum( pay_fee_yen ) * (- 1) AS fee_num"
        + " FROM sql_fee_order_store"
        + " WHERE"
        + " nyu_date = "
        + str(nyu_date_int)
        + " GROUP BY coltd_cd, syoken_cd_main"
        + ") AS tmp1"
        + " GROUP BY coltd_cd, syoken_cd_main"
        + ") AS tmp2"
        + " WHERE fee_num > 2 OR fee_num < - 2;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data
