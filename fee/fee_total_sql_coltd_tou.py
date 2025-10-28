from _mod import sql_config


# 当月 L2.L3.L4.L5.L6
def mz_sql_fee_tou_list(nyu_date, cat_cd, section_cd):
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
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_date = "
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
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_date = "
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
