from _mod import sql_config


def mz_cust_new_old_name(cust_new_old_cd):
    cust_new_old_name = ""
    sql = (
        "SELECT"
        + " *"
        + " FROM sql_cust_new_old"
        + " WHERE"
        + " cust_new_old_cd = "
        + '"'
        + str(cust_new_old_cd)
        + '"'
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        cust_new_old_name = dt["cust_new_old_name"]
    return cust_new_old_name


def mz_cust_new_old_data():
    sql = "SELECT" + " *" + " FROM sql_cust_new_old" + " ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data
