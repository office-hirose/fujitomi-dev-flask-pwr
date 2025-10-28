from _mod import sql_config


def mz_sql_fee_store(fdate_int, staff_email, main_sub_gyotei_all):
    sql1 = """
        SELECT
        fos.id,
        fos.nyu_nendo,
        fos.nyu_date,
        fos.kind_cd,
        fos.cat_cd,
        fos.coltd_cd,
        fos.siki_date,
        fos.manki_date,
        fos.kind_cd_main,
        fos.kind_cd_sub,
        fos.pay_num_cd,
        fos.syoken_cd_main,
        fos.syoken_cd_sub,
        fos.hoken_ryo,
        fos.fee_num,
        fos.section_cd,
        fos.section_cd_email,
        fos.pay_person_kind,
        fos.pay_person_cd,
        fos.pay_person_email,
        fos.pay_fee_per,
        fos.pay_fee_yen,
        fos.pay_gyotei_cd,
        fos.kei_name,
        fos.pay_gyotei_1year_over,
        fos.kaime,
        fos.fee_memo,
        col.name_simple AS coltd_name,
        ksub.kind_name_main AS kind_name_main,
        ksub.kind_name_sub AS kind_name_sub,
        pnc.pay_num_name AS pay_num_name,
        sec.section_name AS section_name,
        prk.person_kind_name AS person_kind_name,
        stf.staff_name AS staff_name,
        gyo.name_simple AS gyotei_name,
        pg1over.pay_gyotei_1year_over_name AS pay_gyotei_1year_over_name

        FROM
        sql_fee_order_store AS fos

        LEFT JOIN sql_coltd AS col ON
        fos.cat_cd = col.cat_cd AND
        fos.coltd_cd = col.coltd_cd

        LEFT JOIN sql_kind_sub AS ksub ON
        fos.cat_cd = ksub.cat_cd AND
        fos.coltd_cd = ksub.coltd_cd AND
        fos.kind_cd_main = ksub.kind_cd_main AND
        fos.kind_cd_sub = ksub.kind_cd_sub

        LEFT JOIN sql_pay_num AS pnc ON
        fos.pay_num_cd = pnc.pay_num_cd

        LEFT JOIN sql_section AS sec ON
        fos.section_cd = sec.section_cd

        LEFT JOIN sql_person_kind AS prk ON
        fos.pay_person_kind = prk.person_kind

        LEFT JOIN (SELECT min(staff_email) AS staff_email, min(name_simple) AS staff_name
        FROM sql_staff GROUP BY sql_staff.staff_email) AS stf ON
        fos.pay_person_email = stf.staff_email

        LEFT JOIN sql_gyotei AS gyo ON
        fos.pay_gyotei_cd = gyo.gyotei_cd

        LEFT JOIN sql_pay_gyotei_1year_over AS pg1over ON
        fos.pay_gyotei_1year_over = pg1over.pay_gyotei_1year_over_cd
        """
    sql_main = (
        " WHERE fos.nyu_date = "
        + str(fdate_int)
        + " AND fos.pay_person_email = "
        + '"'
        + staff_email
        + '"'
        + " AND fos.pay_person_kind = 'main'"
        + " ORDER BY cat_cd, coltd_cd, syoken_cd_main, syoken_cd_sub, id, kind_cd;"
    )
    sql_sub = (
        " WHERE fos.nyu_date = "
        + str(fdate_int)
        + " AND fos.pay_person_email = "
        + '"'
        + staff_email
        + '"'
        + " AND fos.pay_person_kind = 'sub'"
        + " ORDER BY cat_cd, coltd_cd, syoken_cd_main, syoken_cd_sub, id, kind_cd;"
    )
    sql_gyotei = (
        " WHERE fos.nyu_date = "
        + str(fdate_int)
        + " AND fos.pay_person_email = "
        + '"'
        + staff_email
        + '"'
        + " AND (fos.pay_person_kind = 'gyotei1' OR fos.pay_person_kind = 'gyotei2' OR fos.pay_person_kind = 'gyotei3')"
        + " ORDER BY cat_cd, coltd_cd, syoken_cd_main, syoken_cd_sub, id, kind_cd;"
    )
    sql_all = (
        " WHERE fos.nyu_date = "
        + str(fdate_int)
        + " AND fos.pay_person_email = "
        + '"'
        + staff_email
        + '"'
        + " ORDER BY cat_cd, coltd_cd, syoken_cd_main, syoken_cd_sub, id, kind_cd;"
    )

    if main_sub_gyotei_all == "main":
        sql = sql1 + sql_main
    if main_sub_gyotei_all == "sub":
        sql = sql1 + sql_sub
    if main_sub_gyotei_all == "gyotei":
        sql = sql1 + sql_gyotei
    if main_sub_gyotei_all == "all":
        sql = sql1 + sql_all

    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_sql_fee_store_cnt(fdate_int, staff_email):
    sql_data_cnt = 0
    sql = (
        "SELECT COUNT(*) AS cnt FROM sql_fee_order_store"
        + " WHERE nyu_date = "
        + str(fdate_int)
        + " AND pay_person_email = "
        + '"'
        + staff_email
        + '"'
        + " GROUP BY syoken_cd_main;"
    )
    sql_data = sql_config.mz_sql(sql)
    sql_data_cnt = len(sql_data)
    return sql_data_cnt


# 主担当を調べる
def mz_main_staff_name(coltd_cd, syoken_cd_main, syoken_cd_sub):
    sql = (
        "SELECT stf1.name_simple AS staff_name"
        + " FROM sql_order_store AS os"
        + " LEFT JOIN sql_staff AS stf1 ON os.staff1_cd = stf1.staff_cd"
        + " WHERE os.coltd_cd = "
        + '"'
        + coltd_cd
        + '"'
        + " AND os.syoken_cd_main = "
        + '"'
        + syoken_cd_main
        + '"'
        + " AND os.syoken_cd_sub = "
        + '"'
        + syoken_cd_sub
        + '"'
        + " ORDER BY os.syoken_cd_sub;"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff_name = dt["staff_name"]
        break
    staff_name = "主担当：" + staff_name
    return staff_name
