from _mod import sql_config


def mz_sql_order_store(keijyo_date_int, section_cd, staff_cd, stf_key):
    sql1 = """
        SELECT
        sec.section_name AS sec_name,
        os.keijyo_date AS keijyo_date,
        os.siki_date AS siki_date,
        os.manki_date AS manki_date,
        ky.keiyaku_name AS keiyaku_name,
        os.syoken_cd_main AS syoken_cd_main,
        os.syoken_cd_sub AS syoken_cd_sub,
        os.old_syoken_cd_main AS old_syoken_cd_main,
        os.old_syoken_cd_sub AS old_syoken_cd_sub,
        os.mosikomi_cd AS mosikomi,
        cat.cat_name_simple AS cat_name,
        col.name_simple AS coltd_name,
        km.kind_name_main AS kind_name_main,
        ks.kind_name_sub AS kind_name_sub,
        os.kei_name AS kei_name,
        os.memo AS memo,
        pn.pay_num_name AS pay_num_name,
        os.hoken_ryo AS hoken_ryo,
        os.hoken_ryo_year AS hoken_ryo_year,
        ROUND(os.fee_ritu * os.hoken_ryo * 0.01) AS fee_sonpo_yen,
        os.fee_seiho_kikan AS fee_seiho_kikan,
        os.fee_seiho_first AS fee_seiho_first,
        os.fee_seiho_next AS fee_seiho_next,
        os.ido_kai_date AS ido_kai_date,
        os.ido_kai_hoken_ryo AS ido_kai_hoken_ryo,
        sf1.name_simple AS staff1_name,
        sf2.name_simple AS staff2_name,
        sf3.name_simple AS staff3_name,
        gyo1.name_simple AS gyotei1_name,
        gyo2.name_simple AS gyotei2_name,
        gyo3.name_simple AS gyotei3_name,
        os.fee_staff1 AS fee_staff1,
        os.fee_staff2 AS fee_staff2,
        os.fee_staff3 AS fee_staff3,
        os.fee_gyotei1 AS fee_gyotei1,
        os.fee_gyotei2 AS fee_gyotei2,
        os.fee_gyotei3 AS fee_gyotei3

        FROM sql_order_store AS os
        LEFT JOIN sql_keiyaku AS ky ON os.keiyaku_cd = ky.keiyaku_cd
        LEFT JOIN sql_section AS sec ON os.section_cd = sec.section_cd
        LEFT JOIN sql_staff AS sf1 ON os.staff1_cd = sf1.staff_cd
        LEFT JOIN sql_staff AS sf2 ON os.staff2_cd = sf2.staff_cd
        LEFT JOIN sql_staff AS sf3 ON os.staff3_cd = sf3.staff_cd
        LEFT JOIN sql_cat AS cat ON os.cat_cd = cat.cat_cd
        LEFT JOIN sql_coltd AS col ON os.coltd_cd = col.coltd_cd
        LEFT JOIN sql_kind_main AS km ON
        os.cat_cd = km.cat_cd AND
        os.coltd_cd = km.coltd_cd AND
        os.kind_cd_main = km.kind_cd_main

        LEFT JOIN sql_kind_sub AS ks ON
        os.cat_cd = ks.cat_cd AND
        os.coltd_cd = ks.coltd_cd AND
        os.kind_cd_main = ks.kind_cd_main AND
        os.kind_cd_sub = ks.kind_cd_sub

        LEFT JOIN sql_pay_num AS pn ON os.pay_num_cd = pn.pay_num_cd
        LEFT JOIN sql_hoken_kikan AS hk ON os.hoken_kikan_cd = hk.hoken_kikan_cd
        LEFT JOIN sql_gyotei AS gyo1 ON os.gyotei1_cd = gyo1.gyotei_cd
        LEFT JOIN sql_gyotei AS gyo2 ON os.gyotei2_cd = gyo2.gyotei_cd
        LEFT JOIN sql_gyotei AS gyo3 ON os.gyotei3_cd = gyo3.gyotei_cd
    """

    sql2 = " WHERE os.keijyo_date = " + str(keijyo_date_int) + " AND os.section_cd = " + '"' + str(section_cd) + '"'
    sql4 = " ORDER BY os.cat_cd, os.coltd_cd, os.syoken_cd_main, os.syoken_cd_sub;"

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
