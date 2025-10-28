from _mod import sql_config


# staff all
def mz_staff_data_all():
    sql = "SELECT * FROM sql_staff ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# staff master
def mz_staff_data_find():
    sql = """
        SELECT
        stf.id AS id,
        stf.onoff_cd AS onoff_cd,
        stf.sales_cd AS sales_cd,
        stf.sort AS sort,

        sta.sta_name AS sta_name,
        sta.style_color AS sta_style_color,
        sta.style_border AS sta_style_border,

        stf.staff_email AS staff_email,
        stf.staff_cd AS staff_cd,

        stf.section_cd AS section_cd,
        stf.section_cd_email AS section_cd_email,

        stf.name AS name,
        stf.name_kana AS name_kana,
        stf.name_simple AS name_simple,
        stf.name_simple_len AS name_simple_len,
        stf.kana1moji AS kana1moji,

        stf.nttgw_send_email_onoff AS nttgw_send_email_onoff,
        stf.send_email_onoff AS send_email_onoff,
        stf.send_email AS send_email,

        stf.pay_rate AS pay_rate,
        stf.kojo_fee AS kojo_fee,

        stf.memo AS memo,
        stf.memo_pass AS memo_pass,
        stf.w3_text_color AS w3_text_color,

        sec.section_name AS section_name,

        lm.level_cd AS level_cd,
        lml.level_name AS level_name,
        lml.style_color AS level_style_color

        FROM sql_staff AS stf

        LEFT JOIN sql_sta AS sta ON sta.catego = 'staff' AND stf.onoff_cd = sta.sta_cd
        LEFT JOIN sql_section AS sec ON stf.section_cd = sec.section_cd
        LEFT JOIN com_lm AS lm ON stf.staff_email = lm.lm_email
        LEFT JOIN com_lm_level AS lml ON lm.level_cd = lml.level_cd

        ORDER BY stf.section_cd, stf.sort;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_staff_cd(user_email):
    staff_cd = ""
    sql = "SELECT *" + " FROM sql_staff" + " WHERE" + " staff_email = " + '"' + str(user_email) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff_cd = dt["staff_cd"]
    return staff_cd


def mz_staff_name(staff_cd):
    staff_name = ""
    sql = "SELECT *" + " FROM sql_staff" + " WHERE" + " staff_cd = " + '"' + str(staff_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff_name = dt["name"]
    return staff_name


def mz_staff_email(staff_cd):
    staff_email = ""
    sql = "SELECT *" + " FROM sql_staff" + " WHERE" + " staff_cd = " + '"' + str(staff_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff_email = dt["staff_email"]
    return staff_email


def mz_staff_name_nospace(staff_cd):
    staff_name = ""
    sql = "SELECT *" + " FROM sql_staff" + " WHERE" + " staff_cd = " + '"' + str(staff_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff_name = (dt["name"]).replace(" ", "")
    return staff_name


# staff_cdからstaff_nameを出す
def mz_staff_name_simple(staff_cd):
    staff_name_simple = ""
    sql = "SELECT *" + " FROM sql_staff" + " WHERE" + " staff_cd = " + '"' + str(staff_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff_name_simple = dt["name_simple"]
    return staff_name_simple


# staff_emailからstaff_nameを出す
def mz_staff_name_simple_email(staff_email):
    staff_name_simple = ""
    sql = "SELECT *" + " FROM sql_staff" + " WHERE" + " staff_email = " + '"' + str(staff_email) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff_name_simple = dt["name_simple"]
    return staff_name_simple


def mz_staff_name_kana(staff_cd):
    staff_name_kana = ""
    sql = "SELECT *" + " FROM sql_staff" + " WHERE" + " staff_cd = " + '"' + str(staff_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff_name_kana = dt["name_kana"]
    return staff_name_kana


def mz_staff_email2staff_name_simple(user_email):
    staff_name_simple = ""
    if user_email == "empty@tokyo":
        staff_name_simple = "-"
    else:
        sql = "SELECT *" + " FROM sql_staff" + " WHERE" + " staff_email = " + '"' + str(user_email) + '"' + ";"
        sql_con = sql_config.mz_sql_con()
        with sql_con.cursor() as cur:
            cur.execute(sql)
            sql_data = cur.fetchall()
        for dt in sql_data:
            staff_name_simple = dt["name_simple"]
    return staff_name_simple


# スタッフ section内の全て
def mz_staff_data(section_cd):
    sql = (
        "SELECT *"
        + " FROM sql_staff"
        + " WHERE"
        + " onoff_cd = "
        + '"on"'
        + " AND"
        + " section_cd = "
        + '"'
        + str(section_cd)
        + '"'
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# スタッフ全て。staff_email
def mz_staff_data_email(section_cd_email):
    sql = (
        "SELECT *"
        + " FROM sql_staff"
        + " WHERE"
        + " onoff_cd = "
        + '"on"'
        + " AND"
        + " section_cd_email = "
        + '"'
        + str(section_cd_email)
        + '"'
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# スタッフ全て。staff_email、「なし」を除く
def mz_staff_data_email_not_nasi(section_cd_email):
    sql = (
        "SELECT *"
        + " FROM sql_staff"
        + " WHERE"
        + " onoff_cd = "
        + '"on"'
        + " AND"
        + " section_cd_email = "
        + '"'
        + str(section_cd_email)
        + '"'
        + " AND"
        + " name != "
        + '"'
        + "なし"
        + '"'
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 最初のデータ
def mz_staff_data_1st(section_cd_email):
    sql = (
        "SELECT *"
        + " FROM sql_staff"
        + " WHERE"
        + " onoff_cd = "
        + '"on"'
        + " AND"
        + " section_cd_email = "
        + '"'
        + str(section_cd_email)
        + '"'
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff_email = dt["staff_email"]
        staff_name = dt["name_simple"]
        break
    return staff_email, staff_name


# 最初のデータ、「なし」を除く
def mz_staff_data_1st_not_nasi(section_cd_email):
    sql = (
        "SELECT *"
        + " FROM sql_staff"
        + " WHERE"
        + " onoff_cd = "
        + '"on"'
        + " AND"
        + " section_cd_email = "
        + '"'
        + str(section_cd_email)
        + '"'
        + " AND"
        + " name != "
        + '"'
        + "なし"
        + '"'
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff_email = dt["staff_email"]
        staff_name = dt["name_simple"]
        break
    return staff_email, staff_name


def mz_staff_data_sum(section_cd):
    sql = (
        "SELECT *"
        + " FROM sql_staff"
        + " WHERE"
        + " sales_cd = "
        + '"on"'
        + " AND"
        + " section_cd = "
        + '"'
        + str(section_cd)
        + '"'
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_staff_data_fee(section_cd):
    sql = (
        "SELECT *"
        + " FROM sql_staff"
        + " WHERE"
        + " onoff_cd = "
        + '"on"'
        + " AND"
        + " section_cd = "
        + '"'
        + str(section_cd)
        + '"'
        + " ORDER BY sort;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_staff_data_cd(user_email):
    staff_cd = ""
    sql = "SELECT *" + " FROM sql_staff" + " WHERE" + " staff_email = " + '"' + str(user_email) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff_cd = dt["staff_cd"]
    return sql_data, staff_cd


# user_emailから、sql_data, staff_cd, staff_name, section_cdを出す
def mz_staff_data_cd_name_section(user_email):
    staff_cd = ""
    staff_name = ""
    section_cd = ""
    sql = "SELECT *" + " FROM sql_staff" + " WHERE" + " staff_email = " + '"' + str(user_email) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff_cd = dt["staff_cd"]
        staff_name = dt["name_simple"]
        section_cd = dt["section_cd"]
    return sql_data, staff_cd, staff_name, section_cd


# user_emailから、sql_data, staff_email, staff_nameを出す
def mz_staff_data_email_name(user_email):
    staff_email = ""
    staff_name = ""
    sql = "SELECT *" + " FROM sql_staff" + " WHERE" + " staff_email = " + '"' + str(user_email) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        staff_email = dt["staff_email"]
        staff_name = dt["name_simple"]
    return sql_data, staff_email, staff_name


def mz_staff_send_email(user_email):
    send_email = ""
    sql = "SELECT *" + " FROM sql_staff" + " WHERE" + " staff_email = " + '"' + str(user_email) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        send_email = dt["send_email"]
    return send_email


def mz_staff_gyotei_email(section_cd):
    gyotei_email = ""
    sql = (
        "SELECT *"
        + " FROM sql_staff"
        + " WHERE"
        + " section_cd = "
        + '"'
        + str(section_cd)
        + '"'
        + " AND"
        + " staff_cd like "
        + '"'
        + "%"
        + "gyotei"
        + "%"
        + '"'
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        gyotei_email = dt["staff_email"]
    return gyotei_email


def mz_staff_modal(staff_cd):
    sql = "SELECT *" + " FROM sql_staff" + " WHERE" + " staff_cd = " + '"' + staff_cd + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_staff_for_fee(staff_email):
    sql = "SELECT * FROM sql_staff WHERE staff_email = " + '"' + str(staff_email) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data
