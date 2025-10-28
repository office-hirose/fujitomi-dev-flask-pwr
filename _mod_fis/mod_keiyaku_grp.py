from _mod import sql_config


def mz_keiyaku_grp_data_all():
    sql = "SELECT * FROM sql_keiyaku_grp ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_keiyaku_grp_name(keiyaku_grp_cd):
    keiyaku_grp_name = ""
    sql = (
        "SELECT"
        + " keiyaku_grp_name"
        + " FROM sql_keiyaku_grp"
        + " WHERE"
        + " keiyaku_grp_cd = "
        + '"'
        + str(keiyaku_grp_cd)
        + '"'
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        keiyaku_grp_name = dt["keiyaku_grp_name"]
    return keiyaku_grp_name
