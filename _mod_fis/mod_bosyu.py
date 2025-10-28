from _mod import sql_config


def mz_bosyu_data_all():
    sql = "SELECT * FROM sql_bosyu;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_bosyu_name(bosyu_cd):
    bosyu_name = "不明"
    if bosyu_cd != "":
        sql = "SELECT * FROM sql_bosyu WHERE bosyu_cd = " + '"' + str(bosyu_cd) + '"' + ";"
        sql_con = sql_config.mz_sql_con()
        with sql_con.cursor() as cur:
            cur.execute(sql)
            sql_data = cur.fetchall()
        for dt in sql_data:
            bosyu_name = dt["name_simple"]
    return bosyu_name


def mz_bosyu_section_staff(bosyu_cd):
    section_cd = "7777"
    staff1_cd = "empty@fumei"
    staff2_cd = "empty@fumei"
    staff3_cd = "empty@fumei"
    gyotei1_cd = "99990001"
    gyotei2_cd = "99990001"
    gyotei3_cd = "99990001"
    if bosyu_cd != "":
        sql = (
            "SELECT"
            + " sb.bosyu_cd,"
            + " sb.staff_cd,"
            + " ss.section_cd"
            + " FROM sql_bosyu AS sb"
            + " LEFT JOIN sql_staff AS ss ON ss.staff_cd = sb.staff_cd"
            + " WHERE"
            + " sb.bosyu_cd = "
            + '"'
            + str(bosyu_cd)
            + '"'
            + ";"
        )
        sql_con = sql_config.mz_sql_con()
        with sql_con.cursor() as cur:
            cur.execute(sql)
            sql_data = cur.fetchall()
        for dt in sql_data:
            section_cd = dt["section_cd"]
            staff1_cd = dt["staff_cd"]

    # empty_staff_cd 取得
    sql = "SELECT * FROM sql_section WHERE section_cd = " + section_cd + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff2_cd = dt["empty_staff_cd"]
        staff3_cd = dt["empty_staff_cd"]
    return (
        section_cd,
        staff1_cd,
        staff2_cd,
        staff3_cd,
        gyotei1_cd,
        gyotei2_cd,
        gyotei3_cd,
    )


def mz_bosyu_data_find():
    sql = """
        SELECT
        bos.id,
        bos.bosyu_cd AS bosyu_cd,
        bos.cat_cd AS cat_cd,
        bos.staff_cd AS staff_cd,
        bos.name_simple AS name_simple,
        bos.memo AS memo,
        sec.section_cd AS section_cd,
        sec.section_name AS section_name
        FROM sql_bosyu AS bos
        LEFT JOIN sql_staff AS stf ON bos.staff_cd = stf.staff_cd
        LEFT JOIN sql_section AS sec ON stf.section_cd = sec.section_cd
        ORDER BY section_cd, staff_cd;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_bosyu_find_bosyu(bosyu_cd):
    sql = "SELECT * FROM sql_bosyu WHERE bosyu_cd = " + '"' + str(bosyu_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data
