from _mod import sql_config


def mz_gyotei_data_all():
    sql = "SELECT * FROM sql_gyotei ORDER BY kanri_cd;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_gyotei_section_data_all():
    sql = """
    SELECT
        gyo.onoff_cd,
        gyo.sort,
        gyo.section_cd,
        sec.section_name,
        gyo.kana1moji,
        gyo.gyotei_cd,
        gyo.kanri_cd,
        gyo.name_simple,
        gyo.name_simple_len,
        gyo.fee_staff1,
        gyo.fee_staff2,
        gyo.fee_staff3,
        gyo.fee_gyotei
    FROM sql_gyotei AS gyo
    LEFT JOIN sql_section AS sec ON sec.section_cd = gyo.section_cd
    ORDER BY sort, section_cd, kana1moji, gyotei_cd;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_gyotei_data_find():
    sql = """
        SELECT
        gyo.id AS id,
        gyo.onoff_cd AS onoff_cd,
        gyotei.sta_name AS onoff_name,
        gyo.kanri_cd AS kanri_cd,
        gyo.gensen_cd AS gensen_cd,
        gensen.sta_name AS gensen_name,
        gyo.sort AS sort,
        gyo.gyotei_cd AS gyotei_cd,
        gyo.section_cd AS section_cd,
        sec.section_name AS section_name,
        gyo.staff_cd AS staff_cd,
        stf.name_simple AS staff_name,
        gyo.name AS name,
        gyo.name_kana AS name_kana,
        gyo.name_simple AS name_simple,
        gyo.name_simple_len AS name_simple_len,
        gyo.kana1moji AS kana1moji,
        gyo.fee_gyotei AS fee_gyotei,
        gyo.fee_staff1 AS fee_staff1,
        gyo.fee_staff2 AS fee_staff2,
        gyo.fee_staff3 AS fee_staff3,
        gyo.pay_kikan AS pay_kikan,
        gyo.kojo_fee AS kojo_fee,
        gyo.com_per_sta AS com_per_sta,
        gyo_com_per.sta_name AS com_per_name,
        gyo.keiri_list_onoff AS keiri_list_onoff,
        gyo_keiri_list.sta_name AS keiri_list_name,
        gyo.invoice_sta AS invoice_sta,
        gyo_invoice_list.sta_name AS invoice_sta_name,
        gyo.bank_name AS bank_name,
        gyo.bank_branch AS bank_branch,
        gyo.bank_kind AS bank_kind,
        gyo.bank_account AS bank_account,
        gyo.bank_account_name AS bank_account_name,
        gyo.memo AS memo

        FROM sql_gyotei AS gyo

        LEFT JOIN sql_sta AS gyotei
        ON gyotei.catego = 'gyotei'
        AND gyo.onoff_cd = gyotei.sta_cd

        LEFT JOIN sql_sta AS gensen
        ON gensen.catego = 'gensen'
        AND gyo.gensen_cd = gensen.sta_cd

        LEFT JOIN sql_sta AS gyo_com_per
        ON gyo_com_per.catego = 'gyotei_company_personal'
        AND gyo.com_per_sta = gyo_com_per.sta_cd

        LEFT JOIN sql_sta AS gyo_keiri_list
        ON gyo_keiri_list.catego = 'gyotei_keiri_list'
        AND gyo.keiri_list_onoff = gyo_keiri_list.sta_cd

        LEFT JOIN sql_section AS sec
        ON gyo.section_cd = sec.section_cd

        LEFT JOIN sql_staff AS stf
        ON gyo.section_cd = sec.section_cd AND gyo.staff_cd = stf.staff_cd

        LEFT JOIN sql_sta AS gyo_invoice_list
        ON gyo_invoice_list.catego = 'invoice_sta'
        AND gyo.invoice_sta = gyo_invoice_list.sta_cd

        ORDER BY gyo.kanri_cd;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_gyotei_data_xlsx(onoff_cd):
    sql1 = """
        SELECT
        gyotei.sta_name AS onoff_name,
        gyo.section_cd AS section_cd,
        sec.section_name AS section_name,
        gyo.kanri_cd AS kanri_cd,
        gensen.sta_name AS gensen_name,
        stf.name_simple AS staff_name,
        gyo.name AS name,
        gyo.fee_staff1 AS fee_staff1,
        gyo.fee_gyotei AS fee_gyotei,
        gyo.pay_kikan AS pay_kikan,
        gyo.kojo_fee AS kojo_fee,
        gyo.bank_name AS bank_name,
        gyo.bank_branch AS bank_branch,
        gyo.bank_kind AS bank_kind,
        gyo.bank_account AS bank_account,
        gyo.bank_account_name AS bank_account_name,
        gyo.memo AS memo,
        gyo.gyotei_cd AS gyotei_cd,
        gyo_invoice_list.sta_name AS invoice_sta_name

        FROM sql_gyotei AS gyo

        LEFT JOIN sql_sta AS gyotei
        ON gyotei.catego = 'gyotei'
        AND gyo.onoff_cd = gyotei.sta_cd

        LEFT JOIN sql_sta AS gensen
        ON gensen.catego = 'gensen'
        AND gyo.gensen_cd = gensen.sta_cd

        LEFT JOIN sql_sta AS gyo_com_per
        ON gyo_com_per.catego = 'gyotei_company_personal'
        AND gyo.com_per_sta = gyo_com_per.sta_cd

        LEFT JOIN sql_section AS sec
        ON gyo.section_cd = sec.section_cd

        LEFT JOIN sql_staff AS stf
        ON gyo.section_cd = sec.section_cd AND gyo.staff_cd = stf.staff_cd

        LEFT JOIN sql_sta AS gyo_invoice_list
        ON gyo_invoice_list.catego = 'invoice_sta'
        AND gyo.invoice_sta = gyo_invoice_list.sta_cd
    """

    if onoff_cd == "on":
        sql2 = """
            WHERE
            gyo.onoff_cd = 'on'
            AND
            gyo.kanri_cd != 0
            ORDER BY kanri_cd;
        """

    if onoff_cd == "off":
        sql2 = """
        WHERE
        gyo.onoff_cd = 'off'
        ORDER BY gyo.section_cd, gyo.gyotei_cd;
        """

    sql = sql1 + sql2
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_gyotei_name_simple(gyotei_cd):
    gyotei_name_simple = ""
    sql = "SELECT * FROM sql_gyotei WHERE gyotei_cd = " + '"' + str(gyotei_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        gyotei_name_simple = dt["name_simple"]
    return gyotei_name_simple


def mz_kanri_cd_gyotei_name(gyotei_cd):
    kanri_cd = 0
    gyotei_name = ""
    gyotei_name_simple = ""
    sql = "SELECT * FROM sql_gyotei WHERE gyotei_cd = " + '"' + str(gyotei_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        kanri_cd = dt["kanri_cd"]
        gyotei_name = dt["name"]
        gyotei_name_simple = dt["name_simple"]
    return kanri_cd, gyotei_name, gyotei_name_simple


def mz_gyotei_kanri_cd(gyotei_cd):
    kanri_cd = 0
    sql = "SELECT * FROM sql_gyotei WHERE gyotei_cd = " + '"' + str(gyotei_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        kanri_cd = dt["kanri_cd"]
    return kanri_cd


def mz_gyotei_bank(gyotei_cd):
    sp = "　"
    bank_account_all = ""
    bank_account_name = ""
    sql = "SELECT * FROM sql_gyotei WHERE gyotei_cd = " + '"' + str(gyotei_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        bank_account_all = dt["bank_name"] + sp + dt["bank_branch"] + sp + dt["bank_kind"] + sp + dt["bank_account"]
        bank_account_name = dt["bank_account_name"]
    return bank_account_all, bank_account_name


def mz_gyotei_simple_name_len(gyotei_cd):
    gyotei_name_simple_len = 0
    sql = "SELECT * FROM sql_gyotei WHERE gyotei_cd = " + '"' + str(gyotei_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        gyotei_name_simple_len = dt["name_simple_len"]
    return gyotei_name_simple_len


def mz_gyotei_gensen_kojo(gyotei_cd):
    gensen_cd = ""
    kojo_fee = 0
    sql = "SELECT * FROM sql_gyotei WHERE gyotei_cd = " + '"' + str(gyotei_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        gensen_cd = dt["gensen_cd"]
        kojo_fee = dt["kojo_fee"]
    return gensen_cd, kojo_fee


def mz_gyotei_data_sel(gyotei_cd):
    # ここを変更するか検討中
    # sql = (
    #     "SELECT * FROM sql_gyotei WHERE gyotei_cd = " + '"' + str(gyotei_cd) + '"' + ";"
    # )
    # sql1 = """
    #     SELECT
    #     gyo.*,
    #     sta.sta_name
    #     FROM sql_gyotei AS gyo
    #     LEFT JOIN
    #     (
    #     SELECT
    #     *
    #     FROM
    #     sql_sta
    #     WHERE
    #     catego = 'gyotei_bank_kind'
    #     ) AS sta
    #     ON gyo.bank_kind = sta.sta_cd
    #     WHERE gyo.gyotei_cd =
    # """
    # sql2 = '"' + str(gyotei_cd) + '"' + ";"
    # sql = sql1 + sql2
    # print(sql)
    # sql_data = sql_config.mz_sql(sql)

    sql = "SELECT * FROM sql_gyotei WHERE gyotei_cd = " + '"' + str(gyotei_cd) + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_gyotei_data_cd_name(section_cd):
    sql = (
        "SELECT * FROM sql_gyotei"
        + " WHERE"
        + " onoff_cd = "
        + '"on"'
        + " AND"
        + " section_cd = "
        + '"'
        + str(section_cd)
        + '"'
        + " ORDER BY kanri_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        gyotei_cd = dt["gyotei_cd"]
        gyotei_name = dt["name_simple"]
        kanri_cd = dt["kanri_cd"]
        kana1moji = dt["kana1moji"]
        break
    return sql_data, gyotei_cd, gyotei_name, kanri_cd, kana1moji


def mz_gyotei_view(gyotei_cd):
    sql1 = """
    SELECT
    gyo.sort,
    gyo.section_cd,
    sec.section_name,
    gyo.kana1moji,
    gyo.gyotei_cd,
    gyo.name_simple,
    gyo.name_simple_len,
    gyo.fee_staff1,
    gyo.fee_staff2,
    gyo.fee_staff3,
    gyo.fee_gyotei
    FROM sql_gyotei AS gyo
    LEFT JOIN sql_section AS sec
    ON sec.section_cd = gyo.section_cd
    """
    sql2 = " WHERE gyo.gyotei_cd = " + '"' + str(gyotei_cd) + '"'
    sql = sql1 + sql2
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_aiueo_view():
    sql = "SELECT * FROM sql_aiueo ORDER BY aiueo_cd;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_gyotei_list(kana1moji):
    sql1 = """
    SELECT
    gyo.sort,
    gyo.section_cd,
    sec.section_name,
    gyo.kana1moji,
    gyo.gyotei_cd,
    gyo.name_simple,
    gyo.name_simple_len,
    gyo.fee_staff1,
    gyo.fee_staff2,
    gyo.fee_staff3,
    gyo.fee_gyotei
    FROM sql_gyotei AS gyo
    LEFT JOIN sql_section AS sec
    ON sec.section_cd = gyo.section_cd
    """
    sql2 = " WHERE gyo.onoff_cd = " + '"' + "on" + '"' + " AND gyo.kana1moji = " + '"' + kana1moji + '"' + ";"
    sql = sql1 + sql2
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def mz_gyotei_invoice_sta():
    sql = "SELECT * FROM sql_sta WHERE catego='invoice_sta' ORDER BY sort;"
    sql_data = sql_config.mz_sql(sql)
    return sql_data
