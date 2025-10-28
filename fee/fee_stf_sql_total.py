from _mod import sql_config


def mz_sql_total(nyu_date_int, staff_email):
    tan_fee_yen = 0
    sql = (
        "SELECT sum(pay_fee_yen) AS tan_fee_yen FROM sql_fee_order_store"
        + " WHERE nyu_date = "
        + nyu_date_int
        + " AND pay_person_email = "
        + "'"
        + staff_email
        + "'"
        + " AND (pay_person_kind = 'main' OR pay_person_kind = 'sub')"
        + " GROUP BY pay_person_email;"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        tan_fee_yen = dt["tan_fee_yen"]
    return tan_fee_yen


def mz_sql_total_section(nyu_date_int, staff_email, section_cd):
    tan_fee_yen = 0
    sql = (
        "SELECT sum(pay_fee_yen) AS tan_fee_yen FROM sql_fee_order_store"
        + " WHERE nyu_date = "
        + nyu_date_int
        + " AND pay_person_email = "
        + "'"
        + staff_email
        + "'"
        + " AND (pay_person_kind = 'main' OR pay_person_kind = 'sub')"
        + " AND section_cd = "
        + "'"
        + section_cd
        + "'"
        + " GROUP BY pay_person_email;"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        tan_fee_yen = dt["tan_fee_yen"]
    return tan_fee_yen


def mz_sql_total_main_shimada(nyu_date_int, staff_email, section_cd):
    tan_fee_yen = 0
    sql = (
        "SELECT sum(pay_fee_yen) AS tan_fee_yen FROM sql_fee_order_store"
        + " WHERE nyu_date = "
        + nyu_date_int
        + " AND pay_person_email = "
        + "'"
        + staff_email
        + "'"
        + " AND pay_person_kind = 'main'"
        + " AND section_cd = "
        + "'"
        + section_cd
        + "'"
        + " GROUP BY pay_person_email;"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        tan_fee_yen = dt["tan_fee_yen"]
    return tan_fee_yen


def mz_sql_total_sub_shimada(nyu_date_int, staff_email, section_cd):
    tan_fee_yen = 0
    sql = (
        "SELECT sum(pay_fee_yen) AS tan_fee_yen FROM sql_fee_order_store"
        + " WHERE nyu_date = "
        + nyu_date_int
        + " AND pay_person_email = "
        + "'"
        + staff_email
        + "'"
        + " AND pay_person_kind = 'sub'"
        + " AND section_cd = "
        + "'"
        + section_cd
        + "'"
        + " GROUP BY pay_person_email;"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        tan_fee_yen = dt["tan_fee_yen"]
    return tan_fee_yen
