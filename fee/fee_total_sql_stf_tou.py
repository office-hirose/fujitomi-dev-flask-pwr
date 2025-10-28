# 当月
from _mod import sql_config


# 当月・担当
def mz_tou_tan(nyu_date, cat_cd, section_cd):
    if cat_cd != "all":
        sql = (
            "SELECT"
            + " stf.staff_cd AS staff_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_staff AS stf"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " pay_person_cd,"
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
            + " section_cd = "
            + '"'
            + str(section_cd)
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
            + " pay_person_cd"
            + " ) AS fee"
            + " ON stf.staff_cd = fee.pay_person_cd"
            + " WHERE"
            + " stf.sales_cd = "
            + '"on"'
            + " AND"
            + " stf.section_cd = "
            + '"'
            + str(section_cd)
            + '"'
            + " ORDER BY"
            + " stf.sort"
            + ";"
        )
    if cat_cd == "all":
        sql = (
            "SELECT"
            + " stf.staff_cd AS staff_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_staff AS stf"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " pay_person_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_date = "
            + str(nyu_date)
            + " AND"
            + " section_cd = "
            + '"'
            + str(section_cd)
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
            + " pay_person_cd"
            + " ) AS fee"
            + " ON stf.staff_cd = fee.pay_person_cd"
            + " WHERE"
            + " stf.sales_cd = "
            + '"on"'
            + " AND"
            + " stf.section_cd = "
            + '"'
            + str(section_cd)
            + '"'
            + " ORDER BY"
            + " stf.sort"
            + ";"
        )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 当月・提携
def mz_tou_gyo(nyu_date, cat_cd, section_cd):
    if cat_cd != "all":
        sql = (
            "SELECT"
            + " stf.staff_cd AS staff_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_staff AS stf"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " pay_person_cd,"
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
            + " section_cd = "
            + '"'
            + str(section_cd)
            + '"'
            + " AND"
            + " pay_person_kind like "
            + '"'
            + "%"
            + "gyotei"
            + "%"
            + '"'
            + " GROUP BY"
            + " pay_person_cd"
            + " ) AS fee"
            + " ON stf.staff_cd = fee.pay_person_cd"
            + " WHERE"
            + " stf.sales_cd = "
            + '"on"'
            + " AND"
            + " stf.section_cd = "
            + '"'
            + str(section_cd)
            + '"'
            + " ORDER BY"
            + " stf.sort"
            + ";"
        )
    if cat_cd == "all":
        sql = (
            "SELECT"
            + " stf.staff_cd AS staff_cd,"
            + " fee.pay_fee_yen AS pay_fee_yen"
            + " FROM"
            + " sql_staff AS stf"
            + " LEFT JOIN"
            + " ("
            + " SELECT"
            + " pay_person_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_date = "
            + str(nyu_date)
            + " AND"
            + " section_cd = "
            + '"'
            + str(section_cd)
            + '"'
            + " AND"
            + " pay_person_kind like "
            + '"'
            + "%"
            + "gyotei"
            + "%"
            + '"'
            + " GROUP BY"
            + " pay_person_cd"
            + " ) AS fee"
            + " ON stf.staff_cd = fee.pay_person_cd"
            + " WHERE"
            + " stf.sales_cd = "
            + '"on"'
            + " AND"
            + " stf.section_cd = "
            + '"'
            + str(section_cd)
            + '"'
            + " ORDER BY"
            + " stf.sort"
            + ";"
        )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 当月・総合計
def mz_tou_total(nyu_date, section_cd):
    sql = (
        "SELECT"
        + " stf.staff_cd AS staff_cd,"
        + " fee.pay_fee_yen AS pay_fee_yen"
        + " FROM"
        + " sql_staff AS stf"
        + " LEFT JOIN"
        + " ("
        + " SELECT"
        + " pay_person_cd,"
        + " SUM(pay_fee_yen) AS pay_fee_yen"
        + " FROM"
        + " sql_fee_order_store"
        + " WHERE"
        + " nyu_date = "
        + str(nyu_date)
        + " AND"
        + " section_cd = "
        + '"'
        + str(section_cd)
        + '"'
        + " GROUP BY"
        + " pay_person_cd"
        + " ) AS fee"
        + " ON stf.staff_cd = fee.pay_person_cd"
        + " WHERE"
        + " stf.sales_cd = "
        + '"on"'
        + " AND"
        + " stf.section_cd = "
        + '"'
        + str(section_cd)
        + '"'
        + " ORDER BY"
        + " stf.sort"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data
