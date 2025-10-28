from _mod import sql_config


def mz_nttgw_search(cat_cd, syoken_cd_main):
    sql1 = """
        SELECT
        ngw.id,
        ngw.imp_file_name,
        ngw.keiyaku_cd,
        kei.keiyaku_name,
        kei.w3_text_color AS keiyaku_w3_text_color,

        ngw.siki_date,
        ngw.manki_date,
        ngw.ido_kai_date,

        ngw.syoken_cd_main,
        ngw.syoken_cd_sub,
        ngw.old_syoken_cd_main,
        ngw.old_syoken_cd_sub,
        ngw.keijyo_date,

        ngw.cat_cd,
        ngw.coltd_cd,
        col.name_simple AS coltd_name,
        ngw.kei_name,

        ngw.kind_cd_main,
        ngw.kind_cd_sub,

        ngw.hoken_ryo,
        ngw.ido_kai_hoken_ryo,

        ngw.bosyu_cd,
        sub.kind_name_main,
        sub.kind_name_sub

        FROM sql_nttgw_dat AS ngw

        LEFT JOIN sql_keiyaku AS kei
        ON ngw.keiyaku_cd = kei.keiyaku_cd

        LEFT JOIN sql_coltd AS col
        ON ngw.coltd_cd = col.coltd_cd

        LEFT JOIN sql_kind_sub AS sub
        ON ngw.coltd_cd = sub.coltd_cd
        AND ngw.kind_cd_main = sub.kind_cd_main
        AND ngw.kind_cd_sub = sub.kind_cd_sub
        """
    sql2 = (
        " WHERE ngw.cat_cd = "
        + '"'
        + cat_cd
        + '"'
        + ' AND ngw.syoken_cd_main LIKE "%'
        + syoken_cd_main
        + '%"'
        + " ORDER BY ngw.coltd_cd, ngw.syoken_cd_main, ngw.syoken_cd_sub, ngw.id;"
    )
    sql = sql1 + sql2
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_nttgw_import(id):
    sql = "SELECT * FROM sql_nttgw_dat WHERE id = " + str(id) + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data
