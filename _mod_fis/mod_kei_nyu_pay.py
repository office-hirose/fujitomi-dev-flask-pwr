from _mod import sql_config, mod_datetime


# keijyo year
def mz_kei_nyu_pay_data():
    now_date_int = mod_datetime.mz_now_date_num()
    now_year_int = mod_datetime.mz_num2yy(now_date_int)
    # now_month_int = mod_datetime.mz_num2mm(now_date_int)
    # year_start = now_year_int - 20
    # 常に2000年から表示できるようにする
    year_start = 2000
    year_end = int(now_year_int) + 1

    sql = (
        "SELECT * FROM sql_kei_nyu_pay"
        + " WHERE"
        + " kei_year >= "
        + str(year_start)
        + " AND"
        + " kei_year <= "
        + str(year_end)
        + " ORDER BY kei_year_month_int DESC;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# keijyo year, jsuites
def mz_kei_nyu_pay_data_jsuites():
    now_date_int = mod_datetime.mz_now_date_num()
    now_year_int = mod_datetime.mz_num2yy(now_date_int)
    # now_month_int = mod_datetime.mz_num2mm(now_date_int)
    # year_start = now_year_int - 20
    # 常に2000年から表示できるようにする
    year_start = 2000
    year_end = int(now_year_int) + 1

    sql = (
        "SELECT"
        + " kei_year_month_int AS id,"
        + " kei_year_month_str AS name"
        + " FROM sql_kei_nyu_pay"
        + " WHERE"
        + " kei_year >= "
        + str(year_start)
        + " AND"
        + " kei_year <= "
        + str(year_end)
        + " ORDER BY kei_year_month_int DESC;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 入金年月専用 fee
def mz_nyu_data_fee():
    now_date_int = mod_datetime.mz_now_date_num()
    now_year_int = mod_datetime.mz_num2yy(now_date_int)
    # now_month_int = mod_datetime.mz_num2mm(now_date_int)
    year_start = int(now_year_int) - 1
    year_end = int(now_year_int) + 0

    sql = (
        "SELECT * FROM sql_kei_nyu_pay"
        + " WHERE"
        + " nyu_year >= "
        + str(year_start)
        + " AND"
        + " nyu_year <= "
        + str(year_end)
        + " ORDER BY nyu_year_month_int DESC;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 計上年月専用 start end
def mz_kei_nyu_pay_data_start_end_kei(fdate_start, fdate_end):
    sql = (
        "SELECT * FROM sql_kei_nyu_pay"
        + " WHERE"
        + " kei_year_month_int >= "
        + str(fdate_start)
        + " AND"
        + " kei_year_month_int <= "
        + str(fdate_end)
        + " ORDER BY kei_year_month_int DESC;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 入金年月専用 start end
def mz_kei_nyu_pay_data_start_end_nyu(fdate_start, fdate_end):
    sql = (
        "SELECT * FROM sql_kei_nyu_pay"
        + " WHERE"
        + " nyu_year_month_int >= "
        + str(fdate_start)
        + " AND"
        + " nyu_year_month_int <= "
        + str(fdate_end)
        + " ORDER BY nyu_year_month_int DESC;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_kei_nyu_pay_sel(fdate_int):
    kei_year_month_str = ""
    sql = "SELECT * FROM sql_kei_nyu_pay WHERE kei_year_month_int = " + str(fdate_int) + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        kei_year_month_str = dt["kei_year_month_str"]
    return kei_year_month_str


def mz_kei_nyu_pay_sel_data(fdate_int):
    sql = "SELECT * FROM sql_kei_nyu_pay WHERE kei_year_month_int = " + str(fdate_int) + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 入金年月専用sel
def mz_kei_nyu_pay_sel_nyu(fdate_int):
    nyu_year_month_str = ""
    sql = "SELECT * FROM sql_kei_nyu_pay WHERE nyu_year_month_int = " + str(fdate_int) + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        nyu_year_month_str = dt["nyu_year_month_str"]
    return nyu_year_month_str


# 入金年月専用data
def mz_kei_nyu_pay_sel_data_nyu(fdate_int):
    sql = "SELECT * FROM sql_kei_nyu_pay WHERE nyu_year_month_int = " + str(fdate_int) + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 年月str作成 202001 -> 2020年01月
def mz_num_date2str_date(num_date):
    str_date = ""
    if num_date == 0:
        str_date = "9999年99月"
    else:
        str_temp = str(num_date)
        yyyy = str_temp[0:4]
        mm = str_temp[4:6]
        str_date = yyyy + "年" + mm + "月"
    return str_date


# ------------------------------------------------------------
# 共通モジュール、計上日を選択する。keijyo, sum_stf, sum_total, sum_list
def mz_common_kei_sel(start):
    now_date_int = mod_datetime.mz_now_date_num()
    now_year_int = mod_datetime.mz_num2yy(now_date_int)
    now_month_int = mod_datetime.mz_num2mm(now_date_int)
    end = int(str(now_year_int) + str(now_month_int).zfill(2))
    kei_data = mz_kei_nyu_pay_data_start_end_kei(start, end)
    return kei_data


# ------------------------------------------------------------
# 共通モジュール、入金日を選択する。
def mz_common_nyu_sel(start):
    now_date_int = mod_datetime.mz_now_date_num()
    now_year_int = mod_datetime.mz_num2yy(now_date_int)
    now_month_int = mod_datetime.mz_num2mm(now_date_int)
    end = int(str(now_year_int) + str(now_month_int).zfill(2))
    nyu_data = mz_kei_nyu_pay_data_start_end_nyu(start, end)
    return nyu_data


# ------------------------------------------------------------
# 共通モジュール、満期日を選択する。
def mz_common_man_sel(start):
    # now date
    now_date_int = mod_datetime.mz_now_date_num()
    now_year_int = mod_datetime.mz_num2yy(now_date_int)
    now_month_int = mod_datetime.mz_num2mm(now_date_int)
    end = int(str(int(now_year_int) + 1) + str(now_month_int).zfill(2))
    kei_data = mz_kei_nyu_pay_data_start_end_kei(start, end)
    return kei_data


# ------------------------------------------------------------
# 共通モジュール、年度を選択する。fee_cre_month
def mz_common_nendo_sel(start):
    now_date_int = mod_datetime.mz_now_date_num()
    now_year_int = mod_datetime.mz_num2yy(now_date_int)
    end = int(now_year_int) + 1
    nendo_data = mz_nendo_data_start_end_nyu(start, end)
    return nendo_data


# ------------------------------------------------------------
# 年度
# ------------------------------------------------------------
# 入金年度専用 start end
def mz_nendo_data_start_end_nyu(nendo_start, nendo_end):
    sql = (
        "SELECT * FROM sql_nendo"
        + " WHERE"
        + " nendo_int >= "
        + str(nendo_start)
        + " AND"
        + " nendo_int <= "
        + str(nendo_end)
        + " ORDER BY nendo_int DESC;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 年度str作成 2020 -> 2020年度
def mz_nendo_int2nendo_str(nendo_int):
    nendo_str = ""
    if nendo_int == 0:
        nendo_str = "9999年度"
    else:
        nendo_str = str(nendo_int) + "年度"
    return nendo_str


# 年月から、その年度の最初の月を算出する
def mz_yyyymm_nendo_start(yyyymm):
    sql = "SELECT * FROM sql_kei_nyu_pay WHERE kei_year_month_int = " + str(yyyymm) + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        kei_nendo = dt["kei_nendo"]

    sql = (
        "SELECT * FROM sql_kei_nyu_pay"
        + " WHERE kei_nendo = "
        + str(kei_nendo)
        + " ORDER BY kei_year_month_int"
        + " LIMIT 0, 1"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        nendo_start_yyyymm = dt["kei_year_month_int"]

    return nendo_start_yyyymm
