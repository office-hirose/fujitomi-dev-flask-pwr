from _mod import sql_config


def mz_coltd_data_all():
    sql = "SELECT * FROM sql_coltd ORDER BY cat_cd, coltd_cd;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_coltd_name(coltd_cd):
    coltd_name = ""
    sql = "SELECT * FROM sql_coltd WHERE coltd_cd = " + '"' + str(coltd_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        coltd_name = dt["name"]
    return coltd_name


def mz_coltd_name_simple(coltd_cd):
    coltd_name_simple = ""
    sql = "SELECT * FROM sql_coltd WHERE coltd_cd = " + '"' + str(coltd_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        coltd_name_simple = dt["name_simple"]
    return coltd_name_simple


def mz_coltd2cat(coltd_cd):
    cat_cd = ""
    sql = "SELECT * FROM sql_coltd WHERE coltd_cd = " + '"' + str(coltd_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        cat_cd = dt["cat_cd"]
    return cat_cd


def mz_coltd_data(cat_cd):
    sql = (
        "SELECT *"
        + " FROM sql_coltd"
        + " WHERE"
        + " onoff_cd = "
        + '"on"'
        + " AND"
        + " cat_cd = "
        + '"'
        + str(cat_cd)
        + '"'
        + " ORDER BY cat_cd, coltd_cd;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_coltd_data_fee():
    sql = """
    SELECT
    coltd.cat_cd,
    cat.cat_name_simple AS cat_name,
    coltd.coltd_cd,
    coltd.name_simple AS coltd_name

    FROM
    sql_coltd AS coltd

    LEFT JOIN sql_cat AS cat
    ON coltd.cat_cd = cat.cat_cd

    WHERE
    coltd.onoff_cd = 'on'

    ORDER BY
    coltd.cat_cd, coltd.coltd_cd;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_coltd_data_find():
    sql = """
    SELECT
    coltd.id AS id,
    coltd.onoff_cd AS onoff_cd,
    coltd.nttgw_data AS nttgw_data,
    sta.sta_name AS sta_name,
    sta.style_color AS sta_style_color,
    sta.style_border AS sta_style_border,
    coltd.cat_cd AS cat_cd,
    cat.cat_name_simple AS cat_name_simple,
    coltd.sort AS coltd_sort,
    coltd.coltd_cd AS coltd_cd,
    coltd.name AS coltd_name,
    coltd.name_simple AS coltd_name_simple,
    coltd.name_simple_len AS coltd_name_simple_len,
    coltd.kaime AS kaime,
    coltd.memo AS memo

    FROM sql_coltd AS coltd
    LEFT JOIN sql_sta AS sta ON sta.catego = 'tori' AND coltd.onoff_cd = sta.sta_cd
    LEFT JOIN sql_cat AS cat ON cat.cat_cd = coltd.cat_cd

    ORDER BY coltd.cat_cd, coltd.coltd_cd;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_coltd_modal(coltd_cd):
    sql = "SELECT * FROM sql_coltd WHERE coltd_cd = " + '"' + str(coltd_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_coltd_onoff_cat(onoff_cd, cat_cd):
    sql = (
        "SELECT *"
        + " FROM sql_coltd"
        + " WHERE"
        + " onoff_cd = "
        + '"'
        + onoff_cd
        + '"'
        + " AND"
        + " cat_cd = "
        + '"'
        + str(cat_cd)
        + '"'
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data
