from _mod import sql_config


# section all
def mz_section_data_all():
    sql = "SELECT * FROM sql_section ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# section on
def mz_section_data_on():
    sql = "SELECT * FROM sql_section WHERE onoff_cd = " + '"on"' + " ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# user_emailからsection_cdを出す
def mz_section_cd(user_email):
    section_cd = ""
    sql = "SELECT *" + " FROM sql_staff" + " WHERE staff_email = " + '"' + str(user_email) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        section_cd = dt["section_cd"]
    return section_cd


# user_emailからsection_cdを出す。九州統括なし
def mz_section_cd_kyuto_nasi(user_email):
    section_cd_email = ""
    sql = (
        "SELECT *"
        + " FROM sql_staff"
        + " WHERE staff_email = "
        + '"'
        + str(user_email)
        + '"'
        + " AND section_cd != "
        + '"5"'
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        section_cd_email = dt["section_cd_email"]
    return section_cd_email


# section_cdからsection_nameを出す
def mz_section_name(section_cd):
    section_name = ""
    sql = "SELECT * FROM sql_section WHERE section_cd = " + '"' + str(section_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        section_name = dt["section_name"]
    return section_name


def mz_section_name4sum_total(section_cd):
    section_name = "全社"
    sql = "SELECT * FROM sql_section WHERE section_cd = " + '"' + str(section_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        section_name = dt["section_name"]
    return section_name


def mz_section_name4sum_stf(section_cd):
    section_name = "合計"
    sql = "SELECT *" + " FROM sql_section" + " WHERE section_cd = " + '"' + str(section_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        section_name = dt["section_name"]
    return section_name


# section_cdから、sql_data, section_cd, section_nameを出す
def mz_section_data_cd_name(section_cd):
    section_name = ""
    sql = "SELECT *" + " FROM sql_section" + " WHERE section_cd = " + '"' + str(section_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        section_cd = dt["section_cd"]
        section_name = dt["section_name"]
    return sql_data, section_cd, section_name


# セクション全て。九州統括なし。
def mz_section_data_kyuto_nasi():
    sql = (
        "SELECT *"
        + " FROM sql_section"
        + " WHERE onoff_cd = "
        + '"on"'
        + " AND section_cd != "
        + '"5"'
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 最初のデータ。九州統括なし
def mz_section_data_1st():
    sql = (
        "SELECT *"
        + " FROM sql_section"
        + " WHERE onoff_cd = "
        + '"on"'
        + " AND section_cd != "
        + '"5"'
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        section_cd = dt["section_cd"]
        section_name = dt["section_name"]
        break
    return section_cd, section_name


# 不明を除く
def mz_section_data_fumei_nasi():
    sql = """
        SELECT *
        FROM sql_section
        WHERE onoff_cd = "on" AND section_cd != "7777"
        ORDER BY sort;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 不明と熊本2を除く
def mz_section_data_fumei_nasi_keiri():
    sql = """
        SELECT
        section_cd,
        section_name_keiri AS section_name
        FROM sql_section
        WHERE onoff_cd = "on" AND section_cd != "7777" AND section_cd != "4"
        ORDER BY sort;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data
