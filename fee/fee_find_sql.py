from _mod import sql_config


def select_from_sql():
    select_from = """
        SELECT
        fos.id,
        fos.nyu_nendo,
        fos.nyu_date,

        fos.kind_cd,
        fkind.kind_name AS kind_name,

        fos.coltd_cd,
        col.name_simple AS coltd_name,

        fos.siki_date,
        fos.manki_date,

        fos.pay_num_cd,
        paynum.pay_num_name AS pay_num_name,

        fos.syoken_cd_main,
        fos.syoken_cd_sub,
        fos.hoken_ryo,
        fos.fee_num,

        fos.section_cd,
        sec.section_name AS section_name,

        fos.pay_person_kind,
        pkind.person_kind_name AS person_kind_name,

        fos.pay_person_cd,
        stf.name_simple AS staff_name,

        fos.pay_fee_per,
        fos.pay_fee_yen,

        fos.pay_gyotei_cd,
        gyo.name_simple AS gyotei_name,

        fos.kei_name,

        fos.pay_gyotei_1year_over,
        pay1over.pay_gyotei_1year_over_name,

        fos.kaime,
        fos.fee_memo

        FROM sql_fee_order_store AS fos

        LEFT JOIN sql_fee_kind AS fkind ON fos.kind_cd = fkind.kind_cd
        LEFT JOIN sql_coltd AS col ON fos.coltd_cd = col.coltd_cd
        LEFT JOIN sql_pay_num AS paynum ON fos.pay_num_cd = paynum.pay_num_cd
        LEFT JOIN sql_section AS sec ON fos.section_cd = sec.section_cd
        LEFT JOIN sql_person_kind AS pkind ON fos.pay_person_kind = pkind.person_kind
        LEFT JOIN sql_staff AS stf ON fos.pay_person_cd = stf.staff_cd
        LEFT JOIN sql_gyotei AS gyo ON fos.pay_gyotei_cd = gyo.gyotei_cd
        LEFT JOIN sql_pay_gyotei_1year_over AS pay1over ON fos.pay_gyotei_1year_over = pay1over.pay_gyotei_1year_over_cd
    """
    return select_from


def list_sql(nyu_date, section_cd, staff_cd, coltd_cd):
    select_from = select_from_sql()

    where1 = " WHERE fos.nyu_date = " + str(nyu_date) + " AND fos.section_cd = " + '"' + section_cd + '"'

    if staff_cd == "0" and coltd_cd == "0":
        where2 = ""

    if staff_cd != "0" and coltd_cd == "0":
        where2 = " AND fos.pay_person_cd = " + '"' + staff_cd + '"'

    if staff_cd == "0" and coltd_cd != "0":
        where2 = " AND fos.coltd_cd = " + '"' + coltd_cd + '"'

    if staff_cd != "0" and coltd_cd != "0":
        where2 = " AND fos.pay_person_cd = " + '"' + staff_cd + '"' + " AND fos.coltd_cd = " + '"' + coltd_cd + '"'

    order = " ORDER BY fos.nyu_date, fos.id;"
    sql = select_from + where1 + where2 + order
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# fee find search
def search_sql(syoken_cd_main):
    select_from = select_from_sql()
    where = " WHERE fos.syoken_cd_main LIKE " + '"%' + syoken_cd_main + '%"'
    order = " ORDER BY fos.nyu_date, fos.id;"
    sql = select_from + where + order
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# fee find pdf sql
def pdf_sql(id):
    select_from = select_from_sql()
    where = " WHERE fos.id = " + str(id) + ";"
    sql = select_from + where
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# fee find excel sql
def excel_sql(id):
    select_from = select_from_sql()
    where = " WHERE fos.id = " + str(id) + ";"
    sql = select_from + where
    sql_data = sql_config.mz_sql(sql)
    return sql_data
