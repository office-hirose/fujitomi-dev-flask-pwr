from _mod import sql_config


# 年月から年度の開始月と終了月を数値で出す
def nendo_year_month(nyu_date_int):

    year = int(str(nyu_date_int)[:4])
    month = int(str(nyu_date_int)[4:])

    if month >= 4:
        nendo = year
        s_year_month = year * 100 + 4
        e_year_month = (year + 1) * 100 + 3
    else:
        nendo = year - 1
        s_year_month = (year - 1) * 100 + 4
        e_year_month = year * 100 + 3

    return nendo, s_year_month, e_year_month


# sql_fee_kakutei
def mz_ruikei(nyu_date_int):

    # 年月から年度の開始月と終了月を数値で出す
    nendo, s_year_month, e_year_month = nendo_year_month(nyu_date_int)

    # 最終月はその時に選択した年月までとする
    sql = f"""
        SELECT
            *
        FROM
            sql_fee_kakutei
        WHERE
        nyu_date >= {s_year_month} AND nyu_date <= {nyu_date_int};
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data
