# ---------------------------------------------------
# 共通
# ---------------------------------------------------
from _mod import sql_config


def mz_sql_section():
    sql = "SELECT * FROM sql_section" + " WHERE" + " onoff_cd = " + '"on"' + " AND" + " sort < 9999" + " ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_sql_cat():
    sql = "SELECT * FROM sql_cat ORDER BY cat_cd;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_sql_coltd(cat_cd):
    sql = (
        "SELECT * FROM sql_coltd"
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


def mz_sql_nendo(fdate_int):
    sql = "SELECT * FROM sql_kei_nyu_pay WHERE nyu_year_month_int = " + str(fdate_int) + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        nyu_nendo = dt["nyu_nendo"]
        break
    return nyu_nendo


def mz_staff_data(section_cd):
    sql = (
        "SELECT * FROM sql_staff"
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
