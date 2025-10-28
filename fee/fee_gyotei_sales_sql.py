from _mod import sql_config


def mz_sql_fee_order_store_sales(fdate_int, section_cd):
    sql = (
        ""
        + "SELECT"
        + " *"
        + " FROM"
        + " ("
        + " SELECT"
        + " sec.section_cd AS section_cd,"
        + " sec.section_name AS section_name,"
        + " fee.min_pay_gyotei_cd AS pay_gyotei_cd,"
        + " gyo.onoff_cd AS onoff_cd,"
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
        + " gyo.keiri_list_onoff AS keiri_list_onoff"
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
        + " ORDER BY kana1moji, kanri_cd"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data
