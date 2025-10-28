from _mod import sql_config


# sql_salary_store
def mz_sql_salary_store(salary_date_int, nendo):

    sql = f"""
        SELECT
            MIN(sort_staff) AS sort_staff,
            MIN(salary_kind_cd) AS salary_kind_cd,
            MIN(sort_section) AS sort_section,
            MIN(staff_section_cd) AS staff_section_cd,
            MIN(staff_email) AS staff_email,
            sum(fee_no_tax) AS fee_no_tax,
            sum(fee_kotei) AS fee_kotei,
            MIN(fee_pay_ritu) AS fee_pay_ritu,
            sum(fee_hirei_no_tax) AS fee_hirei_no_tax,
            MIN(fee_hirei_tax_ritu) AS fee_hirei_tax_ritu,
            sum(fee_hirei_tax) AS fee_hirei_tax,
            sum(fee_hirei_tax_20) AS fee_hirei_tax_20,
            sum(fee_total) AS fee_total,
            sum(fee_total_sagaku) AS fee_total_sagaku,
            MIN(salary_min_flag) AS salary_min_flag,
            MIN(staff_name) AS staff_name
        FROM sql_salary_store
        WHERE nendo = {nendo} AND salary_year_month <= {salary_date_int}
        GROUP BY staff_email, sort_staff
        ORDER BY sort_staff;
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
