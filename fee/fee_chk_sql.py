from _mod import sql_config


def mz_fee_chk(nyu_date_int):
    sql1 = """
    SELECT
    min( cat_cd ) AS cat_cd,
    min( coltd_cd ) AS coltd_cd,
    min( syoken_cd_main ) AS syoken_cd_main,
    min( syoken_cd_sub ) AS syoken_cd_sub
    FROM
    (
    SELECT
    fee.cat_cd AS cat_cd,
    fee.coltd_cd AS coltd_cd,
    fee.syoken_cd_main AS syoken_cd_main,
    fee.syoken_cd_sub AS syoken_cd_sub
    FROM
    """

    sql2 = " ( SELECT * FROM sql_fee_store WHERE nyu_date = " + str(nyu_date_int) + ") AS fee "

    sql3 = """
    LEFT JOIN (
    SELECT
    min( cat_cd ) AS cat_cd,
    min( coltd_cd ) AS coltd_cd,
    min( syoken_cd_main ) AS syoken_cd_main,
    min( syoken_cd_sub ) AS syoken_cd_sub
    FROM
    sql_order_store
    GROUP BY
    sql_order_store.cat_cd,
    sql_order_store.coltd_cd,
    sql_order_store.syoken_cd_main,
    sql_order_store.syoken_cd_sub
    ) AS os ON
    fee.cat_cd = os.cat_cd
    AND fee.coltd_cd = os.coltd_cd
    AND fee.syoken_cd_main = os.syoken_cd_main
    AND fee.syoken_cd_sub = os.syoken_cd_sub
    WHERE
    os.cat_cd IS NULL
    ) AS res
    GROUP BY
    res.cat_cd,
    res.coltd_cd,
    res.syoken_cd_main,
    res.syoken_cd_sub
    ORDER BY
    cat_cd,
    coltd_cd,
    syoken_cd_main,
    syoken_cd_sub
    ;
    """
    sql = sql1 + sql2 + sql3
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_fee_chk_nttgw_dat(coltd_cd, syoken_cd_main, syoken_cd_sub):
    sql = (
        "SELECT * FROM sql_nttgw_dat"
        + " WHERE coltd_cd = "
        + "'"
        + coltd_cd
        + "'"
        + " AND syoken_cd_main = "
        + "'"
        + syoken_cd_main
        + "'"
        + " AND syoken_cd_sub = "
        + "'"
        + syoken_cd_sub
        + "'"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    nttgw_dat_cnt = len(sql_data)
    return nttgw_dat_cnt
