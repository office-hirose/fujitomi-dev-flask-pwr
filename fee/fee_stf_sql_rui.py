# ---------------------------------------------------
# 累計
# ---------------------------------------------------
from _mod import sql_config


# L9.累計・件数
def mz_sql_fee_rui_kensu(nyu_nendo, cat_cd, staff_email):
    sql = (
        "SELECT"
        + " col.coltd_cd AS coltd_cd,"
        + " fee.kensu AS kensu"
        + " FROM"
        + " sql_coltd AS col"
        + " LEFT JOIN"
        + " ("
        + " SELECT"
        + " coltd_cd,"
        + " COUNT(*) AS kensu"
        + " FROM"
        + " sql_fee_order_store"
        + " WHERE"
        + " nyu_nendo = "
        + str(nyu_nendo)
        + " AND"
        + " pay_person_kind = "
        + '"main"'
        + " AND"
        + " pay_person_email = "
        + '"'
        + str(staff_email)
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
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# L10.累計・手数料・主担当
def mz_sql_fee_rui_fee_main(nyu_nendo, cat_cd, staff_email):
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
        + " nyu_nendo = "
        + str(nyu_nendo)
        + " AND"
        + " pay_person_kind = "
        + '"main"'
        + " AND"
        + " pay_person_email = "
        + '"'
        + str(staff_email)
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
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# L11.累計・手数料・副担当
def mz_sql_fee_rui_fee_sub(nyu_nendo, cat_cd, staff_email):
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
        + " nyu_nendo = "
        + str(nyu_nendo)
        + " AND"
        + " pay_person_kind = "
        + '"sub"'
        + " AND"
        + " pay_person_email = "
        + '"'
        + str(staff_email)
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
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# L12.累計・手数料・担当合計
def mz_sql_fee_rui_fee_main_sub(nyu_nendo, cat_cd, staff_email):
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
        + " ("
        + " nyu_nendo = "
        + str(nyu_nendo)
        + " AND"
        + " pay_person_kind = "
        + '"main"'
        + " AND"
        + " pay_person_email = "
        + '"'
        + str(staff_email)
        + '"'
        + " )"
        + " OR"
        + " ("
        + " nyu_nendo = "
        + str(nyu_nendo)
        + " AND"
        + " pay_person_kind = "
        + '"sub"'
        + " AND"
        + " pay_person_email = "
        + '"'
        + str(staff_email)
        + '"'
        + " )"
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


# L13.累計・手数料・提携
def mz_sql_fee_rui_fee_gyo(nyu_nendo, cat_cd, staff_email):
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
        + " nyu_nendo = "
        + str(nyu_nendo)
        + " AND"
        + " pay_person_kind like "
        + '"'
        + "%"
        + "gyotei"
        + "%"
        + '"'
        + " AND"
        + " pay_person_email = "
        + '"'
        + str(staff_email)
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
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# L14.累計・手数料・総合計
def mz_sql_fee_rui_fee_total(nyu_nendo, cat_cd, staff_email):
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
        + " nyu_nendo = "
        + str(nyu_nendo)
        + " AND"
        + " pay_person_email = "
        + '"'
        + str(staff_email)
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
    sql_data = sql_config.mz_sql(sql)
    return sql_data
