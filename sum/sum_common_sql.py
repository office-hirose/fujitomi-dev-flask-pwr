from _mod import sql_config


def mz_sql_section():
    sql = "SELECT * FROM sql_section WHERE onoff_cd = 'on' AND sort < 9999 ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_sql_cat():
    sql = "SELECT * FROM sql_cat ORDER BY cat_cd;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_sql_coltd(cat_cd):
    sql = (
        "SELECT * FROM sql_coltd WHERE onoff_cd = 'on' AND cat_cd = " + '"' + str(cat_cd) + '"' + " ORDER BY coltd_cd;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_sql_nendo(nyu_date):
    sql = "SELECT * FROM sql_kei_nyu_pay WHERE nyu_year_month_int = " + str(nyu_date) + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        nyu_nendo = dt["nyu_nendo"]
        break
    return nyu_nendo


def mz_staff_data(section_cd):
    sql = (
        "SELECT * FROM sql_staff WHERE sales_cd = 'on' AND section_cd = "
        + '"'
        + str(section_cd)
        + '"'
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# list data all/ list data all list
def mz_sql1():
    sql1 = """
        SELECT
            sss.keijyo_nendo AS keijyo_nendo,
            sss.keijyo_date AS keijyo_date,
            kei.keiyaku_name AS keiyaku_name,
            sec.section_name AS section_name,
            prk.person_kind_name AS person_kind_name,
            sss.staff_email AS staff_email,
            cat.cat_name_simple AS cat_name,
            col.name_simple AS coltd_name,
            sss.syoken_cd_main AS syoken_cd_main,
            kns.kind_name_main AS kind_name_main,
            kns.kind_name_sub AS kind_name_sub,
            pan.pay_num_name AS pay_num_name,
            sss.siki_date AS siki_date,
            sss.manki_date AS manki_date,
            sss.ido_kai_date AS ido_kai_date,
            sss.mikeika_month AS mikeika_month,
            sss.res_hoken_kikan_year AS res_hoken_kikan_year,
            sss.staff_fee_per AS staff_fee_per,
            sss.res_hoken_ryo AS res_hoken_ryo,
            sss.res_hoken_ryo_year AS res_hoken_ryo_year,
            sss.res_hoken_ryo_total AS res_hoken_ryo_total,
            sss.fee_ritu AS fee_ritu,
            sss.res_fee_money AS res_fee_money,
            sss.res_fee_money_year AS res_fee_money_year,
            sss.res_fee_money_total AS res_fee_money_total,
            sss.kei_name AS kei_name,
            stf.staff_name AS staff_name,
            gyo.name_simple AS gyotei_name
        FROM
            sql_sum_store AS sss
            LEFT JOIN sql_keiyaku AS kei ON sss.keiyaku_cd = kei.keiyaku_cd
            LEFT JOIN sql_cat AS cat ON sss.cat_cd = cat.cat_cd
            LEFT JOIN sql_coltd AS col ON sss.coltd_cd = col.coltd_cd

            LEFT JOIN sql_kind_sub AS kns ON
            sss.cat_cd = kns.cat_cd AND
            sss.coltd_cd = kns.coltd_cd AND
            sss.kind_cd_main = kns.kind_cd_main AND
            sss.kind_cd_sub = kns.kind_cd_sub

            LEFT JOIN sql_pay_num AS pan ON
            sss.pay_num_cd = pan.pay_num_cd

            LEFT JOIN sql_section AS sec ON
            sss.section_cd = sec.section_cd

            LEFT JOIN
            (SELECT min(staff_email) AS staff_email, min(name_simple) AS staff_name
            FROM sql_staff GROUP BY sql_staff.staff_email) AS stf ON
            sss.staff_email = stf.staff_email

            LEFT JOIN sql_gyotei AS gyo ON sss.gyotei_cd = gyo.gyotei_cd
            LEFT JOIN sql_person_kind AS prk ON sss.staff_kind = prk.person_kind
    """
    return sql1


def mz_keiyaku_grp(keiyaku_grp_cd):
    # 1=未設定, 2=新規, 3=更改, 4=満期落ち, 6=解約, 7=異動, 8=不成立, 9999=入力ミス
    # 新規更改
    if keiyaku_grp_cd == "1":
        sql3 = """
            AND (
            sss.keiyaku_cd = '1' or
            sss.keiyaku_cd = '2' or
            sss.keiyaku_cd = '3' or
            sss.keiyaku_cd = '4' or
            sss.keiyaku_cd = '5' or
            sss.keiyaku_cd = '8' or
            sss.keiyaku_cd = '9999'
            )
        """
    # 異動
    if keiyaku_grp_cd == "2":
        sql3 = " AND sss.keiyaku_cd = '7'"
    # 解約
    if keiyaku_grp_cd == "3":
        sql3 = " AND sss.keiyaku_cd = '6'"
    return sql3


# stf list
def mz_data_stf_list(kei_date_int, keiyaku_grp_cd, staff_email):
    sql1 = mz_sql1()
    sql2 = " WHERE sss.keijyo_date = " + str(kei_date_int) + " AND sss.staff_email = " + '"' + str(staff_email) + '"'
    sql3 = mz_keiyaku_grp(keiyaku_grp_cd)
    sql4 = " ORDER BY sss.keijyo_date, sss.cat_cd, sss.coltd_cd, " "sss.syoken_cd_main, sss.id;"
    sql = sql1 + sql2 + sql3 + sql4
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# sum stfのEmail送信の表示用
def mz_data_stf_kensu_for_email(kei_date_int, keiyaku_grp_cd, staff_email):
    sql1 = "SELECT count(*) AS cnt FROM sql_sum_store AS sss"
    sql2 = " WHERE sss.keijyo_date = " + str(kei_date_int) + " AND sss.staff_email = " + '"' + str(staff_email) + '"'
    sql3 = mz_keiyaku_grp(keiyaku_grp_cd)
    sql4 = " AND sss.staff_kind = 'main';"
    sql = sql1 + sql2 + sql3 + sql4
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        kensu_for_email = dt["cnt"]
    return kensu_for_email


# total list
def mz_data_total_list(kei_date_int, keiyaku_grp_cd):
    sql1 = mz_sql1()
    sql2 = " WHERE sss.keijyo_date = " + str(kei_date_int)
    sql3 = mz_keiyaku_grp(keiyaku_grp_cd)
    sql4 = " ORDER BY sss.keijyo_date, sss.cat_cd, sss.coltd_cd, " "sss.syoken_cd_main, sss.id;"
    sql = sql1 + sql2 + sql3 + sql4
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# sum totalのEmail送信の表示用
def mz_data_total_kensu_for_email(kei_date_int, keiyaku_grp_cd):
    sql1 = "SELECT count(*) AS cnt FROM sql_sum_store AS sss"
    sql2 = " WHERE sss.keijyo_date = " + str(kei_date_int)
    sql3 = " AND sss.staff_kind = 'main'"
    sql4 = mz_keiyaku_grp(keiyaku_grp_cd)
    sql = sql1 + sql2 + sql3 + sql4
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        kensu_for_email = dt["cnt"]
    return kensu_for_email


# list list, main sub gyotei
def mz_data_list_list(kei_date_int):
    sql1 = mz_sql1()
    sql2 = " WHERE sss.keijyo_date = " + str(kei_date_int)
    sql3 = " ORDER BY sss.keijyo_date, sss.cat_cd, sss.coltd_cd, sss.syoken_cd_main, sss.id;"
    sql = sql1 + sql2 + sql3
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# list list, main only
def mz_data_list_list_main(kei_date_int):
    sql1 = mz_sql1()
    sql2 = " WHERE sss.keijyo_date = " + str(kei_date_int)
    sql3 = " AND sss.staff_kind = 'main'"
    sql4 = " ORDER BY sss.keijyo_date, sss.cat_cd, sss.coltd_cd, sss.syoken_cd_main, sss.id;"
    sql = sql1 + sql2 + sql3 + sql4
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# sum totalのEmail送信の表示用
def mz_data_list_kensu_for_email(kei_date_int):
    sql1 = "SELECT count(*) AS cnt FROM sql_sum_store AS sss"
    sql2 = " WHERE sss.keijyo_date = " + str(kei_date_int)
    sql3 = " AND sss.staff_kind = 'main';"
    sql = sql1 + sql2 + sql3
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        kensu_for_email = dt["cnt"]
    return kensu_for_email


# sql1 = "SELECT count(*) AS cnt FROM sql_sum_store AS sss"
# sql2 = " WHERE sss.keijyo_date >= " + str(kei_date_int)
# sql3 = mz_keiyaku_grp(keiyaku_grp_cd)
# sql4 = " AND sss.staff_kind = 'main';"
# sql = sql1 + sql2 + sql3 + sql4
# sql_data = sql_config.mz_sql(sql)
# for dt in sql_data:
#     kensu_for_email = dt["cnt"]
# return kensu_for_email
