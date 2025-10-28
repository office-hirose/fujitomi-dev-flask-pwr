from _mod import sql_config


def mz_cat_data_all():
    sql = "SELECT * FROM sql_cat ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_cat_name(cat_cd):
    cat_name = ""
    sql = "SELECT" + " cat_name" + " FROM sql_cat" + " WHERE" + " cat_cd = " + '"' + str(cat_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        cat_name = dt["cat_name"]
    return cat_name


def mz_cat_name_simple(cat_cd):
    cat_name_simple = ""
    sql = "SELECT" + " cat_name_simple" + " FROM sql_cat" + " WHERE" + " cat_cd = " + '"' + str(cat_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        cat_name_simple = dt["cat_name_simple"]
    return cat_name_simple


def mz_cat_data(cat_cd):
    sql = (
        "SELECT" + " cat_cd," + " cat_name" + " FROM sql_cat" + " WHERE" + " cat_cd = " + '"' + str(cat_cd) + '"' + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_cat_coltd(cat_cd):
    sql = (
        "SELECT"
        + " cat_cd,"
        + " coltd_cd"
        + " FROM sql_coltd"
        + " WHERE"
        + " onoff_cd = "
        + '"on"'
        + " AND"
        + " cat_cd = "
        + '"'
        + str(cat_cd)
        + '"'
        + " ORDER BY sort"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        coltd_cd = dt["coltd_cd"]
        break
    return coltd_cd


# def mz_cat_data_find(onoff_cd):

#     sql1 = '''
#     SELECT
#     coltd.onoff_cd AS onoff_cd,
#     sta.sta_name AS sta_name,
#     sta.style_color AS sta_style_color,
#     sta.style_border AS sta_style_border,

#     cat.sort AS sort,
#     coltd.cat_cd AS cat_cd,
#     cat.cat_name_simple AS cat_name_simple,
#     coltd.coltd_cd AS coltd_cd,
#     coltd.name AS name,
#     coltd.name_simple AS name_simple,
#     coltd.name_simple_len AS name_simple_len,
#     coltd.memo AS memo

#     FROM
#     sql_coltd AS coltd

#     LEFT JOIN sql_cat AS cat
#     ON cat.cat_cd = coltd.cat_cd

#     LEFT JOIN sql_sta AS sta
#     ON sta.catego = 'cat'
#     AND cat.cat_cd = sta.sta_cd
#     '''

#     if onoff_cd == 'all':
#         sql2 = ''
#     else:
#         sql2 = ' WHERE coltd.onoff_cd = ' + '\"' + onoff_cd + '\"'

#     sql3 = ' ORDER BY coltd.cat_cd, coltd.coltd_cd;'
#     sql = sql1 + sql2 + sql3
#     sql_con = sql_config.mz_sql_con()
#     with sql_con.cursor() as cur:
#         cur.execute(sql)
#         sql_data = cur.fetchall()
#     return sql_data
