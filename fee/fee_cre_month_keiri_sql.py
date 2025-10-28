from _mod import sql_config


# delete record execute
def mz_sql_fee_order_store_del(nyu_date_int):
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = "DELETE FROM sql_fee_order_store_keiri WHERE nyu_date = %s;"
        cur = sql_con.cursor()
        cur.execute(sql, (nyu_date_int,))
        sql_con.commit()
    return


# create
def mz_sql_fee_order_store(nyu_date_int):
    sql = f"""
        SELECT
        knp.nyu_nendo,
        fee.nyu_date,
        fee.kind_cd,
        fee.cat_cd,
        fee.coltd_cd,
        os.siki_date,
        os.manki_date,
        os.kind_cd_main,
        os.kind_cd_sub,
        os.pay_num_cd,
        os.hoken_kikan_cd,
        os.hoken_kikan_year,
        fee.syoken_cd_main,
        fee.syoken_cd_sub,
        os.hoken_ryo,
        fee.fee_num,
        os.section_cd,
        os.staff1_cd,
        os.staff2_cd,
        os.staff3_cd,
        os.gyotei1_cd,
        os.gyotei2_cd,
        os.gyotei3_cd,
        stf1.staff_email AS staff1_email,
        stf2.staff_email AS staff2_email,
        stf3.staff_email AS staff3_email,
        os.fee_staff1,
        os.fee_staff2,
        os.fee_staff3,
        os.fee_gyotei1,
        os.fee_gyotei2,
        os.fee_gyotei3,
        os.kei_name,
        gyo1.pay_kikan AS pay_kikan1,
        gyo2.pay_kikan AS pay_kikan2,
        gyo3.pay_kikan AS pay_kikan3,
        fee.kaime,
        os.fee_memo,
        stf1.section_cd_email AS section_cd_email1,
        stf2.section_cd_email AS section_cd_email2,
        stf3.section_cd_email AS section_cd_email3,
        fee.first_next_year

        FROM
        (
        SELECT
        min(nyu_date) AS nyu_date,
        min(kind_cd) AS kind_cd,
        min(cat_cd) AS cat_cd,
        min(coltd_cd) AS coltd_cd,
        min(syoken_cd_main) AS syoken_cd_main,
        min(syoken_cd_sub) AS syoken_cd_sub,
        max(kaime) AS kaime,
        min(first_next_year) AS first_next_year,
        sum(fee_notax) AS fee_num

        FROM
        (
        SELECT * FROM sql_fee_store
        WHERE nyu_date = {nyu_date_int} AND kind_cd = 1
        ORDER BY cat_cd, coltd_cd, syoken_cd_main, syoken_cd_sub, kind_cd) AS sfs

        GROUP BY
        sfs.nyu_date, sfs.kind_cd, sfs.coltd_cd, sfs.syoken_cd_main, sfs.syoken_cd_sub

        ORDER BY
        cat_cd, coltd_cd, syoken_cd_main, syoken_cd_sub
        )
        AS fee

        LEFT JOIN
        (
        SELECT
        min(coltd_cd) AS coltd_cd,
        min(siki_date) AS siki_date,
        min(manki_date) AS manki_date,
        min(kind_cd_main) AS kind_cd_main,
        min(kind_cd_sub) AS kind_cd_sub,
        min(pay_num_cd) AS pay_num_cd,
        min(hoken_kikan_cd) AS hoken_kikan_cd,
        min(hoken_kikan_year) AS hoken_kikan_year,
        min(syoken_cd_main) AS syoken_cd_main,
        min(syoken_cd_sub) AS syoken_cd_sub,
        min(hoken_ryo) AS hoken_ryo,
        min(section_cd) AS section_cd,
        min(staff1_cd) AS staff1_cd,
        min(staff2_cd) AS staff2_cd,
        min(staff3_cd) AS staff3_cd,
        min(gyotei1_cd) AS gyotei1_cd,
        min(gyotei2_cd) AS gyotei2_cd,
        min(gyotei3_cd) AS gyotei3_cd,
        min(fee_staff1) AS fee_staff1,
        min(fee_staff2) AS fee_staff2,
        min(fee_staff3) AS fee_staff3,
        min(fee_gyotei1) AS fee_gyotei1,
        min(fee_gyotei2) AS fee_gyotei2,
        min(fee_gyotei3) AS fee_gyotei3,
        min(kei_name) AS kei_name,
        min(fee_memo) AS fee_memo

        FROM
        sql_order_store AS sos

        GROUP BY
        sos.coltd_cd, sos.syoken_cd_main, sos.syoken_cd_sub
        ) AS os
        ON fee.syoken_cd_main = os.syoken_cd_main
        AND fee.syoken_cd_sub = os.syoken_cd_sub
        AND fee.coltd_cd = os.coltd_cd

        LEFT JOIN sql_kei_nyu_pay AS knp ON fee.nyu_date = knp.nyu_year_month_int
        LEFT JOIN sql_staff AS stf1 ON os.staff1_cd = stf1.staff_cd
        LEFT JOIN sql_staff AS stf2 ON os.staff2_cd = stf2.staff_cd
        LEFT JOIN sql_staff AS stf3 ON os.staff3_cd = stf3.staff_cd
        LEFT JOIN sql_gyotei AS gyo1 ON os.gyotei1_cd = gyo1.gyotei_cd
        LEFT JOIN sql_gyotei AS gyo2 ON os.gyotei2_cd = gyo2.gyotei_cd
        LEFT JOIN sql_gyotei AS gyo3 ON os.gyotei3_cd = gyo3.gyotei_cd
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data
