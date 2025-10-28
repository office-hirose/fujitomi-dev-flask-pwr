from _mod import sql_config


def mz_kind_main_data_all():
    sql = "SELECT * FROM sql_kind_main WHERE onoff_cd = " + '"on"' + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_kind_sub_data_all():
    sql = "SELECT * FROM sql_kind_sub WHERE onoff_cd = " + '"on"' + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_kind_cd_main2name(kind_cd_main):
    kind_name_main = ""
    sql = "SELECT * FROM sql_kind_main WHERE kind_cd_main = " + '"' + str(kind_cd_main) + '"' + " LIMIT 0, 1;"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        kind_name_main = dt["kind_name_main"]
    return kind_name_main


def mz_kind_cd_sub2name(cat_cd, coltd_cd, kind_cd_main, kind_cd_sub):
    kind_name_sub = ""
    sql = (
        "SELECT * FROM sql_kind_sub"
        + " WHERE"
        + " cat_cd = "
        + '"'
        + str(cat_cd)
        + '"'
        + " AND"
        + " coltd_cd = "
        + '"'
        + str(coltd_cd)
        + '"'
        + " AND"
        + " kind_cd_main = "
        + '"'
        + str(kind_cd_main)
        + '"'
        + " AND"
        + " kind_cd_sub = "
        + '"'
        + str(kind_cd_sub)
        + '"'
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        kind_name_sub = dt["kind_name_sub"]
    return kind_name_sub
