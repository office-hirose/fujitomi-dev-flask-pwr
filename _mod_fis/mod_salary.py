from _mod import sql_config


def mz_salary_kind_data_all():
    sql = "SELECT * FROM sql_salary_kind ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data
