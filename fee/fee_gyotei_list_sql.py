from _mod import sql_config


def mz_sql_fee_order_store(fdate_int, gyotei_cd):
    # 振替手数料を表示する場合 kind_cd
    # sql = 'SELECT * FROM sql_fee_order_store' + \
    #     ' WHERE nyu_date = ' + str(fdate_int) + \
    #     ' AND pay_gyotei_cd = ' + '\"' + str(gyotei_cd) + '\"' + \
    #     ' AND pay_fee_yen != 0' + \
    #     ' ORDER BY cat_cd, coltd_cd, syoken_cd_main, kind_cd'

    # 振替手数料を表示しない場合 kind_cd
    sql1 = """
        SELECT
        min(nyu_nendo) AS nyu_nendo,
        min(nyu_date) AS nyu_date,
        min(kind_cd) AS kind_cd,
        min(cat_cd) AS cat_cd,
        min(coltd_cd) AS coltd_cd,
        min(siki_date) AS siki_date,
        min(manki_date) AS manki_date,
        min(kind_cd_main) AS kind_cd_main,
        min(kind_cd_sub) AS kind_cd_sub,
        min(pay_num_cd) AS pay_num_cd,
        min(syoken_cd_main) AS syoken_cd_main,
        min(syoken_cd_sub) AS syoken_cd_sub,
        min(hoken_ryo) AS hoken_ryo,
        sum(fee_num) AS fee_num,
        min(section_cd) AS section_cd,
        min(section_cd_email) AS section_cd_email,
        min(pay_person_kind) AS pay_person_kind,
        min(pay_person_cd) AS pay_person_cd,
        min(pay_person_email) AS pay_person_email,
        min(pay_fee_per) AS pay_fee_per,
        sum(pay_fee_yen) AS pay_fee_yen,
        min(pay_gyotei_cd) AS pay_gyotei_cd,
        min(kei_name) AS kei_name,
        min(pay_gyotei_1year_over) AS pay_gyotei_1year_over,
        max(kaime) AS kaime,
        min(fee_memo) AS fee_memo
        FROM sql_fee_order_store
        """

    # 提携ありだが手数料配分が０の場合は表示しない
    sql2 = (
        ""
        + " WHERE nyu_date = "
        + str(fdate_int)
        + " AND pay_gyotei_cd = "
        + '"'
        + str(gyotei_cd)
        + '"'
        + " AND pay_fee_yen != 0"
        + " GROUP BY pay_gyotei_cd, cat_cd, coltd_cd, syoken_cd_main"
        + " ORDER BY cat_cd, coltd_cd, syoken_cd_main, kind_cd;"
    )

    # 提携ありだが手数料配分が０の場合でも表示する
    # sql2 = '' + \
    #     ' WHERE nyu_date = ' + str(fdate_int) + \
    #     ' AND pay_gyotei_cd = ' + '\"' + str(gyotei_cd) + '\"' + \
    #     ' GROUP BY pay_gyotei_cd, cat_cd, coltd_cd, syoken_cd_main' + \
    #     ' ORDER BY cat_cd, coltd_cd, syoken_cd_main, kind_cd;'

    sql = sql1 + sql2
    sql_data = sql_config.mz_sql(sql)
    return sql_data
