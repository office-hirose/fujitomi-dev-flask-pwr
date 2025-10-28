# 総合計
from _mod import sql_config


# 当月・担当
def mz_tou_tan(nyu_date, cat_cd):
    if cat_cd != "all":
        sql = (
            "SELECT"
            + " sec.section_cd AS section_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_section AS sec"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " section_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_date = "
            + str(nyu_date)
            + " AND"
            + " cat_cd = "
            + '"'
            + str(cat_cd)
            + '"'
            + " AND"
            + " (pay_person_kind = "
            + '"'
            + "main"
            + '"'
            + " OR pay_person_kind = "
            + '"'
            + "sub"
            + '"'
            + ")"
            + " GROUP BY"
            + " section_cd"
            + " ) AS fee"
            + " ON sec.section_cd = fee.section_cd"
            + " WHERE"
            + " sec.onoff_cd = "
            + '"on"'
            + " ORDER BY"
            + " sec.sort"
            + ";"
        )
    if cat_cd == "all":
        sql = (
            "SELECT"
            + " sec.section_cd AS section_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_section AS sec"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " section_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_date = "
            + str(nyu_date)
            + " AND"
            + " (pay_person_kind = "
            + '"'
            + "main"
            + '"'
            + " OR pay_person_kind = "
            + '"'
            + "sub"
            + '"'
            + ")"
            + " GROUP BY"
            + " section_cd"
            + " ) AS fee"
            + " ON sec.section_cd = fee.section_cd"
            + " WHERE"
            + " sec.onoff_cd = "
            + '"on"'
            + " ORDER BY"
            + " sec.sort"
            + ";"
        )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 当月・提携
def mz_tou_gyo(nyu_date, cat_cd):
    if cat_cd != "all":
        sql = (
            "SELECT"
            + " sec.section_cd AS section_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_section AS sec"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " section_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_date = "
            + str(nyu_date)
            + " AND"
            + " cat_cd = "
            + '"'
            + str(cat_cd)
            + '"'
            + " AND"
            + " pay_person_kind like "
            + '"'
            + "%"
            + "gyotei"
            + "%"
            + '"'
            + " GROUP BY"
            + " section_cd"
            + " ) AS fee"
            + " ON sec.section_cd = fee.section_cd"
            + " WHERE"
            + " sec.onoff_cd = "
            + '"on"'
            + " ORDER BY"
            + " sec.sort"
            + ";"
        )
    if cat_cd == "all":
        sql = (
            "SELECT"
            + " sec.section_cd AS section_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_section AS sec"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " section_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_date = "
            + str(nyu_date)
            + " AND"
            + " pay_person_kind like "
            + '"'
            + "%"
            + "gyotei"
            + "%"
            + '"'
            + " GROUP BY"
            + " section_cd"
            + " ) AS fee"
            + " ON sec.section_cd = fee.section_cd"
            + " WHERE"
            + " sec.onoff_cd = "
            + '"on"'
            + " ORDER BY"
            + " sec.sort"
            + ";"
        )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 当月・総合計
def mz_tou_total(nyu_date):
    sql = (
        "SELECT"
        + " sec.section_cd AS section_cd,"
        + " fee.pay_fee_yen AS pay_fee_yen"
        + " FROM"
        + " sql_section AS sec"
        + " LEFT JOIN"
        + " ("
        + " SELECT"
        + " section_cd,"
        + " SUM(pay_fee_yen) AS pay_fee_yen"
        + " FROM"
        + " sql_fee_order_store"
        + " WHERE"
        + " nyu_date = "
        + str(nyu_date)
        + " GROUP BY"
        + " section_cd"
        + " ) AS fee"
        + " ON sec.section_cd = fee.section_cd"
        + " WHERE"
        + " sec.onoff_cd = "
        + '"on"'
        + " ORDER BY"
        + " sec.sort"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# -------------------------------------------------------


# 累計・担当
def mz_rui_tan(nyu_date, nyu_nendo, cat_cd):
    if cat_cd != "all":
        sql = (
            "SELECT"
            + " sec.section_cd AS section_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_section AS sec"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " section_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
            + " AND"
            + " nyu_date <= "
            + str(nyu_date)
            + " AND"
            + " cat_cd = "
            + '"'
            + str(cat_cd)
            + '"'
            + " AND"
            + " (pay_person_kind = "
            + '"'
            + "main"
            + '"'
            + " OR pay_person_kind = "
            + '"'
            + "sub"
            + '"'
            + ")"
            + " GROUP BY"
            + " section_cd"
            + " ) AS fee"
            + " ON sec.section_cd = fee.section_cd"
            + " WHERE"
            + " sec.onoff_cd = "
            + '"on"'
            + " ORDER BY"
            + " sec.sort"
            + ";"
        )
    if cat_cd == "all":
        sql = (
            "SELECT"
            + " sec.section_cd AS section_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_section AS sec"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " section_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
            + " AND"
            + " nyu_date <= "
            + str(nyu_date)
            + " AND"
            + " (pay_person_kind = "
            + '"'
            + "main"
            + '"'
            + " OR pay_person_kind = "
            + '"'
            + "sub"
            + '"'
            + ")"
            + " GROUP BY"
            + " section_cd"
            + " ) AS fee"
            + " ON sec.section_cd = fee.section_cd"
            + " WHERE"
            + " sec.onoff_cd = "
            + '"on"'
            + " ORDER BY"
            + " sec.sort"
            + ";"
        )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 累計・提携
def mz_rui_gyo(nyu_date, nyu_nendo, cat_cd):
    if cat_cd != "all":
        sql = (
            "SELECT"
            + " sec.section_cd AS section_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_section AS sec"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " section_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
            + " AND"
            + " nyu_date <= "
            + str(nyu_date)
            + " AND"
            + " cat_cd = "
            + '"'
            + str(cat_cd)
            + '"'
            + " AND"
            + " pay_person_kind like "
            + '"'
            + "%"
            + "gyotei"
            + "%"
            + '"'
            + " GROUP BY"
            + " section_cd"
            + " ) AS fee"
            + " ON sec.section_cd = fee.section_cd"
            + " WHERE"
            + " sec.onoff_cd = "
            + '"on"'
            + " ORDER BY"
            + " sec.sort"
            + ";"
        )
    if cat_cd == "all":
        sql = (
            "SELECT"
            + " sec.section_cd AS section_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_section AS sec"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " section_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
            + " AND"
            + " nyu_date <= "
            + str(nyu_date)
            + " AND"
            + " pay_person_kind like "
            + '"'
            + "%"
            + "gyotei"
            + "%"
            + '"'
            + " GROUP BY"
            + " section_cd"
            + " ) AS fee"
            + " ON sec.section_cd = fee.section_cd"
            + " WHERE"
            + " sec.onoff_cd = "
            + '"on"'
            + " ORDER BY"
            + " sec.sort"
            + ";"
        )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 累計・総合計
def mz_rui_total(nyu_date, nyu_nendo):
    sql = (
        "SELECT"
        + " sec.section_cd AS section_cd,"
        + " fee.pay_fee_yen AS pay_fee_yen"
        + " FROM"
        + " sql_section AS sec"
        + " LEFT JOIN"
        + " ("
        + " SELECT"
        + " section_cd,"
        + " SUM(pay_fee_yen) AS pay_fee_yen"
        + " FROM"
        + " sql_fee_order_store"
        + " WHERE"
        + " nyu_nendo = "
        + str(nyu_nendo)
        + " AND"
        + " nyu_date <= "
        + str(nyu_date)
        + " GROUP BY"
        + " section_cd"
        + " ) AS fee"
        + " ON sec.section_cd = fee.section_cd"
        + " WHERE"
        + " sec.onoff_cd = "
        + '"on"'
        + " ORDER BY"
        + " sec.sort"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data
