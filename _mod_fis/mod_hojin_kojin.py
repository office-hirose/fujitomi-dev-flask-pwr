from _mod import sql_config


def mz_hojin_kojin_data_all():
    sql = "SELECT * FROM sql_hojin_kojin WHERE onoff_cd = 1 ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data
