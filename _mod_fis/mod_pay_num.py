from _mod import sql_config


def mz_pay_num_name(pay_num_cd):
    pay_num_name = ""
    if pay_num_cd == "0":
        pay_num_name = "未入力"
    else:
        sql = "SELECT" + " *" + " FROM sql_pay_num" + " WHERE" + " pay_num_cd = " + '"' + str(pay_num_cd) + '"' + ";"
        sql_con = sql_config.mz_sql_con()
        with sql_con.cursor() as cur:
            cur.execute(sql)
            sql_data = cur.fetchall()
        for dt in sql_data:
            pay_num_name = dt["pay_num_name"]
    return pay_num_name


def mz_pay_num_data():
    sql = "SELECT" + " *" + " FROM sql_pay_num" + " WHERE" + " onoff_cd = " + '"on"' + " ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_pay_num_data_sel(pay_num_cd):
    sql = "SELECT" + " *" + " FROM sql_pay_num" + " WHERE" + " pay_num_cd = " + '"' + str(pay_num_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        keisu_year = dt["keisu_year"]
    return keisu_year
