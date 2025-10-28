# PyMySql
# https://pymysql.readthedocs.io/en/latest/index.html

import pymysql
import pymysql.cursors
from _mod import fs_config


def mz_sql_con():
    fs_dic = fs_config.fs_dic()
    if fs_dic is None:
        raise ValueError("Failed to load database configuration from Firestore.")

    sql_con = pymysql.connect(
        unix_socket=fs_dic["mysql_unix_socket"],
        database=fs_dic["mysql_database"],
        user=fs_dic["mysql_user"],
        password=fs_dic["mysql_password"],
        cursorclass=pymysql.cursors.DictCursor,
    )
    # sql_con = pymysql.connect(
    #     unix_socket=os.environ["mysql_unix_socket"],
    #     database=os.environ["mysql_database"],
    #     user=os.environ["mysql_user"],
    #     password=os.environ["mysql_password"],
    #     cursorclass=pymysql.cursors.DictCursor,
    # )
    return sql_con


def mz_sql(sql):
    sql_con = mz_sql_con()
    with sql_con.cursor() as cur:
        cur.execute(sql)
        sql_data = cur.fetchall()
    return sql_data
