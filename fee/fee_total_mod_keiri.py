from _mod_fis import mod_section
from fee import (
    fee_total_sql_common,
    fee_total_sql_keiri_gol,
    fee_total_sql_keiri_rui,
    fee_total_sql_keiri_tou,
)


# cell width, height set
def mz_setting_sum(sheet):
    # section data
    sec_data = mod_section.mz_section_data_on()

    sheet.set_paper(9)  # A4 size paper
    sheet.set_default_row(22)  # height

    sheet.set_column(0, 0, 4)  # NO
    sheet.set_column(1, 1, 42)  # 会社名

    # 当月
    col = 1
    for dt in sec_data:
        col += 1
        sheet.set_column(col, col, 18)

    # 合計
    col += 1
    sheet.set_column(col, col, 18)

    # ブランク
    col += 1
    sheet.set_column(col, col, 1)

    # 年度累計
    for dt in sec_data:
        col += 1
        sheet.set_column(col, col, 18)

    # 合計
    col += 1
    sheet.set_column(col, col, 18)

    return sheet


# title
def mz_title_sum(sheet, cf_dic, row, title_name, nyu_nendo_str):
    cf_l18 = cf_dic["cf_l18"]
    cf_l11_bor_btm = cf_dic["cf_l11_bor_btm"]
    cf_l14_bor = cf_dic["cf_l14_bor"]
    cf_c14_bor = cf_dic["cf_c14_bor"]

    # section data 営業所の件数を取得
    sec_data = mod_section.mz_section_data_on()
    kensu = len(sec_data)

    # 印鑑
    sheet.set_row(row, 40)  # height
    sheet.write(row, 0, title_name, cf_l18)
    sheet.write(row, (kensu * 2) + 3, "担当印", cf_l11_bor_btm)
    sheet.write(row, (kensu * 2) + 4, "確認印", cf_l11_bor_btm)
    row += 1

    # spacer
    sheet.set_row(row, 10)  # height
    sheet.write(row, 0, "")
    row += 1

    # タイトル
    sheet.set_row(row, 22)  # height
    sheet.merge_range(row, 0, row + 1, 0, "No", cf_c14_bor)
    sheet.merge_range(row, 1, row + 1, 1, "分野/会社名", cf_l14_bor)
    sheet.merge_range(row, 2, row, kensu + 2, "当月", cf_c14_bor)
    sheet.merge_range(row, kensu + 4, row, (kensu * 2) + 4, "年度累計", cf_c14_bor)
    row += 1

    # 当月の営業所名作成
    col = 1
    for dt in sec_data:
        section_name = dt["section_name"]
        col += 1
        sheet.write(row, col, section_name, cf_c14_bor)

    col += 1
    sheet.write(row, col, "合計", cf_c14_bor)

    # 累計の営業所名作成
    col += 1  # 空白部分
    for dt in sec_data:
        section_name = dt["section_name"]
        col += 1
        sheet.write(row, col, section_name, cf_c14_bor)

    col += 1
    sheet.write(row, col, "合計", cf_c14_bor)

    return sheet, row


# create data
def mz_data_sum(sheet, cf_dic, row, nyu_date, nyu_nendo):
    cf_l14_bor = cf_dic["cf_l14_bor"]
    cf_c14_bor = cf_dic["cf_c14_bor"]
    cf_r14_comma = cf_dic["cf_r14_comma"]
    cf_l14_bor_top = cf_dic["cf_l14_bor_top"]
    cf_r14_comma_bor_top = cf_dic["cf_r14_comma_bor_top"]

    # ---------------------------------------------------
    # 総合計
    # ---------------------------------------------------

    # init
    sec_data = mod_section.mz_section_data_on()
    cat_data = fee_total_sql_common.mz_sql_cat()
    col = 1

    # title
    row += 2
    sql_data = fee_total_sql_common.mz_sql_cat()
    left_number = 1
    for dt in sql_data:
        sheet.write(row, 0, left_number, cf_c14_bor)
        sheet.write(row, col, dt["cat_name_simple"], cf_l14_bor)
        left_number += 1
        row += 1
    sheet.write(row, 0, "", cf_l14_bor_top)
    sheet.write(row, col, "総合計", cf_l14_bor_top)

    # 当月・営業所別
    for dt in sec_data:
        section_cd = dt["section_cd"]

        # init
        gtotal = 0
        row += -3
        col += 1

        sql_data = fee_total_sql_keiri_gol.mz_sql_fee_tou_sum(nyu_date, section_cd)
        for dt in sql_data:
            sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
            row += 1
            res = mz_gtotal_calc(dt["pay_fee_yen"])
            gtotal += res
        sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

    # 当月・合計
    gtotal = 0
    row += -3
    col += 1
    section_cd = "all"
    sql_data = fee_total_sql_keiri_gol.mz_sql_fee_tou_sum(nyu_date, section_cd)
    for dt in sql_data:
        sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
        row += 1
        res = mz_gtotal_calc(dt["pay_fee_yen"])
        gtotal += res
    sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

    # ブランク
    col += 1

    # 累計・営業所別
    for dt in sec_data:
        section_cd = dt["section_cd"]

        # init
        gtotal = 0
        row += -3
        col += 1

        sql_data = fee_total_sql_keiri_gol.mz_sql_fee_rui_sum(nyu_date, nyu_nendo, section_cd)
        for dt in sql_data:
            sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
            row += 1
            res = mz_gtotal_calc(dt["pay_fee_yen"])
            gtotal += res
        sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

    # 累計・合計
    gtotal = 0
    row += -3
    col += 1
    section_cd = "all"
    sql_data = fee_total_sql_keiri_gol.mz_sql_fee_rui_sum(nyu_date, nyu_nendo, section_cd)
    for dt in sql_data:
        sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
        row += 1
        res = mz_gtotal_calc(dt["pay_fee_yen"])
        gtotal += res
    sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

    # ---------------------------------------------------
    # 保険会社別リスト
    # ---------------------------------------------------

    # init
    start_row = row + 2
    col = 1

    # title
    row = start_row
    for cdt in cat_data:
        left_number = 1
        sql_data = fee_total_sql_common.mz_sql_coltd(cdt["cat_cd"])
        for dt in sql_data:
            sheet.write(row, 0, left_number, cf_c14_bor)
            sheet.write(row, col, dt["name_simple"], cf_l14_bor)
            left_number += 1
            row += 1
        row += 1

    # 当月・営業所別
    for dt in sec_data:
        section_cd = dt["section_cd"]
        row = start_row
        col += 1

        for cdt in cat_data:
            sql_data = fee_total_sql_keiri_tou.mz_sql_fee_tou_list(nyu_date, cdt["cat_cd"], section_cd)
            for dt in sql_data:
                sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
                row += 1
            row += 1

    # 当月・合計
    row = start_row
    col += 1
    section_cd = "all"
    for cdt in cat_data:
        sql_data = fee_total_sql_keiri_tou.mz_sql_fee_tou_list(nyu_date, cdt["cat_cd"], section_cd)
        for dt in sql_data:
            sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
            row += 1
        row += 1

    # ブランク
    col += 1

    # 累計・営業所別
    for dt in sec_data:
        section_cd = dt["section_cd"]
        row = start_row
        col += 1

        for cdt in cat_data:
            sql_data = fee_total_sql_keiri_rui.mz_sql_fee_rui_list(nyu_date, nyu_nendo, cdt["cat_cd"], section_cd)
            for dt in sql_data:
                sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
                row += 1
            row += 1

    # 累計・合計
    row = start_row
    col += 1
    section_cd = "all"
    for cdt in cat_data:
        sql_data = fee_total_sql_keiri_rui.mz_sql_fee_rui_list(nyu_date, nyu_nendo, cdt["cat_cd"], section_cd)
        for dt in sql_data:
            sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
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
