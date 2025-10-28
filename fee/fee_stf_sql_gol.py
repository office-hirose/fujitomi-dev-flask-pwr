# ---------------------------------------------------
# 総合計
# ---------------------------------------------------
from _mod import sql_config


# G2.分野別合計・当月・件数
def mz_sql_fee_tou_kensu_sum(fdate_int, staff_email):
    sql = (
        "SELECT"
        + " cat.cat_cd AS cat_cd,"
        + " cat.cat_name_simple AS cat_name,"
        + " fee.kensu AS kensu"
        + " FROM"
        + " sql_cat AS cat"
        + " LEFT JOIN"
        + " ("
        + " SELECT"
        + " cat_cd,"
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
        + " cat_cd"
        + " ) AS fee"
        + " ON cat.cat_cd = fee.cat_cd"
        + " ORDER BY"
        + " cat.cat_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# G3.分野別合計・当月・手数料・主担当
def mz_sql_fee_tou_fee_main_sum(fdate_int, staff_email):
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
        + " cat_cd"
        + " ) AS fee"
        + " ON cat.cat_cd = fee.cat_cd"
        + " ORDER BY"
        + " cat.cat_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# G4.分野別合計・当月・手数料・副担当
def mz_sql_fee_tou_fee_sub_sum(fdate_int, staff_email):
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
        + " cat_cd"
        + " ) AS fee"
        + " ON cat.cat_cd = fee.cat_cd"
        + " ORDER BY"
        + " cat.cat_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# G5.分野別合計・当月・手数料・担当合計
def mz_sql_fee_tou_fee_main_sub_sum(fdate_int, staff_email):
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
        + " cat_cd"
        + " ) AS fee"
        + " ON cat.cat_cd = fee.cat_cd"
        + " ORDER BY"
        + " cat.cat_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# G6.分野別合計・当月・手数料・提携
def mz_sql_fee_tou_fee_gyo_sum(fdate_int, staff_email):
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
        + " cat_cd"
        + " ) AS fee"
        + " ON cat.cat_cd = fee.cat_cd"
        + " ORDER BY"
        + " cat.cat_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# G7.分野別合計・当月・手数料・総合計
def mz_sql_fee_tou_fee_total_sum(fdate_int, staff_email):
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
        + " cat_cd"
        + " ) AS fee"
        + " ON cat.cat_cd = fee.cat_cd"
        + " ORDER BY"
        + " cat.cat_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# G9.分野別合計・累計・件数
def mz_sql_fee_rui_kensu_sum(nyu_nendo, staff_email):
    sql = (
        "SELECT"
        + " cat.cat_cd AS cat_cd,"
        + " cat.cat_name_simple AS cat_name,"
        + " fee.kensu AS kensu"
        + " FROM"
        + " sql_cat AS cat"
        + " LEFT JOIN"
        + " ("
        + " SELECT"
        + " cat_cd,"
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
        + " cat_cd"
        + " ) AS fee"
        + " ON cat.cat_cd = fee.cat_cd"
        + " ORDER BY"
        + " cat.cat_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# G10.分野別合計・累計・手数料・主担当
def mz_sql_fee_rui_fee_main_sum(nyu_nendo, staff_email):
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
        + " cat_cd"
        + " ) AS fee"
        + " ON cat.cat_cd = fee.cat_cd"
        + " ORDER BY"
        + " cat.cat_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# G11.分野別合計・累計・手数料・副担当
def mz_sql_fee_rui_fee_sub_sum(nyu_nendo, staff_email):
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
        + " cat_cd"
        + " ) AS fee"
        + " ON cat.cat_cd = fee.cat_cd"
        + " ORDER BY"
        + " cat.cat_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# G12.分野別合計・累計・手数料・担当合計
def mz_sql_fee_rui_fee_main_sub_sum(nyu_nendo, staff_email):
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
        + " cat_cd"
        + " ) AS fee"
        + " ON cat.cat_cd = fee.cat_cd"
        + " ORDER BY"
        + " cat.cat_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# G13.分野別合計・累計・手数料・提携
def mz_sql_fee_rui_fee_gyo_sum(nyu_nendo, staff_email):
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
        + " cat_cd"
        + " ) AS fee"
        + " ON cat.cat_cd = fee.cat_cd"
        + " ORDER BY"
        + " cat.cat_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# G14.分野別合計・累計・手数料・総合計
def mz_sql_fee_rui_fee_total_sum(nyu_nendo, staff_email):
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
        + " cat_cd"
        + " ) AS fee"
        + " ON cat.cat_cd = fee.cat_cd"
        + " ORDER BY"
        + " cat.cat_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data
