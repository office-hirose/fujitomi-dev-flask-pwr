from _mod import sql_config


def mz_manki_chk_data_all():
    sql = "SELECT * FROM sql_manki_chk ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data
