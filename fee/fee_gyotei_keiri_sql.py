from _mod import sql_config


def mz_sql_fee_order_store_keiri(fdate_int, section_cd, com_per_sta_value, invoice_sta):
    # 熊本1以外を作成する場合。熊本2はここでは検索されない。ここに来る前に制御されている mz_section_data_fumei_nasi_keiri()
    if section_cd != "3":
        # 東京、法人、invoice_sta=2の場合は、蛭田さんを追加する
        if section_cd == "1" and com_per_sta_value == "company" and invoice_sta == "2":
            sql1 = (
                ""
                + "("
                + "SELECT"
                + " *"
                + " FROM"
                + " ("
                + " SELECT"
                + " sec.section_cd AS section_cd,"
                + " sec.section_name_keiri AS section_name,"
                + " fee.min_pay_gyotei_cd AS pay_gyotei_cd,"
                + " gyo.kanri_cd AS kanri_cd,"
                + " gyo.name AS gyotei_name,"
                + " fee.pay_fee_yen AS pay_fee,"
                + " gyo.kojo_fee AS kojo_fee,"
                + " gyo.gensen_cd AS gensen_cd,"
                + " gyo.bank_name AS bank_name,"
                + " gyo.bank_branch AS bank_branch,"
                + " gyo.bank_kind AS bank_kind,"
                + " gyo.bank_account AS bank_account,"
                + " gyo.bank_account_name AS bank_account_name,"
                + " gyo.kana1moji AS kana1moji,"
                + " gyo.com_per_sta AS com_per_sta,"
                + " gyo.keiri_list_onoff AS keiri_list_onoff,"
                + " gyo.invoice_sta AS invoice_sta"
                + " FROM"
                + " ("
                + " SELECT"
                + " MIN(pay_gyotei_cd) AS min_pay_gyotei_cd,"
                + " SUM(pay_fee_yen) AS pay_fee_yen"
                + " FROM"
                + " sql_fee_order_store"
                + " WHERE"
                + " pay_person_kind like "
                + '"'
                + "%"
                + "gyotei"
                + "%"
                + '"'
                + " AND"
                + " nyu_date = "
                + str(fdate_int)
                + " GROUP BY pay_gyotei_cd"
                + " ) AS fee"
                + " LEFT JOIN sql_gyotei AS gyo ON fee.min_pay_gyotei_cd = gyo.gyotei_cd"
                + " LEFT JOIN sql_section AS sec ON gyo.section_cd = sec.section_cd"
                + ") AS res"
                + " WHERE"
                + " pay_fee != 0"
                + " AND section_cd = "
                + '"'
                + section_cd
                + '"'
                + " AND com_per_sta = "
                + '"'
                + com_per_sta_value
                + '"'
                + " AND keiri_list_onoff = "
                + '"'
                + "on"
                + '"'
                + " AND invoice_sta = "
                + '"'
                + invoice_sta
                + '"'
                + " ORDER BY invoice_sta, kana1moji, kanri_cd"
                + " LIMIT 9999"
                + ")"
            )
            # 蛭田さんを追加
            sql2 = """
                UNION ALL
                (
                SELECT
                section_cd,
                section_name,
                pay_gyotei_cd,
                kanri_cd,
                gyotei_name,
                pay_fee,
                kojo_fee,
                gensen_cd,
                bank_name,
                bank_branch,
                bank_kind,
                bank_account,
                bank_account_name,
                kana1moji,
                com_per_sta,
                keiri_list_onoff,
                invoice_sta
                FROM sql_keiri_list_tuika
                )
            """
            sql = sql1 + sql2
        else:
            sql = (
                ""
                + "SELECT"
                + " *"
                + " FROM"
                + " ("
                + " SELECT"
                + " sec.section_cd AS section_cd,"
                + " sec.section_name_keiri AS section_name,"
                + " fee.min_pay_gyotei_cd AS pay_gyotei_cd,"
                + " gyo.kanri_cd AS kanri_cd,"
                + " gyo.name AS gyotei_name,"
                + " fee.pay_fee_yen AS pay_fee,"
                + " gyo.kojo_fee AS kojo_fee,"
                + " gyo.gensen_cd AS gensen_cd,"
                + " gyo.bank_name AS bank_name,"
                + " gyo.bank_branch AS bank_branch,"
                + " gyo.bank_kind AS bank_kind,"
                + " gyo.bank_account AS bank_account,"
                + " gyo.bank_account_name AS bank_account_name,"
                + " gyo.kana1moji AS kana1moji,"
                + " gyo.com_per_sta AS com_per_sta,"
                + " gyo.keiri_list_onoff AS keiri_list_onoff,"
                + " gyo.invoice_sta AS invoice_sta"
                + " FROM"
                + " ("
                + " SELECT"
                + " MIN(pay_gyotei_cd) AS min_pay_gyotei_cd,"
                + " SUM(pay_fee_yen) AS pay_fee_yen"
                + " FROM"
                + " sql_fee_order_store"
                + " WHERE"
                + " pay_person_kind like "
                + '"'
                + "%"
                + "gyotei"
                + "%"
                + '"'
                + " AND"
                + " nyu_date = "
                + str(fdate_int)
                + " GROUP BY pay_gyotei_cd"
                + " ) AS fee"
                + " LEFT JOIN sql_gyotei AS gyo ON fee.min_pay_gyotei_cd = gyo.gyotei_cd"
                + " LEFT JOIN sql_section AS sec ON gyo.section_cd = sec.section_cd"
                + ") AS res"
                + " WHERE"
                + " pay_fee != 0"
                + " AND section_cd = "
                + '"'
                + section_cd
                + '"'
                + " AND com_per_sta = "
                + '"'
                + com_per_sta_value
                + '"'
                + " AND keiri_list_onoff = "
                + '"'
                + "on"
                + '"'
                + " AND invoice_sta = "
                + '"'
                + invoice_sta
                + '"'
                + " ORDER BY invoice_sta, kana1moji, kanri_cd"
                + ";"
            )

    # section_cd=3, 熊本1の場合は,熊本1と熊本2を両方出す.section_cdは全て3にセットする.
    if section_cd == "3":
        sql = (
            ""
            + "SELECT"
            + '"'
            + "3"
            + '"'
            + "AS section_cd,"
            + " section_name,"
            + " pay_gyotei_cd,"
            + " kanri_cd,"
            + " gyotei_name,"
            + " pay_fee,"
            + " kojo_fee,"
            + " gensen_cd,"
            + " bank_name,"
            + " bank_branch,"
            + " bank_kind,"
            + " bank_account,"
            + " bank_account_name,"
            + " kana1moji,"
            + " com_per_sta,"
            + " keiri_list_onoff,"
            + " invoice_sta"
            + " FROM"
            + " ("
            + " SELECT"
            + " sec.section_cd AS section_cd,"
            + " sec.section_name_keiri AS section_name,"
            + " fee.min_pay_gyotei_cd AS pay_gyotei_cd,"
            + " gyo.kanri_cd AS kanri_cd,"
            + " gyo.name AS gyotei_name,"
            + " fee.pay_fee_yen AS pay_fee,"
            + " gyo.kojo_fee AS kojo_fee,"
            + " gyo.gensen_cd AS gensen_cd,"
            + " gyo.bank_name AS bank_name,"
            + " gyo.bank_branch AS bank_branch,"
            + " gyo.bank_kind AS bank_kind,"
            + " gyo.bank_account AS bank_account,"
            + " gyo.bank_account_name AS bank_account_name,"
            + " gyo.kana1moji AS kana1moji,"
            + " gyo.com_per_sta AS com_per_sta,"
            + " gyo.keiri_list_onoff AS keiri_list_onoff,"
            + " gyo.invoice_sta AS invoice_sta"
            + " FROM"
            + " ("
            + " SELECT"
            + " MIN(pay_gyotei_cd) AS min_pay_gyotei_cd,"
            + " SUM(pay_fee_yen) AS pay_fee_yen"
            + " FROM"
            + " sql_fee_order_store"
            + " WHERE"
            + " pay_person_kind like "
            + '"'
            + "%"
            + "gyotei"
            + "%"
            + '"'
            + " AND"
            + " nyu_date = "
            + str(fdate_int)
            + " GROUP BY pay_gyotei_cd"
            + " ) AS fee"
            + " LEFT JOIN sql_gyotei AS gyo ON fee.min_pay_gyotei_cd = gyo.gyotei_cd"
            + " LEFT JOIN sql_section AS sec ON gyo.section_cd = sec.section_cd"
            + ") AS res"
            + " WHERE"
            + " pay_fee != 0"
            + " AND (section_cd = "
            + '"'
            + "3"
            + '"'
            + " OR "
            + "section_cd = "
            + '"'
            + "4"
            + '"'
            + ")"
            + " AND com_per_sta = "
            + '"'
            + com_per_sta_value
            + '"'
            + " AND keiri_list_onoff = "
            + '"'
            + "on"
            + '"'
            + " AND invoice_sta = "
            + '"'
            + invoice_sta
            + '"'
            + " ORDER BY invoice_sta, kana1moji, kanri_cd"
            + ";"
        )

    sql_data = sql_config.mz_sql(sql)
    return sql_data
