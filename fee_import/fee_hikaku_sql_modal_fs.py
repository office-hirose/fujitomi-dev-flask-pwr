from _mod import sql_config


# -------------------------------------------
# fsデータ
# -------------------------------------------
def mz_fs(nyu_date_int, coltd_cd):
    # fs/手数料税込/手数料税抜/手数料消費税額
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
            kind_cd = 1 AND
            fee_tax_per != 0 AND
            syoken_cd_main != 'balance';
    """
    sql_data = sql_config.mz_sql(sql)

    for dt in sql_data:
        # Noneの場合には0を代入する
        fs_fee_withtax = dt["fee_withtax"] if dt["fee_withtax"] is not None else 0
        fs_fee_notax = dt["fee_notax"] if dt["fee_notax"] is not None else 0
        fs_fee_tax_num = dt["fee_tax_num"] if dt["fee_tax_num"] is not None else 0

    # 以降、fs_fee_withtax、fs_fee_notax、fs_fee_tax_numを使用する

    # fs/振替課税税込/振替課税税抜/振替課税消費税額
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
            syoken_cd_main != 'balance';
    """
    sql_data = sql_config.mz_sql(sql)

    for dt in sql_data:
        # Noneの場合には0を代入する
        fs_furi_kazei_withtax = dt["fee_withtax"] if dt["fee_withtax"] is not None else 0
        fs_furi_kazei_notax = dt["fee_notax"] if dt["fee_notax"] is not None else 0
        fs_furi_kazei_tax_num = dt["fee_tax_num"] if dt["fee_tax_num"] is not None else 0

    # fs/振替非課税税込/振替非課税税抜/振替非課税消費税額
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
            syoken_cd_main != 'balance';
    """
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        # Noneの場合には0を代入する
        fs_furi_hikazei_withtax = dt["fee_withtax"] if dt["fee_withtax"] is not None else 0
        fs_furi_hikazei_notax = dt["fee_notax"] if dt["fee_notax"] is not None else 0
        fs_furi_hikazei_tax_num = dt["fee_tax_num"] if dt["fee_tax_num"] is not None else 0

    # fs/dic
    fs_data = {
        "fee_withtax": fs_fee_withtax,
        "fee_notax": fs_fee_notax,
        "fee_tax_num": fs_fee_tax_num,
        #
        "furi_kazei_withtax": fs_furi_kazei_withtax,
        "furi_kazei_notax": fs_furi_kazei_notax,
        "furi_kazei_tax_num": fs_furi_kazei_tax_num,
        #
        "furi_hikazei_withtax": fs_furi_hikazei_withtax,
        "furi_hikazei_notax": fs_furi_hikazei_notax,
        "furi_hikazei_tax_num": fs_furi_hikazei_tax_num,
        # 税込合計
        "fee_withtax_total": fs_fee_withtax + fs_furi_kazei_withtax + fs_furi_hikazei_withtax,
        # 税別合計
        "fee_notax_total": fs_fee_notax + fs_furi_kazei_notax + fs_furi_hikazei_notax,
        # 消費税額合計
        "fee_tax_num_total": fs_fee_tax_num + fs_furi_kazei_tax_num + fs_furi_hikazei_tax_num,
    }
    return fs_data
