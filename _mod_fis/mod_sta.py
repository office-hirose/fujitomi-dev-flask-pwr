from _mod import sql_config


def mz_sta_all():
    sql = "SELECT * FROM sql_sta ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_sta_name_admin(catego, sta_cd):
    sta_name_admin = ""
    sql1 = """
    SELECT
        sta_name
    FROM
        sql_sta
    WHERE
    """
    sql2 = " catego = " + '"' + catego + '"'
    sql3 = " AND"
    sql4 = " sta_cd = " + '"' + sta_cd + '"' + ";"
    sql = sql1 + sql2 + sql3 + sql4
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        sta_name_admin = dt["sta_name"]
    return sta_name_admin


def mz_tori():
    sql = """
    SELECT
        *
    FROM
        sql_sta
    WHERE
        onoff_cd = 'on'
        AND
        catego = 'tori'
    ORDER BY
        sort;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_tori_not_all():
    sql = """
    SELECT
        *
    FROM
        sql_sta
    WHERE
        onoff_cd = 'on'
        AND
        catego = 'tori'
        AND
        sta_cd != 'all'
    ORDER BY
        sort;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_kintai():
    sql = """
    SELECT
        *
    FROM
        sql_sta
    WHERE
        onoff_cd = 'on'
        AND
        catego = 'staff'
    ORDER BY
        sort;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_bosyu():
    sql = """
    SELECT
        *
    FROM
        sql_sta
    WHERE
        onoff_cd = 'on'
        AND
        catego = 'cat'
    ORDER BY
        sort;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_gyotei():
    sql = """
    SELECT
        *
    FROM
        sql_sta
    WHERE
        onoff_cd = 'on'
        AND
        catego = 'gyotei'
    ORDER BY
        sort;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_gyotei_xlsx():
    sql = """
    SELECT
        *
    FROM
        sql_sta
    WHERE
        catego = 'gyotei'
        AND
        onoff_cd = 'on'
        AND
        sta_cd != 'all'
    ORDER BY
        sort;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_gensen():
    sql = """
    SELECT
        *
    FROM
        sql_sta
    WHERE
        onoff_cd = 'on'
        AND
        catego = 'gensen'
    ORDER BY
        sort;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data
