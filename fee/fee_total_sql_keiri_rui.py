from _mod import sql_config


# 累計 L8.L9.L10.L11.L12
def mz_sql_fee_rui_list(nyu_date, nyu_nendo, cat_cd, section_cd):
    if section_cd != "all":
        sql = (
            "SELECT"
            + " col.coltd_cd AS coltd_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_coltd AS col"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " coltd_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store_keiri"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
            + " AND"
            + " nyu_date <= "
            + str(nyu_date)
            + " AND"
            + " section_cd_email = "
            + '"'
            + str(section_cd)
            + '"'
            + " GROUP BY"
            + " coltd_cd"
            + " ) AS fee"
            + " ON col.coltd_cd = fee.coltd_cd"
            + " WHERE"
            + " col.onoff_cd = "
            + '"on"'
            + " AND"
            + " col.cat_cd = "
            + '"'
            + str(cat_cd)
            + '"'
            + " ORDER BY"
            + " col.coltd_cd"
            + ";"
        )
    if section_cd == "all":
        sql = (
            "SELECT"
            + " col.coltd_cd AS coltd_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_coltd AS col"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " coltd_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store_keiri"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
            + " AND"
            + " nyu_date <= "
            + str(nyu_date)
            + " GROUP BY"
            + " coltd_cd"
            + " ) AS fee"
            + " ON col.coltd_cd = fee.coltd_cd"
            + " WHERE"
            + " col.onoff_cd = "
            + '"on"'
            + " AND"
            + " col.cat_cd = "
            + '"'
            + str(cat_cd)
            + '"'
            + " ORDER BY"
            + " col.coltd_cd"
            + ";"
        )
    sql_data = sql_config.mz_sql(sql)
    return sql_data
