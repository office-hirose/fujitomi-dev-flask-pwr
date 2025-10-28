# 共通
from _mod import sql_config


def mz_sql_section():
    sql = (
        "SELECT *"
        + " FROM sql_section"
        + " WHERE"
        + " onoff_cd = "
        + '"on"'
        + " AND"
        + " sort < 9999"
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# def mz_sql_section_kyutou_nasi():
#     sql = (
#         "SELECT *"
#         + " FROM sql_section"
#         + " WHERE"
#         + " onoff_cd = "
#         + '"on"'
#         + " AND"
#         + " sort < 9999"
#         + " AND"
#         + " section_cd != "
#         + '"5"'
#         + " ORDER BY sort;"
#     )
#     sql_data = sql_config.mz_sql(sql)
#     return sql_data


def mz_sql_cat():
    sql = "SELECT * FROM sql_cat ORDER BY cat_cd;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_sql_coltd(cat_cd):
    sql = (
        "SELECT *"
        + " FROM sql_coltd"
        + " WHERE"
        + " onoff_cd = "
        + '"on"'
        + " AND"
        + " cat_cd = "
        + '"'
        + str(cat_cd)
        + '"'
        + " ORDER BY coltd_cd;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_sql_nendo(nyu_date):
    sql = "SELECT *" + " FROM sql_kei_nyu_pay" + " WHERE" + " nyu_year_month_int = " + str(nyu_date) + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        nyu_nendo = dt["nyu_nendo"]
        break
    return nyu_nendo


def mz_staff_data(section_cd):
    sql = (
        "SELECT *"
        + " FROM sql_staff"
        + " WHERE"
        + " sales_cd = "
        + '"on"'
        + " AND"
        + " section_cd = "
        + '"'
        + str(section_cd)
        + '"'
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_staff_data_email(section_cd_email):
    sql = (
        "SELECT"
        + " min(sort) AS sort,"
        + " min(section_cd_email) AS section_cd_email,"
        + " min(staff_email) AS staff_email,"
        + " min(name_simple) AS name_simple"
        + " FROM sql_staff"
        + " WHERE"
        + " sales_cd = "
        + '"on"'
        + " AND"
        + " section_cd_email = "
        + '"'
        + str(section_cd_email)
        + '"'
        + " GROUP BY sql_staff.staff_email"
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# def mz_staff_data_email(section_cd_email):
#     sql = (
#         "SELECT"
#         + " min(sort) AS sort,"
#         + " min(section_cd_email) AS section_cd_email,"
#         + " min(staff_email) AS staff_email,"
#         + " min(name_simple) AS name_simple"
#         + " FROM sql_staff"
#         + " WHERE"
#         + " sales_cd = "
#         + '"on"'
#         + " AND"
#         + " section_cd != "
#         + '"5"'
#         + " AND"
#         + " section_cd_email = "
#         + '"'
#         + str(section_cd_email)
#         + '"'
#         + " GROUP BY sql_staff.staff_email"
#         + " ORDER BY sort;"
#     )
#     sql_data = sql_config.mz_sql(sql)
#     return sql_data
