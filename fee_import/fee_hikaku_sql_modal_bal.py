from _mod import sql_config


# -------------------------------------------
# balanceデータ
# -------------------------------------------
def mz_bal(nyu_date_int, coltd_cd):
    # bal/手数料税込/手数料税抜/手数料消費税額
    sql = f"""
        SELECT *
        FROM
            sql_fee_store
        WHERE
            nyu_date = {nyu_date_int} AND
            coltd_cd = '{coltd_cd}' AND
            kind_cd = 1 AND
            fee_tax_per != 0 AND
            syoken_cd_main = 'balance';
    """
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        bal_fee_withtax = int(dt["fee_withtax"])
        bal_fee_notax = int(dt["fee_notax"])
        bal_fee_tax_num = int(dt["fee_tax_num"])

    # bal/振替課税税込/振替課税税抜/振替課税消費税額
    sql = f"""
        SELECT
            sum(fee_withtax) AS fee_withtax,
            sum(fee_notax) AS fee_notax,
            sum(fee_tax_num) AS fee_tax_num
        FROM
            sql_fee_store
        WHERE
            nyu_date = {nyu_date_int} AND
            coltd_cd = '{coltd_cd}' AND
            kind_cd = 2 AND
            fee_tax_per != 0 AND
            syoken_cd_main = 'balance';
    """
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        bal_furi_kazei_withtax = int(dt["fee_withtax"])
        bal_furi_kazei_notax = int(dt["fee_notax"])
        bal_furi_kazei_tax_num = int(dt["fee_tax_num"])

    # bal/振替非課税税込/振替非課税税抜/振替非課税消費税額
    sql = f"""
        SELECT
            sum(fee_withtax) AS fee_withtax,
            sum(fee_notax) AS fee_notax,
            sum(fee_tax_num) AS fee_tax_num
        FROM
            sql_fee_store
        WHERE
            nyu_date = {nyu_date_int} AND
            coltd_cd = '{coltd_cd}' AND
            kind_cd = 2 AND
            fee_tax_per = 0 AND
            syoken_cd_main = 'balance';
    """
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        bal_furi_hikazei_withtax = int(dt["fee_withtax"])
        bal_furi_hikazei_notax = int(dt["fee_notax"])
        bal_furi_hikazei_tax_num = int(dt["fee_tax_num"])

    # bal/dic
    bal_data = {
        "fee_withtax": bal_fee_withtax,
        "fee_notax": bal_fee_notax,
        "fee_tax_num": bal_fee_tax_num,
        "furi_kazei_withtax": bal_furi_kazei_withtax,
        "furi_kazei_notax": bal_furi_kazei_notax,
        "furi_kazei_tax_num": bal_furi_kazei_tax_num,
        "furi_hikazei_withtax": bal_furi_hikazei_withtax,
        "furi_hikazei_notax": bal_furi_hikazei_notax,
        "furi_hikazei_tax_num": bal_furi_hikazei_tax_num,
        # 税込合計
        "fee_withtax_total": bal_fee_withtax + bal_furi_kazei_withtax + bal_furi_hikazei_withtax,
        # 税別合計
        "fee_notax_total": bal_fee_notax + bal_furi_kazei_notax + bal_furi_hikazei_notax,
        # 消費税額合計
        "fee_tax_num_total": bal_fee_tax_num + bal_furi_kazei_tax_num + bal_furi_hikazei_tax_num,
    }
    return bal_data
