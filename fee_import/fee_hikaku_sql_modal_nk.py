from _mod import sql_config


# 入金金額data
def mz_nk(nyu_date_int, coltd_cd):
    sql = f"""
        SELECT *
        FROM
            sql_fee_nyukin
        WHERE
            nyu_date = {nyu_date_int} AND coltd_cd = '{coltd_cd}'
        ORDER BY
            sort;
    """
    nk_data = sql_config.mz_sql(sql)
    return nk_data


# 入金金額CD
def mz_nk_kind():
    sql = "SELECT * FROM sql_fee_nyukin_kind;"
    nk_kind_data = sql_config.mz_sql(sql)
    return nk_kind_data


# section data
def mz_nk_section():
    sql = "SELECT * FROM sql_section;"
    nk_section_data = sql_config.mz_sql(sql)
    return nk_section_data


# bonus data
def mz_bonus(nyu_date_int):
    sql = f"""
        SELECT
            *
        FROM
            sql_fee_nyukin
        WHERE
            nyu_date = {nyu_date_int} AND nyukin_cd = 10;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data
