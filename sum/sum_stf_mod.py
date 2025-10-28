from sum import (
    sum_common_mod,
    sum_stf_sql_data,
    sum_stf_sql_kensu,
    sum_stf_sql_keiko,
)


# data
def mz_data(
    sheet,
    row,
    cf_dic,
    keijyo_nendo,
    keijyo_date_int,
    keiyaku_grp_cd,
    cat_cd,
    section_cd,
    staff_email,
):
    cf_c14_bor = cf_dic["cf_c14_bor"]
    cf_l14_bor = cf_dic["cf_l14_bor"]
    cf_r14_comma_bor = cf_dic["cf_r14_comma_bor"]

    # init
    row += 1  # increment
    left_number = 0  # 左のナンバー
    sheet.set_row(row, 22)  # height

    kensu_cnt_sum_tou = 0
    kensu_cnt_sum_rui = 0
    keiko_cnt_sum_tou = 0
    keiko_cnt_sum_rui = 0

    res_hoken_ryo_year_sum_tou = 0
    res_hoken_ryo_year_sum_rui = 0
    res_fee_money_year_sum_tou = 0
    res_fee_money_year_sum_rui = 0
    res_fee_money_total_sum_tou = 0
    res_fee_money_total_sum_rui = 0

    # -----------------------------------------------------------------------------------------------------------------
    # 当月 メインデータ
    sql_data = sum_stf_sql_data.mz_data_tou(keijyo_date_int, keiyaku_grp_cd, cat_cd, section_cd, staff_email)

    for dt in sql_data:
        left_number += 1
        row += 1

        sheet.write(row, 0, left_number, cf_c14_bor)
        sheet.write(row, 1, dt["coltd_name"], cf_l14_bor)

        sheet.write(row, 4, dt["res_hoken_ryo_year"], cf_r14_comma_bor)
        sheet.write(row, 5, dt["res_fee_money_year"], cf_r14_comma_bor)
        sheet.write(row, 6, dt["res_fee_money_total"], cf_r14_comma_bor)

        if dt["cnt"] is not None:
            res_hoken_ryo_year_sum_tou += int(dt["res_hoken_ryo_year"])
            res_fee_money_year_sum_tou += int(dt["res_fee_money_year"])
            res_fee_money_total_sum_tou += int(dt["res_fee_money_total"])

    # 当月の合計
    row_total = 4
    row_total += int(cat_cd)
    sheet.write(row_total, 4, res_hoken_ryo_year_sum_tou, cf_r14_comma_bor)
    sheet.write(row_total, 5, res_fee_money_year_sum_tou, cf_r14_comma_bor)
    sheet.write(row_total, 6, res_fee_money_total_sum_tou, cf_r14_comma_bor)

    # -----------------------------------------------------------------------------------------------------------------
    # 累計 メインデータ
    row = sum_common_mod.moz_tori_back(cat_cd, row)  # 取り扱い保険会社件数、上に戻す
    sql_data = sum_stf_sql_data.mz_data_rui(
        keijyo_nendo, keijyo_date_int, keiyaku_grp_cd, cat_cd, section_cd, staff_email
    )

    for dt in sql_data:
        row += 1
        sheet.write(row, 10, dt["res_hoken_ryo_year"], cf_r14_comma_bor)
        sheet.write(row, 11, dt["res_fee_money_year"], cf_r14_comma_bor)
        sheet.write(row, 12, dt["res_fee_money_total"], cf_r14_comma_bor)

        if dt["cnt"] is not None:
            res_hoken_ryo_year_sum_rui += int(dt["res_hoken_ryo_year"])
            res_fee_money_year_sum_rui += int(dt["res_fee_money_year"])
            res_fee_money_total_sum_rui += int(dt["res_fee_money_total"])

    # 累計の合計
    row_total = 4
    row_total += int(cat_cd)
    sheet.write(row_total, 10, res_hoken_ryo_year_sum_rui, cf_r14_comma_bor)
    sheet.write(row_total, 11, res_fee_money_year_sum_rui, cf_r14_comma_bor)
    sheet.write(row_total, 12, res_fee_money_total_sum_rui, cf_r14_comma_bor)

    # -----------------------------------------------------------------------------------------------------------------
    # 当月 契約件数
    row = sum_common_mod.moz_tori_back(cat_cd, row)  # 取り扱い保険会社件数分だけ、上に戻す
    sql_data = sum_stf_sql_kensu.mz_data_tou_kensu(keijyo_date_int, keiyaku_grp_cd, cat_cd, section_cd, staff_email)

    for dt in sql_data:
        row += 1
        sheet.write(row, 2, dt["cnt"], cf_r14_comma_bor)

        if dt["cnt"] is not None:
            kensu_cnt_sum_tou += int(dt["cnt"])

    # 当月の契約顧客件数の合計
    row_total = 4
    row_total += int(cat_cd)
    sheet.write(row_total, 2, kensu_cnt_sum_tou, cf_r14_comma_bor)

    # -----------------------------------------------------------------------------------------------------------------
    # 累計 契約件数
    row = sum_common_mod.moz_tori_back(cat_cd, row)  # 取り扱い保険会社件数分だけ、上に戻す
    sql_data = sum_stf_sql_kensu.mz_data_rui_kensu(keijyo_nendo, keiyaku_grp_cd, cat_cd, section_cd, staff_email)

    for dt in sql_data:
        row += 1
        sheet.write(row, 8, dt["cnt"], cf_r14_comma_bor)

        if dt["cnt"] is not None:
            kensu_cnt_sum_rui += int(dt["cnt"])

    # 当月の契約顧客件数の合計
    row_total = 4
    row_total += int(cat_cd)
    sheet.write(row_total, 8, kensu_cnt_sum_rui, cf_r14_comma_bor)

    # -----------------------------------------------------------------------------------------------------------------
    # 当月 契約顧客件数
    row = sum_common_mod.moz_tori_back(cat_cd, row)  # 取り扱い保険会社件数、上に戻す
    sql_data = sum_stf_sql_keiko.mz_keiko_tou(keijyo_date_int, keiyaku_grp_cd, cat_cd, section_cd, staff_email)

    for dt in sql_data:
        row += 1
        sheet.write(row, 3, dt["keijyo_cnt"], cf_r14_comma_bor)

        if dt["keijyo_cnt"] is not None:
            keiko_cnt_sum_tou += int(dt["keijyo_cnt"])

    # 当月の契約顧客件数の合計
    row_total = 4
    row_total += int(cat_cd)
    sheet.write(row_total, 3, keiko_cnt_sum_tou, cf_r14_comma_bor)

    # -----------------------------------------------------------------------------------------------------------------
    # 累計 契約顧客件数
    row = sum_common_mod.moz_tori_back(cat_cd, row)  # 取り扱い保険会社件数、上に戻す
    sql_data = sum_stf_sql_keiko.mz_keiko_rui(
        keijyo_nendo, keijyo_date_int, keiyaku_grp_cd, cat_cd, section_cd, staff_email
    )

    for dt in sql_data:
        row += 1
        sheet.write(row, 9, dt["keijyo_cnt"], cf_r14_comma_bor)

        if dt["keijyo_cnt"] is not None:
            keiko_cnt_sum_rui += int(dt["keijyo_cnt"])

    # 累計の契約顧客件数の合計
    row_total = 4
    row_total += int(cat_cd)
    sheet.write(row_total, 9, keiko_cnt_sum_rui, cf_r14_comma_bor)

    # -----------------------------------------------------------------------------------------------------------------
    data_dic = {
        "kensu_cnt_sum_tou": kensu_cnt_sum_tou,
        "kensu_cnt_sum_rui": kensu_cnt_sum_rui,
        "keiko_cnt_sum_tou": keiko_cnt_sum_tou,
        "keiko_cnt_sum_rui": keiko_cnt_sum_rui,
        "res_hoken_ryo_year_sum_tou": res_hoken_ryo_year_sum_tou,
        "res_hoken_ryo_year_sum_rui": res_hoken_ryo_year_sum_rui,
        "res_fee_money_year_sum_tou": res_fee_money_year_sum_tou,
        "res_fee_money_year_sum_rui": res_fee_money_year_sum_rui,
        "res_fee_money_total_sum_tou": res_fee_money_total_sum_tou,
        "res_fee_money_total_sum_rui": res_fee_money_total_sum_rui,
    }

    return sheet, row, data_dic
