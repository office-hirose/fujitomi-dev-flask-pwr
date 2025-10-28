# 累計
from _mod import sql_config


# 累計・担当
def mz_rui_tan(nyu_date, nyu_nendo, cat_cd, section_cd_email):
    if cat_cd != "all":
        sql = (
            "SELECT"
            + " name_simple,"
            + " pay_fee_yen"
            + " FROM ( SELECT * FROM sql_staff WHERE sales_cd = "
            + '"'
            + "on"
            + '"'
            + " AND section_cd = "
            + '"'
            + str(section_cd_email)
            + '"'
            + " AND section_cd_email = "
            + '"'
            + str(section_cd_email)
            + '"'
            + ") AS stf"
            + " LEFT JOIN ("
            + " SELECT"
            + " pay_person_email,"
            + " SUM( pay_fee_yen ) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
            + " AND"
            + " nyu_date <= "
            + str(nyu_date)
            + " AND cat_cd = "
            + '"'
            + str(cat_cd)
            + '"'
            + " AND ( pay_person_kind = "
            + '"'
            + "main"
            + '"'
            + " OR pay_person_kind = "
            + '"'
            + "sub"
            + '"'
            + " )"
            + " GROUP BY"
            + " pay_person_email"
            + " ) AS fee ON stf.staff_email = fee.pay_person_email"
            + " ORDER BY"
            + " stf.sort;"
        )
    if cat_cd == "all":
        sql = (
            "SELECT"
            + " name_simple,"
            + " pay_fee_yen"
            + " FROM ( SELECT * FROM sql_staff WHERE sales_cd = "
            + '"'
            + "on"
            + '"'
            + " AND section_cd = "
            + '"'
            + str(section_cd_email)
            + '"'
            + " AND section_cd_email = "
            + '"'
            + str(section_cd_email)
            + '"'
            + ") AS stf"
            + " LEFT JOIN ("
            + " SELECT"
            + " pay_person_email,"
            + " SUM( pay_fee_yen ) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
            + " AND"
            + " nyu_date <= "
            + str(nyu_date)
            + " AND ( pay_person_kind = "
            + '"'
            + "main"
            + '"'
            + " OR pay_person_kind = "
            + '"'
            + "sub"
            + '"'
            + " )"
            + " GROUP BY"
            + " pay_person_email"
            + " ) AS fee ON stf.staff_email = fee.pay_person_email"
            + " ORDER BY"
            + " stf.sort;"
        )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 累計・提携
def mz_rui_gyo(nyu_date, nyu_nendo, cat_cd, section_cd_email):
    if cat_cd != "all":
        sql = (
            "SELECT"
            + " name_simple,"
            + " pay_fee_yen"
            + " FROM ( SELECT * FROM sql_staff WHERE sales_cd = "
            + '"'
            + "on"
            + '"'
            + " AND section_cd = "
            + '"'
            + str(section_cd_email)
            + '"'
            + " AND section_cd_email = "
            + '"'
            + str(section_cd_email)
            + '"'
            + ") AS stf"
            + " LEFT JOIN ("
            + " SELECT"
            + " pay_person_email,"
            + " SUM( pay_fee_yen ) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
            + " AND"
            + " nyu_date <= "
            + str(nyu_date)
            + " AND cat_cd = "
            + '"'
            + str(cat_cd)
            + '"'
            + " AND pay_person_kind like "
            + '"'
            + "%"
            + "gyotei"
            + "%"
            + '"'
            + " GROUP BY"
            + " pay_person_email"
            + " ) AS fee ON stf.staff_email = fee.pay_person_email"
            + " ORDER BY"
            + " stf.sort;"
        )
    if cat_cd == "all":
        sql = (
            "SELECT"
            + " name_simple,"
            + " pay_fee_yen"
            + " FROM ( SELECT * FROM sql_staff WHERE sales_cd = "
            + '"'
            + "on"
            + '"'
            + " AND section_cd = "
            + '"'
            + str(section_cd_email)
            + '"'
            + " AND section_cd_email = "
            + '"'
            + str(section_cd_email)
            + '"'
            + ") AS stf"
            + " LEFT JOIN ("
            + " SELECT"
            + " pay_person_email,"
            + " SUM( pay_fee_yen ) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " nyu_nendo = "
            + str(nyu_nendo)
            + " AND"
            + " nyu_date <= "
            + str(nyu_date)
            + " AND pay_person_kind like "
            + '"'
            + "%"
            + "gyotei"
            + "%"
            + '"'
            + " GROUP BY"
            + " pay_person_email"
            + " ) AS fee ON stf.staff_email = fee.pay_person_email"
            + " ORDER BY"
            + " stf.sort;"
        )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 累計・総合計
def mz_rui_total(nyu_date, nyu_nendo, section_cd_email):
    sql = (
        "SELECT"
        + " name_simple,"
        + " pay_fee_yen"
        + " FROM ( SELECT * FROM sql_staff WHERE sales_cd = "
        + '"'
        + "on"
        + '"'
        + " AND section_cd = "
        + '"'
        + str(section_cd_email)
        + '"'
        + " AND section_cd_email = "
        + '"'
        + str(section_cd_email)
        + '"'
        + ") AS stf"
        + " LEFT JOIN ("
        + " SELECT"
        + " pay_person_email,"
        + " SUM( pay_fee_yen ) AS pay_fee_yen"
        + " FROM"
        + " sql_fee_order_store"
        + " WHERE"
        + " nyu_nendo = "
        + str(nyu_nendo)
        + " AND"
        + " nyu_date <= "
        + str(nyu_date)
        + " GROUP BY"
        + " pay_person_email"
        + " ) AS fee ON stf.staff_email = fee.pay_person_email"
        + " ORDER BY"
        + " stf.sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data
