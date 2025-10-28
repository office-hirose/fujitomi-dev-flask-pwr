from _mod import sql_config


# インポートしたnttgwファイル名の一覧を取得
def mz_sel_imp_file_name():
    sql = "SELECT id, imp_file_name FROM sql_nttgw_imp_file_name_chk ORDER BY id DESC LIMIT 0, 3;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# idからインポートファイル名を取得
def mz_find_imp_file_name(id):
    imp_file_name = ""
    sql = "SELECT id, imp_file_name FROM sql_nttgw_imp_file_name_chk WHERE id = " + str(id) + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        imp_file_name = dt["imp_file_name"]
        break
    return imp_file_name
