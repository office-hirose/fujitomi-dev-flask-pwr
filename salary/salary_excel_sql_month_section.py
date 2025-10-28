from _mod import sql_config


# sql_salary_store
def mz_sql_salary_store(salary_date_int):
    sql = f"""
        SELECT
            MIN(staff_section_cd) AS staff_section_cd,
            sum(fee_no_tax) AS fee_no_tax,
            sum(fee_kotei) AS fee_kotei,
            sum(fee_hirei_no_tax) AS fee_hirei_no_tax,
            sum(fee_hirei_tax) AS fee_hirei_tax,
            sum(fee_hirei_tax_20) AS fee_hirei_tax_20,
            sum(fee_total) AS fee_total,
            sum(fee_total_sagaku) AS fee_total_sagaku
        FROM sql_salary_store
        WHERE salary_year_month = {salary_date_int}
        GROUP BY staff_section_cd, sort_section
        ORDER BY sort_section;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# section_name
def mz_sql_section_name(staff_section_cd):
    sql = f"""
        SELECT * FROM sql_section WHERE section_cd = '{staff_section_cd}';
    """
    sql_data = sql_config.mz_sql(sql)
    sql_data_cnt = len(sql_data)
    if sql_data_cnt == 0:
        section_name = "ERROR"
    else:
        for dt in sql_data:
            section_name = dt["section_name"]
    return section_name
