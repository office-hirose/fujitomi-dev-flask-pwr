from _mod import sql_config


def mz_sql_order_store(keijyo_date_int):
    sql1 = """
        SELECT
        os.section_cd AS section_cd,
        sec.section_name AS section_name,
        os.cat_cd AS cat_cd,
        cat.cat_name_simple AS cat_name_simple,
        os.keiyaku_cd AS keiyaku_cd,
        ky.keiyaku_name AS keiyaku_name,
        os.mosikomi_cd AS mosikomi_cd,
        os.syoken_cd_main AS syoken_cd_main,
        os.syoken_cd_sub AS syoken_cd_sub,
        os.old_syoken_cd_main AS old_syoken_cd_main,
        os.old_syoken_cd_sub AS old_syoken_cd_sub,
        os.coltd_cd AS coltd_cd,
        col.name_simple AS coltd_name,
        os.kind_cd_main AS kind_cd_main,
        km.kind_name_main AS kind_name_main,
        os.kind_cd_sub AS kind_cd_sub,
        os.keijyo_date AS keijyo_date,
        os.siki_date AS siki_date,
        os.manki_date AS manki_date,
        os.ido_kai_date AS ido_kai_date,
        os.hoken_kikan_cd AS hoken_kikan_cd,
        hk.hoken_kikan_name AS hoken_kikan_name,
        os.pay_num_cd AS pay_num_cd,
        pn.pay_num_name AS pay_num_name,
        pn.keisu_year AS keisu_year,
        os.hoken_ryo AS hoken_ryo,
        os.hoken_ryo_year AS hoken_ryo_year,
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
        os.fee_gyotei3 AS fee_gyotei3,
        os.fee_cat AS fee_cat,
        os.fee_ritu AS fee_ritu,
        ROUND(os.fee_ritu * os.hoken_ryo * 0.01) AS fee_yen,
        os.fee_cd_all AS fee_cd_all,
        os.fee_seiho_kikan AS fee_seiho_kikan,
        os.fee_seiho_first AS fee_seiho_first,
        os.fee_seiho_next AS fee_seiho_next,
        os.hojin_kojin_cd AS hojin_kojin_cd,
        os.kei_name AS kei_name,
        os.kei_name_hira AS kei_name_hira,
        os.kei_post AS kei_post,
        os.kei_address AS kei_address,
        os.kei_tel AS kei_tel,
        os.fis_cd AS fis_cd

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

        LEFT JOIN sql_pay_num AS pn ON os.pay_num_cd = pn.pay_num_cd
        LEFT JOIN sql_hoken_kikan AS hk ON os.hoken_kikan_cd = hk.hoken_kikan_cd
        LEFT JOIN sql_gyotei AS gyo1 ON os.gyotei1_cd = gyo1.gyotei_cd
        LEFT JOIN sql_gyotei AS gyo2 ON os.gyotei2_cd = gyo2.gyotei_cd
        LEFT JOIN sql_gyotei AS gyo3 ON os.gyotei3_cd = gyo3.gyotei_cd
    """
    sql2 = " WHERE keijyo_date >= " + '"' + str(keijyo_date_int) + '"' + ";"
    sql = sql1 + sql2
    sql_data = sql_config.mz_sql(sql)
    return sql_data
