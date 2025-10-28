from fee import (
    fee_total_sql_common,
    fee_total_sql_stf_gol,
    fee_total_sql_stf_rui,
    fee_total_sql_stf_tou,
)


# cell width, height set
def mz_setting_sum(sheet):
    sheet.set_paper(9)  # A4 size paper
    sheet.set_default_row(22)  # height

    sheet.set_column(0, 0, 4)  # NO
    sheet.set_column(1, 1, 25)  # 営業所/担当

    # 当月
    sheet.set_column(2, 2, 15)  # 生保・担当
    sheet.set_column(3, 3, 15)  # 生保・提携
    sheet.set_column(4, 4, 15)  # 損保・担当
    sheet.set_column(5, 5, 15)  # 損保・提携
    sheet.set_column(6, 6, 15)  # 少短・担当
    sheet.set_column(7, 7, 15)  # 少短・提携
    sheet.set_column(8, 8, 15)  # 合計・担当
    sheet.set_column(9, 9, 15)  # 合計・提携
    sheet.set_column(10, 10, 15)  # 総合計

    sheet.set_column(11, 11, 1)  # ブランク

    # 年度累計
    sheet.set_column(12, 12, 15)  # 生保・担当
    sheet.set_column(13, 13, 15)  # 生保・提携
    sheet.set_column(14, 14, 15)  # 損保・担当
    sheet.set_column(15, 15, 15)  # 損保・提携
    sheet.set_column(16, 16, 15)  # 少短・担当
    sheet.set_column(17, 17, 15)  # 少短・提携
    sheet.set_column(18, 18, 15)  # 合計・担当
    sheet.set_column(19, 19, 15)  # 合計・提携
    sheet.set_column(20, 20, 15)  # 総合計

    return sheet


# title
def mz_title_sum(sheet, cf_dic, row, title_name, nyu_nendo_str):
    cf_l14 = cf_dic["cf_l14"]
    cf_l18 = cf_dic["cf_l18"]
    cf_l14_bor = cf_dic["cf_l14_bor"]
    cf_c14_bor = cf_dic["cf_c14_bor"]
    cf_l11_bor_btm = cf_dic["cf_l11_bor_btm"]

    sheet.set_row(row, 40)  # height
    sheet.write(row, 0, title_name, cf_l18)
    sheet.write(row, 4, "※こちらの営業所合計は目安です。「実収手数料_担当別」のシートを参照してください。", cf_l14)
    sheet.write(row, 19, "担当印", cf_l11_bor_btm)
    sheet.write(row, 20, "確認印", cf_l11_bor_btm)

    row += 1
    sheet.set_row(row, 10)  # height
    sheet.write(row, 0, "")  # spacer

    row += 1
    sheet.set_row(row, 22)  # height
    sheet.merge_range(row, 0, row + 2, 0, "No", cf_c14_bor)
    sheet.merge_range(row, 1, row + 2, 1, "営業所/担当", cf_l14_bor)
    sheet.merge_range(row, 2, row, 10, "当月", cf_c14_bor)
    sheet.merge_range(row, 12, row, 20, "年度累計", cf_c14_bor)

    row += 1
    sheet.merge_range(row, 2, row, 3, "生保", cf_c14_bor)
    sheet.merge_range(row, 4, row, 5, "損保", cf_c14_bor)
    sheet.merge_range(row, 6, row, 7, "少短", cf_c14_bor)
    sheet.merge_range(row, 8, row, 9, "合計", cf_c14_bor)
    sheet.merge_range(row, 10, row + 1, 10, "総合計", cf_c14_bor)

    sheet.merge_range(row, 12, row, 13, "生保", cf_c14_bor)
    sheet.merge_range(row, 14, row, 15, "損保", cf_c14_bor)
    sheet.merge_range(row, 16, row, 17, "少短", cf_c14_bor)
    sheet.merge_range(row, 18, row, 19, "合計", cf_c14_bor)
    sheet.merge_range(row, 20, row + 1, 20, "総合計", cf_c14_bor)

    row += 1
    sheet.write(row, 2, "担当", cf_c14_bor)
    sheet.write(row, 3, "提携", cf_c14_bor)
    sheet.write(row, 4, "担当", cf_c14_bor)
    sheet.write(row, 5, "提携", cf_c14_bor)
    sheet.write(row, 6, "担当", cf_c14_bor)
    sheet.write(row, 7, "提携", cf_c14_bor)
    sheet.write(row, 8, "担当", cf_c14_bor)
    sheet.write(row, 9, "提携", cf_c14_bor)

    sheet.write(row, 12, "担当", cf_c14_bor)
    sheet.write(row, 13, "提携", cf_c14_bor)
    sheet.write(row, 14, "担当", cf_c14_bor)
    sheet.write(row, 15, "提携", cf_c14_bor)
    sheet.write(row, 16, "担当", cf_c14_bor)
    sheet.write(row, 17, "提携", cf_c14_bor)
    sheet.write(row, 18, "担当", cf_c14_bor)
    sheet.write(row, 19, "提携", cf_c14_bor)

    return sheet, row


# create data
def mz_data_sum(sheet, cf_dic, row, nyu_date, nyu_nendo):
    cf_l14_bor = cf_dic["cf_l14_bor"]
    cf_c14_bor = cf_dic["cf_c14_bor"]
    cf_r14_comma = cf_dic["cf_r14_comma"]
    cf_l14_bor_top = cf_dic["cf_l14_bor_top"]
    cf_r14_comma_bor_top = cf_dic["cf_r14_comma_bor_top"]

    # ------------------------------------------------------------------------------------------------------
    # 総合計
    # ------------------------------------------------------------------------------------------------------

    cat_data = fee_total_sql_common.mz_sql_cat()
    sec_data = fee_total_sql_common.mz_sql_section()
    start_row = row + 2

    # section name
    row = start_row
    left_number = 1
    for dt in sec_data:
        sheet.write(row, 0, left_number, cf_c14_bor)
        sheet.write(row, 1, dt["section_name"], cf_l14_bor)
        left_number += 1
        row += 1
    sheet.write(row, 0, "", cf_l14_bor_top)
    sheet.write(row, 1, "総合計", cf_l14_bor_top)

    # ------------------------------------
    # 当月（生保・損保・少短）
    # ------------------------------------
    col = 1
    for cdt in cat_data:
        # 担当
        gtotal = 0
        row = start_row
        col += 1
        sql_data = fee_total_sql_stf_gol.mz_tou_tan(nyu_date, cdt["cat_cd"])
        for dt in sql_data:
            sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
            row += 1
            res = mz_gtotal_calc(dt["pay_fee_yen"])
            gtotal += res
        sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

        # 提携
        gtotal = 0
        row = start_row
        col += 1
        sql_data = fee_total_sql_stf_gol.mz_tou_gyo(nyu_date, cdt["cat_cd"])
        for dt in sql_data:
            sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
            row += 1
            res = mz_gtotal_calc(dt["pay_fee_yen"])
            gtotal += res
        sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

    # 担当・合計
    gtotal = 0
    row = start_row
    col += 1
    sql_data = fee_total_sql_stf_gol.mz_tou_tan(nyu_date, "all")
    for dt in sql_data:
        sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
        row += 1
        res = mz_gtotal_calc(dt["pay_fee_yen"])
        gtotal += res
    sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

    # 提携・合計
    gtotal = 0
    row = start_row
    col += 1
    sql_data = fee_total_sql_stf_gol.mz_tou_gyo(nyu_date, "all")
    for dt in sql_data:
        sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
        row += 1
        res = mz_gtotal_calc(dt["pay_fee_yen"])
        gtotal += res
    sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

    # 総合計
    gtotal = 0
    row = start_row
    col += 1
    sql_data = fee_total_sql_stf_gol.mz_tou_total(nyu_date)
    for dt in sql_data:
        sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
        row += 1
        res = mz_gtotal_calc(dt["pay_fee_yen"])
        gtotal += res
    sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

    # ------------------------------------
    # 累計（生保・損保・少短）
    # ------------------------------------
    col = 11
    for cdt in cat_data:
        # 担当
        gtotal = 0
        row = start_row
        col += 1
        sql_data = fee_total_sql_stf_gol.mz_rui_tan(nyu_date, nyu_nendo, cdt["cat_cd"])
        for dt in sql_data:
            sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
            row += 1
            res = mz_gtotal_calc(dt["pay_fee_yen"])
            gtotal += res
        sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

        # 提携
        gtotal = 0
        row = start_row
        col += 1
        sql_data = fee_total_sql_stf_gol.mz_rui_gyo(nyu_date, nyu_nendo, cdt["cat_cd"])
        for dt in sql_data:
            sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
            row += 1
            res = mz_gtotal_calc(dt["pay_fee_yen"])
            gtotal += res
        sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

    # 担当・合計
    gtotal = 0
    row = start_row
    col += 1
    sql_data = fee_total_sql_stf_gol.mz_rui_tan(nyu_date, nyu_nendo, "all")
    for dt in sql_data:
        sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
        row += 1
        res = mz_gtotal_calc(dt["pay_fee_yen"])
        gtotal += res
    sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

    # 提携・合計
    gtotal = 0
    row = start_row
    col += 1
    sql_data = fee_total_sql_stf_gol.mz_rui_gyo(nyu_date, nyu_nendo, "all")
    for dt in sql_data:
        sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
        row += 1
        res = mz_gtotal_calc(dt["pay_fee_yen"])
        gtotal += res
    sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

    # 総合計
    gtotal = 0
    row = start_row
    col += 1
    sql_data = fee_total_sql_stf_gol.mz_rui_total(nyu_date, nyu_nendo)
    for dt in sql_data:
        sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
        row += 1
        res = mz_gtotal_calc(dt["pay_fee_yen"])
        gtotal += res
    sheet.write(row, col, gtotal, cf_r14_comma_bor_top)

    # ------------------------------------------------------------------------------------------------------
    # 担当別リスト
    # ------------------------------------------------------------------------------------------------------

    # init
    start_row = row + 2

    # 担当者名
    row = start_row
    for sdt in sec_data:
        left_number = 1
        sql_data = fee_total_sql_common.mz_staff_data(sdt["section_cd"])
        for dt in sql_data:
            sheet.write(row, 0, left_number, cf_c14_bor)
            sheet.write(row, 1, dt["name_simple"], cf_l14_bor)
            left_number += 1
            row += 1
        row += 1

    # ------------------------------------
    # 当月（生保・損保・少短）
    # ------------------------------------
    col = 1
    for cdt in cat_data:
        # 担当
        row = start_row
        col += 1
        for sdt in sec_data:
            sql_data = fee_total_sql_stf_tou.mz_tou_tan(nyu_date, cdt["cat_cd"], sdt["section_cd"])
            for dt in sql_data:
                sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
                row += 1
            row += 1

        # 提携
        row = start_row
        col += 1
        for sdt in sec_data:
            sql_data = fee_total_sql_stf_tou.mz_tou_gyo(nyu_date, cdt["cat_cd"], sdt["section_cd"])
            for dt in sql_data:
                sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
                row += 1
            row += 1

    # 担当・合計
    row = start_row
    col += 1
    for sdt in sec_data:
        sql_data = fee_total_sql_stf_tou.mz_tou_tan(nyu_date, "all", sdt["section_cd"])
        for dt in sql_data:
            sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
            row += 1
        row += 1

    # 提携・合計
    row = start_row
    col += 1
    for sdt in sec_data:
        sql_data = fee_total_sql_stf_tou.mz_tou_gyo(nyu_date, "all", sdt["section_cd"])
        for dt in sql_data:
            sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
            row += 1
        row += 1

    # 総合計
    row = start_row
    col += 1
    for sdt in sec_data:
        sql_data = fee_total_sql_stf_tou.mz_tou_total(nyu_date, sdt["section_cd"])
        for dt in sql_data:
            sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
            row += 1
        row += 1

    # ------------------------------------
    # 累計（生保・損保・少短）
    # ------------------------------------
    col = 11
    for cdt in cat_data:
        # 担当
        row = start_row
        col += 1
        for sdt in sec_data:
            sql_data = fee_total_sql_stf_rui.mz_rui_tan(nyu_date, nyu_nendo, cdt["cat_cd"], sdt["section_cd"])
            for dt in sql_data:
                sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
                row += 1
            row += 1

        # 提携
        row = start_row
        col += 1
        for sdt in sec_data:
            sql_data = fee_total_sql_stf_rui.mz_rui_gyo(nyu_date, nyu_nendo, cdt["cat_cd"], sdt["section_cd"])
            for dt in sql_data:
                sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
                row += 1
            row += 1

    # 担当・合計
    row = start_row
    col += 1
    for sdt in sec_data:
        sql_data = fee_total_sql_stf_rui.mz_rui_tan(nyu_date, nyu_nendo, "all", sdt["section_cd"])
        for dt in sql_data:
            sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
            row += 1
        row += 1

    # 提携・合計
    row = start_row
    col += 1
    for sdt in sec_data:
        sql_data = fee_total_sql_stf_rui.mz_rui_gyo(nyu_date, nyu_nendo, "all", sdt["section_cd"])
        for dt in sql_data:
            sheet.write(row, col, dt["pay_fee_yen"], cf_r14_comma)
            row += 1
        row += 1

    # 総合計
    row = start_row
    col += 1
    for sdt in sec_data:
        sql_data = fee_total_sql_stf_rui.mz_rui_total(nyu_date, nyu_nendo, sdt["section_cd"])
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
