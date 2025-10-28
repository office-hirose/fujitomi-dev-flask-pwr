from _mod import sql_config
import datetime


# 処理実行中かチェックする
def mz_task_sta_chk(task_name):
    task_sta = "end"
    task_start_time = datetime.datetime.now() + datetime.timedelta(hours=9)
    task_exe_user = ""

    sql = "SELECT * FROM sql_task_sta WHERE task_name = " + '"' + task_name + '"' + " AND task_end_time IS NULL;"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        task_sta = dt["task_sta"]
        task_start_time = dt["task_start_time"]
        task_exe_user = dt["task_exe_user"]

    return task_sta, task_start_time, task_exe_user


def mz_task_sta_data():
    sql = "SELECT * FROM sql_task_sta ORDER BY id DESC;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_task_sta_write(task_sta, task_name, task_exe_user):
    # insert
    if task_sta == "working":
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = """
            INSERT INTO sql_task_sta (
                task_sta,
                task_name,
                task_exe_user
            ) VALUES (
                %s,
                %s,
                %s
            );
            """
            cur = sql_con.cursor()
            cur.execute(sql, (task_sta, task_name, task_exe_user))
            sql_con.commit()

    # update
    if task_sta == "end":
        task_end_time = datetime.datetime.now() + datetime.timedelta(hours=9)
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = (
                "UPDATE sql_task_sta SET"
                + " task_sta = %s,"
                + " task_end_time = %s"
                + " WHERE"
                + " task_name = "
                + '"'
                + task_name
                + '"'
                + " AND"
                + " task_end_time IS NULL"
                + " AND"
                + " task_exe_user = "
                + '"'
                + task_exe_user
                + '"'
                + ";"
            )
            cur = sql_con.cursor()
            cur.execute(sql, (task_sta, task_end_time))
            sql_con.commit()
    return
