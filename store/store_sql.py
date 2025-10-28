from _mod import sql_config


def select_from_sql():
    select1 = """
        SELECT
        os.fis_cd,
        os.cat_cd,
        os.keiyaku_cd,
        ky.keiyaku_name,
        ky.w3_text_color AS keiyaku_w3_text_color,
        os.exe_sta,
        sta.sta_name,
        os.siki_date,
        os.manki_date,
        os.syoken_cd_main,
        os.syoken_cd_sub,
        os.old_syoken_cd_main,
        os.old_syoken_cd_sub,
        os.mosikomi_cd,
        os.keijyo_date,
        col.name_simple AS coltd_name,
        km.kind_name_main,
        ks.kind_name_sub,
        os.kei_name,
        os.memo,
        os.memo_json,
        pn.pay_num_name,
        os.hoken_kikan_cd,
        hk.hoken_kikan_name,
        hk.w3_text_color AS hoken_kikan_w3_text_color,
        os.hoken_kikan_year,
        os.hoken_ryo,
        os.hoken_ryo_year,
        os.ido_kai_hoken_ryo,
        os.ido_kai_date,
        sec.section_name,
        os.staff1_cd,
        os.staff2_cd,
        os.staff3_cd,
        sf1.name_simple AS staff1_name,
        sf2.name_simple AS staff2_name,
        sf3.name_simple AS staff3_name,
        gyo1.name_simple AS gyotei1_name,
        gyo2.name_simple AS gyotei2_name,
        gyo3.name_simple AS gyotei3_name,
        CAST(os.fee_staff1 AS CHAR) AS fee_staff1,
        CAST(os.fee_staff2 AS CHAR) AS fee_staff2,
        CAST(os.fee_staff3 AS CHAR) AS fee_staff3,
        CAST(os.fee_gyotei1 AS CHAR) AS fee_gyotei1,
        CAST(os.fee_gyotei2 AS CHAR) AS fee_gyotei2,
        CAST(os.fee_gyotei3 AS CHAR) AS fee_gyotei3,
        os.fee_cat,
        os.fee_ritu,
        os.fee_seiho_kikan,
        os.fee_seiho_first,
        os.fee_seiho_next,
        sf1.w3_text_color AS staff1_w3_text_color,
        os.bosyu_cd,
        os.valid_cd,
        os.regi_email,
        regi_em.name_simple AS regi_name,
        os.regi_time
        """
    from1 = """
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
        LEFT JOIN sql_staff AS regi_em ON os.regi_email = regi_em.staff_email
        LEFT JOIN sql_sta AS sta ON os.exe_sta = sta.sta_cd
        """
    return select1, from1


# store list sql
def list_sql(cat_cd, keijyo_date, section_cd, staff_cd, keiyaku_cd, coltd_cd):
    # select1, from1
    select1, from1 = select_from_sql()
    # where1
    where1 = (
        " WHERE"
        + " os.cat_cd = "
        + '"'
        + cat_cd
        + '"'
        + " AND"
        + " os.keijyo_date = "
        + str(keijyo_date)
        + " AND"
        + " os.section_cd = "
        + '"'
        + section_cd
        + '"'
    )
    # where2
    if staff_cd == "0":
        where2 = ""
    else:
        where2 = " AND os.staff1_cd = " + '"' + staff_cd + '"'
    # where3
    if keiyaku_cd == "0":
        where3 = ""
    else:
        where3 = " AND os.keiyaku_cd = " + '"' + keiyaku_cd + '"'
    # where4
    if coltd_cd == "0":
        where4 = ""
    else:
        where4 = " AND os.coltd_cd = " + '"' + coltd_cd + '"'
    # order
    order1 = " ORDER BY os.coltd_cd, os.syoken_cd_main, os.syoken_cd_sub, os.siki_date, os.keijyo_date;"
    # execute
    sql = select1 + from1 + where1 + where2 + where3 + where4 + order1
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# store search sql
def search_sql(cat_cd, search_text):
    # select1, from1
    select1, from1 = select_from_sql()
    # where1
    where1 = (
        " WHERE"
        + " os.cat_cd = "
        + '"'
        + cat_cd
        + '"'
        + " AND"
        + ' os.search_text LIKE "%'
        + search_text
        + '%"'
        + " ORDER BY os.coltd_cd, os.syoken_cd_main, os.syoken_cd_sub, os.siki_date, os.keijyo_date;"
    )
    sql = select1 + from1 + where1
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# fis_cd sql
def fis_cd_sql(fis_cd):
    # select1, from1
    select1, from1 = select_from_sql()
    # where1
    where1 = " WHERE os.fis_cd = " + '"' + fis_cd + '"' + ";"
    sql = select1 + from1 + where1
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# store pdf sql
def pdf_sql(fis_cd):
    # select1, from1
    select1, from1 = select_from_sql()
    # where1
    where1 = " WHERE os.fis_cd = " + str(fis_cd) + ";"
    sql = select1 + from1 + where1
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# store excel sql
def excel_sql(fis_cd):
    # select1, from1
    select1, from1 = select_from_sql()
    # where1
    where1 = " WHERE os.fis_cd = " + str(fis_cd) + ";"
    sql = select1 + from1 + where1
    sql_data = sql_config.mz_sql(sql)
    return sql_data
