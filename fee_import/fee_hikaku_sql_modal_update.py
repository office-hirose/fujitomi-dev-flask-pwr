from _mod import sql_config


# 入金確定金額/更新
def mz_update(nyu_date_int, coltd_cd, fk_data_form, bal_data_form):
    fk_fee_tax_per = int(fk_data_form["fee_tax_per"])

    fk_fee_notax = int(fk_data_form["fee_notax"])
    fk_fee_tax_num = int(fk_fee_notax * (fk_fee_tax_per / 100))
    fk_fee_withtax = fk_fee_notax + fk_fee_tax_num

    fk_furi_kazei_notax = int(fk_data_form["furi_kazei_notax"])
    fk_furi_kazei_tax_num = int(fk_furi_kazei_notax * (fk_fee_tax_per / 100))
    fk_furi_kazei_withtax = fk_furi_kazei_notax + fk_furi_kazei_tax_num

    fk_furi_hikazei_notax = int(fk_data_form["furi_hikazei_notax"])
    fk_furi_hikazei_tax_num = 0
    fk_furi_hikazei_withtax = fk_furi_hikazei_notax + fk_furi_hikazei_tax_num

    fk_fee_notax_total = fk_fee_notax + fk_furi_kazei_notax + fk_furi_hikazei_notax
    fk_fee_tax_num_total = fk_fee_tax_num + fk_furi_kazei_tax_num + fk_furi_hikazei_tax_num
    fk_fee_withtax_total = fk_fee_withtax + fk_furi_kazei_withtax + fk_furi_hikazei_withtax

    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = """
        UPDATE
            sql_fee_kakutei
        SET
            fee_withtax = %s,
            fee_notax = %s,
            fee_tax_num = %s,

            furi_kazei_withtax = %s,
            furi_kazei_notax = %s,
            furi_kazei_tax_num = %s,

            furi_hikazei_withtax = %s,
            furi_hikazei_notax = %s,
            furi_hikazei_tax_num = %s,

            fee_withtax_total = %s,
            fee_notax_total = %s,
            fee_tax_num_total = %s
        WHERE
            nyu_date = %s AND
            coltd_cd = %s;
        """
        cur = sql_con.cursor()
        cur.execute(
            sql,
            (
                fk_fee_withtax,
                fk_fee_notax,
                fk_fee_tax_num,
                fk_furi_kazei_withtax,
                fk_furi_kazei_notax,
                fk_furi_kazei_tax_num,
                fk_furi_hikazei_withtax,
                fk_furi_hikazei_notax,
                fk_furi_hikazei_tax_num,
                fk_fee_withtax_total,
                fk_fee_notax_total,
                fk_fee_tax_num_total,
                nyu_date_int,
                coltd_cd,
            ),
        )
        sql_con.commit()

    # fs手数料 update, balance
    temp_fee_notax = int(bal_data_form["fee_notax"])
    temp_fee_tax_num = int(temp_fee_notax * (fk_fee_tax_per / 100))
    temp_fee_withtax = temp_fee_notax + temp_fee_tax_num

    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = """
            UPDATE
                sql_fee_store
            SET
                fee_withtax = %s,
                fee_notax = %s,
                fee_tax_num = %s
            WHERE
                nyu_date = %s AND
                coltd_cd = %s AND
                kind_cd = %s AND
                fee_tax_per != %s AND
                syoken_cd_main = %s;
        """
        cur = sql_con.cursor()
        cur.execute(
            sql,
            (
                temp_fee_withtax,
                temp_fee_notax,
                temp_fee_tax_num,
                nyu_date_int,
                coltd_cd,
                1,
                0,
                "balance",
            ),
        )
        sql_con.commit()

    # fs課税振替 update, balance
    temp_fee_notax = int(bal_data_form["furi_kazei_notax"])
    temp_fee_tax_num = int(temp_fee_notax * (fk_fee_tax_per / 100))
    temp_fee_withtax = temp_fee_notax + temp_fee_tax_num

    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = """
            UPDATE
                sql_fee_store
            SET
                fee_withtax = %s,
                fee_notax = %s,
                fee_tax_num = %s
            WHERE
                nyu_date = %s AND
                coltd_cd = %s AND
                kind_cd = %s AND
                fee_tax_per != %s AND
                syoken_cd_main = %s;
        """
        cur = sql_con.cursor()
        cur.execute(
            sql,
            (
                temp_fee_withtax,
                temp_fee_notax,
                temp_fee_tax_num,
                nyu_date_int,
                coltd_cd,
                2,
                0,
                "balance",
            ),
        )
        sql_con.commit()

    # fs非課税振替 update, balance
    temp_fee_notax = int(bal_data_form["furi_hikazei_notax"])
    temp_fee_tax_num = 0
    temp_fee_withtax = temp_fee_notax + temp_fee_tax_num

    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = """
            UPDATE
                sql_fee_store
            SET
                fee_withtax = %s,
                fee_notax = %s,
                fee_tax_num = %s
            WHERE
                nyu_date = %s AND
                coltd_cd = %s AND
                kind_cd = %s AND
                fee_tax_per = %s AND
                syoken_cd_main = %s;
        """
        cur = sql_con.cursor()
        cur.execute(
            sql,
            (
                temp_fee_withtax,
                temp_fee_notax,
                temp_fee_tax_num,
                nyu_date_int,
                coltd_cd,
                2,
                0,
                "balance",
            ),
        )
        sql_con.commit()
    return
