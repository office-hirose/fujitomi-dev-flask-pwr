from _mod import sql_config
from sum import sum_common_sql


# 契約顧客件数 当月
def mz_keiko_tou(keijyo_date, keiyaku_grp_cd, cat_cd, section_cd, staff_email):
    sql1 = """
        SELECT
        coltd.coltd_cd AS coltd_cd,
        coltd.name_simple AS coltd_name,
        kc.keijyo_cnt AS keijyo_cnt

        FROM sql_coltd AS coltd

        LEFT JOIN
        (
        SELECT
        count(*) AS keijyo_cnt,
        ss.coltd_cd

        FROM
        (
        SELECT
        count(*) AS cnt,
        max(sss.coltd_cd) AS coltd_cd,
        max(sss.kei_name_nospace) AS kei_name_nospace

        FROM sql_sum_store AS sss
    """

    if section_cd == "0":
        sql2 = (
            "WHERE sss.keijyo_date = "
            + str(keijyo_date)
            + " AND sss.cat_cd = "
            + '"'
            + str(cat_cd)
            + '"'
            + " AND sss.staff_email = "
            + '"'
            + str(staff_email)
            + '"'
            + " AND sss.staff_kind = 'main'"
        )
    else:
        sql2 = (
            "WHERE sss.keijyo_date = "
            + str(keijyo_date)
            + " AND sss.cat_cd = "
            + '"'
            + str(cat_cd)
            + '"'
            + " AND sss.section_cd = "
            + '"'
            + str(section_cd)
            + '"'
            + " AND sss.staff_email = "
            + '"'
            + str(staff_email)
            + '"'
            + " AND sss.staff_kind = 'main'"
        )

    sql3 = sum_common_sql.mz_keiyaku_grp(keiyaku_grp_cd)
    sql4 = """
        GROUP BY
        sss.coltd_cd, sss.kei_name_nospace
        ) AS ss

        GROUP BY
        coltd_cd
        ) AS kc
        ON kc.coltd_cd = coltd.coltd_cd
    """
    sql5 = " WHERE coltd.onoff_cd = 'on' AND coltd.cat_cd = " + '"' + str(cat_cd) + '"'
    sql6 = " ORDER BY coltd.cat_cd, coltd.coltd_cd;"
    sql = sql1 + sql2 + sql3 + sql4 + sql5 + sql6
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 契約顧客件数 累計
def mz_keiko_rui(keijyo_nendo, keijyo_date, keiyaku_grp_cd, cat_cd, section_cd, staff_email):
    sql1 = """
        SELECT kc.keijyo_cnt AS keijyo_cnt

        FROM sql_coltd AS coltd

        LEFT JOIN
        (
        SELECT
        count(*) AS keijyo_cnt,
        ss.coltd_cd

        FROM
        (
        SELECT
        count(*) AS cnt,
        max(sss.coltd_cd) AS coltd_cd,
        max(sss.kei_name_nospace) AS kei_name_nospace

        FROM sql_sum_store AS sss
    """

    if section_cd == "0":
        sql2 = (
            " WHERE sss.keijyo_nendo = "
            + str(keijyo_nendo)
            + " AND sss.cat_cd = "
            + '"'
            + str(cat_cd)
            + '"'
            + " AND sss.staff_email = "
            + '"'
            + str(staff_email)
            + '"'
            + " AND sss.staff_kind = 'main'"
        )
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
            + " AND sss.staff_email = "
            + '"'
            + str(staff_email)
            + '"'
            + " AND sss.staff_kind = 'main'"
        )

    sql3 = sum_common_sql.mz_keiyaku_grp(keiyaku_grp_cd)
    sql4 = """
        GROUP BY
        sss.coltd_cd, sss.kei_name_nospace
        ) AS ss

        GROUP BY
        coltd_cd
        ) AS kc
        ON kc.coltd_cd = coltd.coltd_cd
    """
    sql5 = " WHERE coltd.onoff_cd = 'on' AND coltd.cat_cd = " + '"' + str(cat_cd) + '"'
    sql6 = " ORDER BY coltd.cat_cd, coltd.coltd_cd;"
    sql = sql1 + sql2 + sql3 + sql4 + sql5 + sql6
    sql_data = sql_config.mz_sql(sql)
    return sql_data
