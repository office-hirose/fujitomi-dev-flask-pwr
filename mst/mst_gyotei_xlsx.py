from _mod_fis import mod_gyotei


# setting, title
def mz_title(sheet, cf_dic):
    # A4 size paper
    sheet.set_paper(9)

    # format
    cf_c10_bor_yellow = cf_dic["cf_c10_bor_yellow"]

    # height
    sheet.set_default_row(25)

    # 1行目固定
    sheet.freeze_panes(1, 0)

    col = -1

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "契約状況", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "営業所", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "管理CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 50)
    sheet.write(0, col, "提携者名", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "提携[率]", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "担当1[率]", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "担当1", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "生保支払年数", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "控除金額", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "源泉ありなし", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "振込銀行名", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "振込銀行支店名", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "振込口座種別", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "振込口座番号", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 50)
    sheet.write(0, col, "振込名義", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 50)
    sheet.write(0, col, "メモ", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "gyotei_cd", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "インボイス登録", cf_c10_bor_yellow)

    return sheet


# write xls
def mz_data(sheet, sta_cd, cf_dic):
    # format
    cf_left_bor = cf_dic["cf_l10_bor"]
    cf_center_bor = cf_dic["cf_c10_bor"]

    # init
    row_cnt = 1

    # sql_data
    sql_data = mod_gyotei.mz_gyotei_data_xlsx(sta_cd)

    # write
    for dt in sql_data:
        sheet.write(row_cnt, 0, dt["onoff_name"], cf_center_bor)
        sheet.write(row_cnt, 1, dt["section_name"], cf_center_bor)
        sheet.write(row_cnt, 2, dt["kanri_cd"], cf_center_bor)
        sheet.write(row_cnt, 3, dt["name"], cf_left_bor)
        sheet.write(row_cnt, 4, dt["fee_gyotei"], cf_center_bor)
        sheet.write(row_cnt, 5, dt["fee_staff1"], cf_center_bor)
        sheet.write(row_cnt, 6, dt["staff_name"], cf_center_bor)
        sheet.write(row_cnt, 7, dt["pay_kikan"], cf_center_bor)
        sheet.write(row_cnt, 8, dt["kojo_fee"], cf_center_bor)
        sheet.write(row_cnt, 9, dt["gensen_name"], cf_center_bor)
        sheet.write(row_cnt, 10, dt["bank_name"], cf_left_bor)
        sheet.write(row_cnt, 11, dt["bank_branch"], cf_left_bor)
        sheet.write(row_cnt, 12, dt["bank_kind"], cf_center_bor)
        sheet.write(row_cnt, 13, dt["bank_account"], cf_center_bor)
        sheet.write(row_cnt, 14, dt["bank_account_name"], cf_left_bor)
        sheet.write(row_cnt, 15, dt["memo"], cf_left_bor)
        sheet.write(row_cnt, 16, dt["gyotei_cd"], cf_center_bor)
        sheet.write(row_cnt, 17, dt["invoice_sta_name"], cf_center_bor)
        row_cnt += 1
    return sheet
