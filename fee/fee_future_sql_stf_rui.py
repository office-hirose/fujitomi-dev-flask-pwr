# 累計
from _mod import sql_config


# 累計・担当
def mz_rui_tan(nyu_nendo, cat_cd, section_cd):
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
            + " sql_fee_future"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
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
            + " sql_fee_future"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
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


# 累計・提携
def mz_rui_gyo(nyu_nendo, cat_cd, section_cd):
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
            + " sql_fee_future"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
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
            + " sql_fee_future"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
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


# 累計・総合計
def mz_rui_total(nyu_nendo, section_cd):
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
