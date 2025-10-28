from _mod import sql_config


# -------------------------------------------
# fk確定金額
# -------------------------------------------
def mz_fk(nyu_date_int, coltd_cd):
    sql = f"""
        SELECT *
        FROM
            sql_fee_kakutei
        WHERE
            nyu_date = {nyu_date_int} AND
            coltd_cd = '{coltd_cd}';
    """
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        fk_fee_tax_per = int(dt["fee_tax_per"])

        fk_fee_withtax = int(dt["fee_withtax"])
        fk_fee_notax = int(dt["fee_notax"])
        fk_fee_tax_num = int(dt["fee_tax_num"])

        fk_furi_kazei_withtax = int(dt["furi_kazei_withtax"])
        fk_furi_kazei_notax = int(dt["furi_kazei_notax"])
        fk_furi_kazei_tax_num = int(dt["furi_kazei_tax_num"])

        fk_furi_hikazei_withtax = int(dt["furi_hikazei_withtax"])
        fk_furi_hikazei_notax = int(dt["furi_hikazei_notax"])
        fk_furi_hikazei_tax_num = int(dt["furi_hikazei_tax_num"])

        fk_fee_withtax_total = int(dt["fee_withtax_total"])
        fk_fee_notax_total = int(dt["fee_notax_total"])
        fk_fee_tax_num_total = int(dt["fee_tax_num_total"])

    # fk/dic
    fk_data = {
        "fee_tax_per": fk_fee_tax_per,
        #
        "fee_withtax": fk_fee_withtax,
        "fee_notax": fk_fee_notax,
        "fee_tax_num": fk_fee_tax_num,
        #
        "furi_kazei_withtax": fk_furi_kazei_withtax,
        "furi_kazei_notax": fk_furi_kazei_notax,
        "furi_kazei_tax_num": fk_furi_kazei_tax_num,
        #
        "furi_hikazei_withtax": fk_furi_hikazei_withtax,
        "furi_hikazei_notax": fk_furi_hikazei_notax,
        "furi_hikazei_tax_num": fk_furi_hikazei_tax_num,
        #
        "fee_withtax_total": fk_fee_withtax_total,
        "fee_notax_total": fk_fee_notax_total,
        "fee_tax_num_total": fk_fee_tax_num_total,
    }
    return fk_data
