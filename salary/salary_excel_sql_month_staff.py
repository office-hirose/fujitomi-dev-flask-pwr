from _mod import sql_config


# sql_salary_store
def mz_sql_salary_store(salary_date_int):
    sql = f"""
        SELECT * FROM sql_salary_store WHERE salary_year_month = {salary_date_int};
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# salary_kind_name
def mz_sql_salary_kind_name(salary_kind_cd):
    sql = f"""
        SELECT * FROM sql_salary_kind WHERE salary_kind_cd = {salary_kind_cd};
    """
    sql_data = sql_config.mz_sql(sql)
    sql_data_cnt = len(sql_data)
    if sql_data_cnt == 0:
        salary_kind_name = "ERROR"
    else:
        for dt in sql_data:
            salary_kind_name = dt["salary_kind_name"]
    return salary_kind_name
