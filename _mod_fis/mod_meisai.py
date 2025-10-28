from _mod import sql_config


def mz_meisai_data(syoken_cd_main):
    sql1 = """
        SELECT
        os.syoken_cd_main,
        os.syoken_cd_sub,
        os.keiyaku_cd,
        kei.keiyaku_name,
        os.keijyo_date,
        os.ngw_keijyo_date,
        os.siki_date,
        os.manki_date,
        os.hoken_ryo,
        os.hoken_ryo_year,
        os.ido_kai_date,
        os.ido_kai_hoken_ryo
        FROM sql_order_store AS os
        LEFT JOIN sql_keiyaku AS kei ON os.keiyaku_cd = kei.keiyaku_cd
        """
    sql2 = " WHERE os.syoken_cd_main = " + '"' + syoken_cd_main + '"'
    sql3 = " ORDER BY os.syoken_cd_sub;"
    sql = sql1 + sql2 + sql3
    sql_data = sql_config.mz_sql(sql)
    return sql_data
