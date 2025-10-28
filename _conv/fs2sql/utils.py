from _mod import sql_config


def truncate_table(table_name):
    sql = f"TRUNCATE TABLE `{table_name}`"
    sql_con = sql_config.mz_sql_con()
    cur = sql_con.cursor()
    cur.execute(sql)
    sql_con.commit()
    return
