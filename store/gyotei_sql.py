from _mod import sql_config


# store list sql
def list_sql(gyotei_cd, cat_cd, keijyo_date):

    # select_from
    select_from = "SELECT * FROM sql_order_store"

    # where1
    where1 = " WHERE gyotei1_cd = " + '"' + gyotei_cd + '"'

    # where2
    if cat_cd == "0":
        where2 = ""
    else:
        where2 = " AND cat_cd = " + '"' + cat_cd + '"'

    # where3
    if keijyo_date == 0:
        where3 = ""
    else:
        where3 = " AND keijyo_date = " + str(keijyo_date)

    # order
    order1 = " ORDER BY coltd_cd, keijyo_date, syoken_cd_main, syoken_cd_sub;"

    # execute
    sql = select_from + where1 + where2 + where3 + order1
    sql_data = sql_config.mz_sql(sql)

    return sql_data
