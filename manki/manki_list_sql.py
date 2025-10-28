from _mod import sql_config


def mz_sql_order_store(manki_date_int, section_cd, staff_cd, stf_key):
    manki_date_s = manki_date_int * 100
    manki_date_e = manki_date_s + 32

    sql1 = """
        SELECT
        ky.keiyaku_name AS keiyaku_name,
        os.syoken_cd_main AS syoken_cd_main,
        os.syoken_cd_sub AS syoken_cd_sub,
        os.old_syoken_cd_main AS old_syoken_cd_main,
        os.old_syoken_cd_sub AS old_syoken_cd_sub,
        os.siki_date AS siki_date,
        os.manki_date AS manki_date,
        os.ido_kai_date AS ido_kai_date,
        col.name_simple AS coltd_name,
        km.kind_name_main AS kind_name_main,
        ks.kind_name_sub AS kind_name_sub,
        os.kei_name AS kei_name,
        os.hoken_ryo AS hoken_ryo,
        sf1.name_simple AS staff1_name,
        sf2.name_simple AS staff2_name,
        sf3.name_simple AS staff3_name,
        gyo1.name_simple AS gyotei1_name,
        gyo2.name_simple AS gyotei2_name,
        gyo3.name_simple AS gyotei3_name
        FROM sql_order_store AS os
        LEFT JOIN sql_keiyaku AS ky ON os.keiyaku_cd = ky.keiyaku_cd
        LEFT JOIN sql_staff AS sf1 ON os.staff1_cd = sf1.staff_cd
        LEFT JOIN sql_staff AS sf2 ON os.staff2_cd = sf2.staff_cd
        LEFT JOIN sql_staff AS sf3 ON os.staff3_cd = sf3.staff_cd
        LEFT JOIN sql_coltd AS col ON os.coltd_cd = col.coltd_cd

        LEFT JOIN sql_kind_main AS km ON
        os.cat_cd = km.cat_cd AND os.coltd_cd = km.coltd_cd AND os.kind_cd_main = km.kind_cd_main

        LEFT JOIN sql_kind_sub AS ks ON
        os.cat_cd = ks.cat_cd AND
        os.coltd_cd = ks.coltd_cd AND
        os.kind_cd_main = ks.kind_cd_main AND
        os.kind_cd_sub = ks.kind_cd_sub

        LEFT JOIN sql_gyotei AS gyo1 ON os.gyotei1_cd = gyo1.gyotei_cd
        LEFT JOIN sql_gyotei AS gyo2 ON os.gyotei2_cd = gyo2.gyotei_cd
        LEFT JOIN sql_gyotei AS gyo3 ON os.gyotei3_cd = gyo3.gyotei_cd
    """

    sql2 = (
        " WHERE os.cat_cd = "
        + '"'
        + "2"
        + '"'
        + " AND os.manki_date > "
        + str(manki_date_s)
        + " AND os.manki_date < "
        + str(manki_date_e)
        + " AND os.section_cd = "
        + '"'
        + str(section_cd)
        + '"'
    )
    sql4 = " ORDER BY os.coltd_cd, os.syoken_cd_main, os.syoken_cd_sub;"

    if stf_key == "staff1":
        if staff_cd == "all":
            sql3 = ""
        else:
            sql3 = " AND os.staff1_cd = " + '"' + str(staff_cd) + '"'
        sql = sql1 + sql2 + sql3 + sql4
        sql_data = sql_config.mz_sql(sql)

    if stf_key == "staff2":
        if staff_cd == "all":
            sql_data = ""
        else:
            sql3 = " AND os.staff2_cd = " + '"' + str(staff_cd) + '"'
            sql = sql1 + sql2 + sql3 + sql4
            sql_data = sql_config.mz_sql(sql)

    if stf_key == "staff3":
        if staff_cd == "all":
            sql_data = ""
        else:
            sql3 = " AND os.staff3_cd = " + '"' + str(staff_cd) + '"'
            sql = sql1 + sql2 + sql3 + sql4
            sql_data = sql_config.mz_sql(sql)

    return sql_data
