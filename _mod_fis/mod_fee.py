from _mod import sql_config


def mz_fee_data_all():
    sql = "SELECT * FROM sql_fee WHERE onoff_cd = " + '"on"' + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_fee(fee_cd_all):
    fee_name = ""
    fee_ritu_str = ""

    if fee_cd_all == "0" or fee_cd_all == "":
        fee_cat = "1"
        fee_cd = ""
        fee_name = ""
        fee_ritu = 0
        fee_ritu_str = "0%"
    else:
        sql = (
            "SELECT"
            + " fee_cat,"
            + " fee_cd,"
            + " fee_name1,"
            + " fee_name2,"
            + " fee_ritu"
            + " FROM sql_fee"
            + " WHERE"
            + " fee_cd_all = "
            + '"'
            + str(fee_cd_all)
            + '"'
            + ";"
        )
        sql_con = sql_config.mz_sql_con()
        with sql_con.cursor() as cur:
            cur.execute(sql)
            sql_data = cur.fetchall()

        for dt in sql_data:
            fee_cat = dt["fee_cat"]
            fee_cd = dt["fee_cd"]
            fee_name1 = dt["fee_name1"]
            fee_name2 = dt["fee_name2"]
            fee_ritu = dt["fee_ritu"]

        # fee name
        fee_name = str(fee_name1 or "") + str(fee_name2 or "")

        # fee_ritu
        fee_ritu_str = str(fee_ritu) + "%"

    return fee_cat, fee_cd, fee_name, fee_ritu, fee_ritu_str


def mz_fee_name(fee_cd_all):
    fee_name = ""
    if fee_cd_all == "0":
        fee_name = "---"
    else:
        sql = (
            "SELECT"
            + " fee_name1,"
            + " fee_name2"
            + " FROM sql_fee"
            + " WHERE"
            + " fee_cd_all = "
            + '"'
            + str(fee_cd_all)
            + '"'
            + ";"
        )
        sql_con = sql_config.mz_sql_con()
        with sql_con.cursor() as cur:
            cur.execute(sql)
            sql_data = cur.fetchall()

        for dt in sql_data:
            fee_name1 = dt["fee_name1"]
            fee_name2 = dt["fee_name2"]
            fee_name = str(fee_name1 or "") + str(fee_name2 or "")
            break
    return fee_name


def mz_fee_ritu_money(fee_cd_all):
    fee_ritu_str = ""
    sql = (
        "SELECT"
        + " fee_cat,"
        + " fee_ritu"
        + " FROM sql_fee"
        + " WHERE"
        + " fee_cd_all = "
        + '"'
        + str(fee_cd_all)
        + '"'
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)

    for dt in sql_data:
        fee_ritu = dt["fee_ritu"]

    # fee ritu
    fee_ritu_str = str(fee_ritu) + "％"
    return fee_ritu_str


def mz_fee_data(cat_cd, kind_cd_main):
    sql = (
        "SELECT"
        + " *"
        + " FROM sql_fee"
        + " WHERE"
        + " onoff_cd = "
        + '"on"'
        + " AND"
        + " cat_cd = "
        + '"'
        + str(cat_cd)
        + '"'
        + " AND"
        + " kind_cd_main = "
        + '"'
        + str(kind_cd_main)
        + '"'
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_fee_conv(cat_cd, kind_cd_main):
    fee_cd = ""
    fee_cd_all = ""
    fee_cat = ""
    fee_ritu = 0

    sql = (
        "SELECT"
        + " *"
        + " FROM sql_fee"
        + " WHERE"
        + " cat_cd = "
        + '"'
        + str(cat_cd)
        + '"'
        + " AND"
        + " kind_cd_main = "
        + '"'
        + str(kind_cd_main)
        + '"'
        + " ORDER BY fee_cd"
        + " LIMIT 0, 1"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)

    for dt in sql_data:
        fee_cd = dt["fee_cd"]
        fee_cd_all = dt["fee_cd_all"]
        fee_cat = dt["fee_cat"]
        fee_ritu = dt["fee_ritu"]

    return fee_cd, fee_cd_all, fee_cat, fee_ritu
