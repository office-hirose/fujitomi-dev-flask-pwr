from _mod import sql_config
from sum import sum_common_sql


# data 当月
def mz_data_tou(keijyo_date_int, keiyaku_grp_cd, cat_cd, section_cd):
    sql1 = """
        SELECT
        ss.cnt AS cnt,
        coltd.cat_cd AS cat_cd,
        coltd.coltd_cd AS coltd_cd,
        coltd.name_simple AS coltd_name,

        ss.res_hoken_ryo,
        ss.res_hoken_ryo_year,
        ss.res_fee_money,
        ss.res_fee_money_year,
        ss.res_fee_money_total

        FROM sql_coltd AS coltd

        LEFT JOIN
        (
        SELECT
        count(*) AS cnt,
        max(sss.cat_cd) AS cat_cd,
        max(sss.coltd_cd) AS coltd_cd,
        sum(sss.res_hoken_ryo) AS res_hoken_ryo,
        sum(sss.res_hoken_ryo_year) AS res_hoken_ryo_year,
        sum(sss.res_fee_money) AS res_fee_money,
        sum(sss.res_fee_money_year) AS res_fee_money_year,
        sum(sss.res_fee_money_total) AS res_fee_money_total

        FROM sql_sum_store AS sss
    """

    if section_cd == "0":
        sql2 = " WHERE sss.keijyo_date = " + str(keijyo_date_int) + " AND sss.cat_cd = " + '"' + str(cat_cd) + '"'
    else:
        sql2 = (
            " WHERE sss.keijyo_date = "
            + str(keijyo_date_int)
            + " AND sss.cat_cd = "
            + '"'
            + str(cat_cd)
            + '"'
            + " AND sss.section_cd = "
            + '"'
            + str(section_cd)
            + '"'
        )

    sql3 = sum_common_sql.mz_keiyaku_grp(keiyaku_grp_cd)
    sql4 = " GROUP BY sss.coltd_cd) AS ss ON ss.coltd_cd = coltd.coltd_cd"
    sql5 = " WHERE coltd.onoff_cd = 'on' AND coltd.cat_cd = " + '"' + str(cat_cd) + '"'
    sql6 = " ORDER BY coltd.cat_cd, coltd.coltd_cd;"
    sql = sql1 + sql2 + sql3 + sql4 + sql5 + sql6
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# data 累計
def mz_data_rui(keijyo_nendo, keiyaku_grp_cd, cat_cd, section_cd):
    sql1 = """
        SELECT
        ss.cnt AS cnt,
        coltd.cat_cd AS cat_cd,
        coltd.coltd_cd AS coltd_cd,
        coltd.name_simple AS coltd_name,

        ss.res_hoken_ryo,
        ss.res_hoken_ryo_year,
        ss.res_fee_money,
        ss.res_fee_money_year,
        ss.res_fee_money_total

        FROM sql_coltd AS coltd

        LEFT JOIN
        (
        SELECT
        count(*) AS cnt,
        max(sss.cat_cd) AS cat_cd,
        max(sss.coltd_cd) AS coltd_cd,
        sum(sss.res_hoken_ryo) AS res_hoken_ryo,
        sum(sss.res_hoken_ryo_year) AS res_hoken_ryo_year,
        sum(sss.res_fee_money) AS res_fee_money,
        sum(sss.res_fee_money_year) AS res_fee_money_year,
        sum(sss.res_fee_money_total) AS res_fee_money_total

        FROM sql_sum_store AS sss
    """
    if section_cd == "0":
        sql2 = " WHERE sss.keijyo_nendo = " + str(keijyo_nendo) + " AND sss.cat_cd = " + '"' + str(cat_cd) + '"'
    else:
        sql2 = (
            " WHERE sss.keijyo_nendo = "
            + str(keijyo_nendo)
            + " AND sss.cat_cd = "
            + '"'
            + str(cat_cd)
            + '"'
            + " AND sss.section_cd = "
            + '"'
            + str(section_cd)
            + '"'
        )

    sql3 = sum_common_sql.mz_keiyaku_grp(keiyaku_grp_cd)
    sql4 = " GROUP BY sss.coltd_cd) AS ss ON ss.coltd_cd = coltd.coltd_cd"
    sql5 = " WHERE coltd.onoff_cd = 'on' AND coltd.cat_cd = " + '"' + str(cat_cd) + '"'
    sql6 = " ORDER BY coltd.cat_cd, coltd.coltd_cd;"
    sql = sql1 + sql2 + sql3 + sql4 + sql5 + sql6
    sql_data = sql_config.mz_sql(sql)
    return sql_data
