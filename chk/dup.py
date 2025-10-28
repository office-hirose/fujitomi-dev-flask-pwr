import sys
from flask import request
from _mod import mod_base, sql_config
from _mod_fis import mod_cat


def dup():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    cat_cd = obj["cat_cd"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "cat_data_all": [],
            "dup_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "cat_data_all": mod_cat.mz_cat_data_all(),
            "dup_data_all": dup_data_sql(cat_cd),
        }
    return dic


def dup_data_sql(cat_cd):
    seiho_sql = """
        SELECT
            main.keiyaku_cd,
            keiyaku.keiyaku_name,
            main.coltd_cd,
            main.syoken_cd_main,
            main.kei_name,
            main.cnt
        FROM
        (
        SELECT
            (MIN( keiyaku_cd )) AS keiyaku_cd,
            (MIN( coltd_cd )) AS coltd_cd,
            syoken_cd_main,
            (MIN( kei_name )) AS kei_name,
            count(*) AS cnt
        FROM sql_order_store
        WHERE cat_cd = '1' AND dup_sta = ''
        GROUP BY syoken_cd_main, syoken_cd_sub, keiyaku_cd, ido_kai_date) AS main
        LEFT JOIN sql_keiyaku AS keiyaku ON main.keiyaku_cd = keiyaku.keiyaku_cd
        WHERE cnt > 1
        ORDER BY main.syoken_cd_main, main.keiyaku_cd;
    """

    sonpo_sql = """
        SELECT
            main.keiyaku_cd,
            keiyaku.keiyaku_name,
            main.coltd_cd,
            main.syoken_cd_main,
            main.kei_name,
            main.cnt
        FROM
        (
        SELECT
            (MIN( keiyaku_cd )) AS keiyaku_cd,
            (MIN( coltd_cd )) AS coltd_cd,
            syoken_cd_main,
            (MIN( kei_name )) AS kei_name,
            count(*) AS cnt
        FROM sql_order_store
        WHERE cat_cd = '2' AND dup_sta = ''
        GROUP BY syoken_cd_main, syoken_cd_sub, keiyaku_cd, hoken_ryo, ido_kai_hoken_ryo) AS main
        LEFT JOIN sql_keiyaku AS keiyaku ON main.keiyaku_cd = keiyaku.keiyaku_cd
        WHERE cnt > 1
        ORDER BY main.syoken_cd_main, main.keiyaku_cd;
    """

    syotan_sql = """
        SELECT
            main.keiyaku_cd,
            keiyaku.keiyaku_name,
            main.coltd_cd,
            main.syoken_cd_main,
            main.kei_name,
            main.cnt
        FROM
        (
        SELECT
            (MIN( keiyaku_cd )) AS keiyaku_cd,
            (MIN( coltd_cd )) AS coltd_cd,
            syoken_cd_main,
            (MIN( kei_name )) AS kei_name,
            count(*) AS cnt
        FROM sql_order_store
        WHERE cat_cd = '3' AND dup_sta = ''
        GROUP BY syoken_cd_main, keiyaku_cd) AS main
        LEFT JOIN sql_keiyaku AS keiyaku ON main.keiyaku_cd = keiyaku.keiyaku_cd
        WHERE cnt > 1
        ORDER BY main.syoken_cd_main, main.keiyaku_cd;
    """

    if cat_cd == "1":
        sql = seiho_sql

    if cat_cd == "2":
        sql = sonpo_sql

    if cat_cd == "3":
        sql = syotan_sql

    sql_data = sql_config.mz_sql(sql)
    return sql_data


def modal_dup_data():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    cat_cd = obj["cat_cd"]
    keiyaku_cd = obj["keiyaku_cd"]
    syoken_cd_main = obj["syoken_cd_main"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "modal_dup_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "modal_dup_data": modal_dup_data_sql(cat_cd, keiyaku_cd, syoken_cd_main),
        }
    return dic


def modal_dup_data_sql(cat_cd, keiyaku_cd, syoken_cd_main):
    select1 = """
        SELECT
        os.fis_cd,
        os.cat_cd,
        os.coltd_cd,
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
    where1 = (
        " WHERE"
        + " os.cat_cd = "
        + '"'
        + cat_cd
        + '"'
        + " AND"
        + " os.keiyaku_cd = "
        + str(keiyaku_cd)
        + " AND"
        + " os.syoken_cd_main = "
        + '"'
        + syoken_cd_main
        + '"'
        + " ORDER BY os.fis_cd"
    )
    sql = select1 + from1 + where1
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def modal_dup_data_del():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    fis_cd = obj["fis_cd"]
    cat_cd = obj["cat_cd"]
    keiyaku_cd = obj["keiyaku_cd"]
    syoken_cd_main = obj["syoken_cd_main"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "modal_dup_data": [],
        }
    else:
        # sql delete
        sql = "DELETE FROM sql_order_store WHERE fis_cd = %s"
        con = sql_config.mz_sql_con()
        cur = con.cursor()
        cur.execute(sql, (fis_cd,))
        con.commit()

        dic = {
            "level_error": level_error,
            "modal_dup_data": modal_dup_data_sql(cat_cd, keiyaku_cd, syoken_cd_main),
        }
    return dic
