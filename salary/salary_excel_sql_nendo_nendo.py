from _mod import sql_config


# 年度を検索
def mz_nendo(salary_date_int):
    sql = f"""
        SELECT nendo FROM sql_salary_store WHERE salary_year_month = {salary_date_int};
    """
    sql_data = sql_config.mz_sql(sql)
    sql_data_cnt = len(sql_data)
    if sql_data_cnt == 0:
        nendo = 9999
    else:
        for dt in sql_data:
            nendo = dt["nendo"]
            break
    return nendo
