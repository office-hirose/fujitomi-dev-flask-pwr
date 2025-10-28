# ---------------------------------------------------
# 当月
# ---------------------------------------------------
from _mod import sql_config


# L2.当月・件数
def mz_sql_fee_tou_kensu(fdate_int, cat_cd, staff_email):
    sql = (
        "SELECT"
        + " col.coltd_cd AS coltd_cd,"
        + " col.name_simple AS coltd_name,"
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
        + " nyu_date = "
        + str(fdate_int)
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


# L3.当月・手数料・主担当
def mz_sql_fee_tou_fee_main(fdate_int, cat_cd, staff_email):
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
        + str(fdate_int)
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


# L4.当月・手数料・副担当
def mz_sql_fee_tou_fee_sub(fdate_int, cat_cd, staff_email):
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
        + str(fdate_int)
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


# L5.当月・手数料・担当合計
def mz_sql_fee_tou_fee_main_sub(fdate_int, cat_cd, staff_email):
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
        + " nyu_date = "
        + str(fdate_int)
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
        + " nyu_date = "
        + str(fdate_int)
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


# L6.当月・手数料・提携
def mz_sql_fee_tou_fee_gyo(fdate_int, cat_cd, staff_email):
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
        + str(fdate_int)
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


# L7.当月・手数料・総合計
def mz_sql_fee_tou_fee_total(fdate_int, cat_cd, staff_email):
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
        + str(fdate_int)
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
