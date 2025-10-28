from _mod import sql_config


def mz_keiyaku_name(keiyaku_cd):
    keiyaku_name = ""
    sql = "SELECT keiyaku_name FROM sql_keiyaku WHERE keiyaku_cd = " + '"' + str(keiyaku_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        keiyaku_name = dt["keiyaku_name"]
    return keiyaku_name


def mz_keiyaku_data_all():
    sql = "SELECT * FROM sql_keiyaku WHERE onoff_cd = " + '"on"' + " ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data
