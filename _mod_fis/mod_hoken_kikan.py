from _mod import sql_config


def mz_hoken_kikan_name(hoken_kikan_cd):
    hoken_kikan_name = ""
    sql = "SELECT * FROM sql_hoken_kikan WHERE hoken_kikan_cd = " + '"' + str(hoken_kikan_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        hoken_kikan_name = dt["hoken_kikan_name"]
    return hoken_kikan_name


def mz_hoken_kikan_data():
    sql = "SELECT * FROM sql_hoken_kikan WHERE onoff_cd = " + '"on"' + " ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_hoken_kikan_year(hoken_kikan_cd):
    sql = "SELECT * FROM sql_hoken_kikan WHERE hoken_kikan_cd = " + '"' + str(hoken_kikan_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data
