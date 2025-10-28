from fee import (
    fee_stf_sql_common,
    fee_stf_sql_tou,
    fee_stf_sql_gol,
)


# create data
def mz_coltd(sheet, cf_dic, row, title_name, nyu_date_int, staff_email):
    cf_l18 = cf_dic["cf_l18"]
    cf_l11_bor = cf_dic["cf_l11_bor"]
    cf_c11_bor = cf_dic["cf_c11_bor"]
    cf_r12_comma = cf_dic["cf_r12_comma"]
    cf_l11_bor_top = cf_dic["cf_l11_bor_top"]
    cf_r14_comma_bor_top = cf_dic["cf_r14_comma_bor_top"]
    cf_l9_bor_btm = cf_dic["cf_l9_bor_btm"]

    # setting ----------------------------------------------------------------------------------------

    sheet.set_paper(9)  # A4 size paper
    sheet.set_default_row(25)  # height

    col = 0
    sheet.set_column(col, col, 4)  # NO

    col += 1
    sheet.set_column(col, col, 4)  # 会社CD

    col += 1
    sheet.set_column(col, col, 35)  # 会社名

    col += 1
    sheet.set_column(col, col, 15)  # 件数・当月

    col += 1
    sheet.set_column(col, col, 15)  # 主担当・当月

    col += 1
    sheet.set_column(col, col, 15)  # 副担当・当月

    col += 1
    sheet.set_column(col, col, 15)  # 担当合計・当月

    col += 1
    sheet.set_column(col, col, 15)  # 提携・当月

    col += 1
    sheet.set_column(col, col, 15)  # 総合計・当月

    # title ----------------------------------------------------------------------------------------

    sheet.set_row(row, 40)  # height
    sheet.write(row, 0, title_name, cf_l18)
    sheet.write(row, 7, "担当印", cf_l9_bor_btm)
    sheet.write(row, 8, "確認印", cf_l9_bor_btm)
    row += 1

    sheet.set_row(row, 10)  # height
    sheet.write(row, 0, "")  # spacer
    row += 1

    sheet.set_row(row, 22)  # height
    sheet.write(row, 0, "No", cf_c11_bor)
    sheet.write(row, 1, "CD", cf_c11_bor)
    sheet.write(row, 2, "分野/会社名", cf_l11_bor)
    sheet.write(row, 3, "件数", cf_c11_bor)
    sheet.write(row, 4, "主担当", cf_c11_bor)
    sheet.write(row, 5, "副担当", cf_c11_bor)
    sheet.write(row, 6, "担当合計", cf_c11_bor)
    sheet.write(row, 7, "提携", cf_c11_bor)
    sheet.write(row, 8, "総合計", cf_c11_bor)

    # data ----------------------------------------------------------------------------------------

    cat_data = fee_stf_sql_common.mz_sql_cat()

    # ---------------------------------------------------
    # 総合計
    # ---------------------------------------------------

    # init
    gtotal_tou_kensu = 0
    gtotal_tou_fee_main = 0
    gtotal_tou_fee_sub = 0
    gtotal_tou_fee_main_sub = 0
    gtotal_tou_fee_gyo = 0
    gtotal_tou_fee_total = 0

    # G2.分野別合計・当月・件数
    row += 2
    sql_data = fee_stf_sql_gol.mz_sql_fee_tou_kensu_sum(nyu_date_int, staff_email)
    left_number = 1
    for dt in sql_data:
        sheet.write(row, 0, left_number, cf_c11_bor)
        sheet.write(row, 1, dt["cat_cd"], cf_c11_bor)
        sheet.write(row, 2, dt["cat_name"], cf_l11_bor)
        sheet.write(row, 3, dt["kensu"], cf_r12_comma)
        left_number += 1
        row += 1
        res = mz_gtotal_calc(dt["kensu"])
        gtotal_tou_kensu += res

    # G3.分野別合計・当月・手数料・主担当
    row += -3
    sql_data = fee_stf_sql_gol.mz_sql_fee_tou_fee_main_sum(nyu_date_int, staff_email)
    for dt in sql_data:
        sheet.write(row, 4, dt["pay_fee_yen"], cf_r12_comma)
        row += 1
        res = mz_gtotal_calc(dt["pay_fee_yen"])
        gtotal_tou_fee_main += res

    # G4.分野別合計・当月・手数料・副担当
    row += -3
    sql_data = fee_stf_sql_gol.mz_sql_fee_tou_fee_sub_sum(nyu_date_int, staff_email)
    for dt in sql_data:
        sheet.write(row, 5, dt["pay_fee_yen"], cf_r12_comma)
        row += 1
        res = mz_gtotal_calc(dt["pay_fee_yen"])
        gtotal_tou_fee_sub += res

    # G5.分野別合計・当月・手数料・担当合計
    row += -3
    sql_data = fee_stf_sql_gol.mz_sql_fee_tou_fee_main_sub_sum(nyu_date_int, staff_email)
    for dt in sql_data:
        sheet.write(row, 6, dt["pay_fee_yen"], cf_r12_comma)
        row += 1
        res = mz_gtotal_calc(dt["pay_fee_yen"])
        gtotal_tou_fee_main_sub += res

    # G6.分野別合計・当月・手数料・提携
    row += -3
    sql_data = fee_stf_sql_gol.mz_sql_fee_tou_fee_gyo_sum(nyu_date_int, staff_email)
    for dt in sql_data:
        sheet.write(row, 7, dt["pay_fee_yen"], cf_r12_comma)
        row += 1
        res = mz_gtotal_calc(dt["pay_fee_yen"])
        gtotal_tou_fee_gyo += res

    # G7.分野別合計・当月・手数料・総合計
    row += -3
    sql_data = fee_stf_sql_gol.mz_sql_fee_tou_fee_total_sum(nyu_date_int, staff_email)
    for dt in sql_data:
        sheet.write(row, 8, dt["pay_fee_yen"], cf_r12_comma)
        row += 1
        res = mz_gtotal_calc(dt["pay_fee_yen"])
        gtotal_tou_fee_total += res

    # S1.分野別合計・当月・件数
    sheet.write(row, 0, "", cf_l11_bor_top)
    sheet.write(row, 1, "", cf_l11_bor_top)
    sheet.write(row, 2, "総合計", cf_l11_bor_top)
    sheet.write(row, 3, gtotal_tou_kensu, cf_r14_comma_bor_top)

    # S3.分野別合計・当月・手数料・主担当
    sheet.write(row, 4, gtotal_tou_fee_main, cf_r14_comma_bor_top)

    # S4.分野別合計・当月・手数料・副担当
    sheet.write(row, 5, gtotal_tou_fee_sub, cf_r14_comma_bor_top)

    # S5.分野別合計・当月・手数料・担当合計
    sheet.write(row, 6, gtotal_tou_fee_main_sub, cf_r14_comma_bor_top)

    # S6.分野別合計・当月・手数料・提携
    sheet.write(row, 7, gtotal_tou_fee_gyo, cf_r14_comma_bor_top)

    # S7.分野別合計・当月・手数料・総合計
    sheet.write(row, 8, gtotal_tou_fee_total, cf_r14_comma_bor_top)

    # ---------------------------------------------------
    # 保険会社別
    # ---------------------------------------------------

    # init
    start_row = row + 2

    # L2.当月・件数
    row = start_row
    for cdt in cat_data:
        left_number = 1
        sql_data = fee_stf_sql_tou.mz_sql_fee_tou_kensu(nyu_date_int, cdt["cat_cd"], staff_email)
        for dt in sql_data:
            sheet.write(row, 0, left_number, cf_c11_bor)
            sheet.write(row, 1, dt["coltd_cd"], cf_c11_bor)
            sheet.write(row, 2, dt["coltd_name"], cf_l11_bor)
            sheet.write(row, 3, dt["kensu"], cf_r12_comma)
            left_number += 1
            row += 1
        row += 1

    # L3.当月・手数料・主担当
    row = start_row
    for cdt in cat_data:
        sql_data = fee_stf_sql_tou.mz_sql_fee_tou_fee_main(nyu_date_int, cdt["cat_cd"], staff_email)
        for dt in sql_data:
            sheet.write(row, 4, dt["pay_fee_yen"], cf_r12_comma)
            row += 1
        row += 1

    # L4.当月・手数料・副担当
    row = start_row
    for cdt in cat_data:
        sql_data = fee_stf_sql_tou.mz_sql_fee_tou_fee_sub(nyu_date_int, cdt["cat_cd"], staff_email)
        for dt in sql_data:
            sheet.write(row, 5, dt["pay_fee_yen"], cf_r12_comma)
            row += 1
        row += 1

    # L5.当月・手数料・担当合計
    row = start_row
    for cdt in cat_data:
        sql_data = fee_stf_sql_tou.mz_sql_fee_tou_fee_main_sub(nyu_date_int, cdt["cat_cd"], staff_email)
        for dt in sql_data:
            sheet.write(row, 6, dt["pay_fee_yen"], cf_r12_comma)
            row += 1
        row += 1

    # L6.当月・手数料・提携
    row = start_row
    for cdt in cat_data:
        sql_data = fee_stf_sql_tou.mz_sql_fee_tou_fee_gyo(nyu_date_int, cdt["cat_cd"], staff_email)
        for dt in sql_data:
            sheet.write(row, 7, dt["pay_fee_yen"], cf_r12_comma)
            row += 1
        row += 1

    # L7.当月・手数料・総合計
    row = start_row
    for cdt in cat_data:
        sql_data = fee_stf_sql_tou.mz_sql_fee_tou_fee_total(nyu_date_int, cdt["cat_cd"], staff_email)
        for dt in sql_data:
            sheet.write(row, 8, dt["pay_fee_yen"], cf_r12_comma)
            row += 1
        row += 1

    return sheet, row


# 合計計算用 nullを0に変換
def mz_gtotal_calc(chk_data):
    if chk_data is None:
        res = 0
    else:
        res = int(chk_data)
    return res
