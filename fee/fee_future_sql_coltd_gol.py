from _mod import sql_config


# 総合計 当月 G2.G3.G4.G5
def mz_sql_fee_tou_sum(nyu_date, section_cd):
    if section_cd != "all":
        sql = (
            "SELECT"
            + " cat.cat_cd AS cat_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_cat AS cat"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " cat_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_future"
            + " WHERE"
            + " nyu_date = "
            + str(nyu_date)
            + " AND"
            + " section_cd = "
            + '"'
            + str(section_cd)
            + '"'
            + " GROUP BY"
            + " cat_cd"
            + " ) AS fee"
            + " ON cat.cat_cd = fee.cat_cd"
            + " ORDER BY"
            + " cat.cat_cd"
            + ";"
        )
    if section_cd == "all":
        sql = (
            "SELECT"
            + " cat.cat_cd AS cat_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_cat AS cat"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " cat_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_future"
            + " WHERE"
            + " nyu_date = "
            + str(nyu_date)
            + " GROUP BY"
            + " cat_cd"
            + " ) AS fee"
            + " ON cat.cat_cd = fee.cat_cd"
            + " ORDER BY"
            + " cat.cat_cd"
            + ";"
        )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 累計 G7.G8.G9.G10
def mz_sql_fee_rui_sum(nyu_nendo, section_cd):
    if section_cd != "all":
        sql = (
            "SELECT"
            + " cat.cat_cd AS cat_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_cat AS cat"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " cat_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_future"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
            + " AND"
            + " section_cd = "
            + '"'
            + str(section_cd)
            + '"'
            + " GROUP BY"
            + " cat_cd"
            + " ) AS fee"
            + " ON cat.cat_cd = fee.cat_cd"
            + " ORDER BY"
            + " cat.cat_cd"
            + ";"
        )
    if section_cd == "all":
        sql = (
            "SELECT"
            + " cat.cat_cd AS cat_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_cat AS cat"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " cat_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_future"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
            + " GROUP BY"
            + " cat_cd"
            + " ) AS fee"
            + " ON cat.cat_cd = fee.cat_cd"
            + " ORDER BY"
            + " cat.cat_cd"
            + ";"
        )
    sql_data = sql_config.mz_sql(sql)
    return sql_data
