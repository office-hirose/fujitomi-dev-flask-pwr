from fee import fee_stf_sql_common


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
    sheet.set_tab_color("blue")
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
    start_row = row + 2

    # G2.分野別合計・当月・件数
    row = start_row
    left_number = 1
    for dt in cat_data:
        sheet.write(row, 0, left_number, cf_c11_bor)
        sheet.write(row, 1, dt["cat_cd"], cf_c11_bor)
        sheet.write(row, 2, dt["cat_name"], cf_l11_bor)
        sheet.write(
            row,
            3,
            "=COUNTIF(INDIRECT(" + '"' + "リスト主担当!B:B" + '"' + ")" + "," + dt["cat_cd"] + ")",
            cf_r12_comma,
        )
        left_number += 1
        row += 1

    # G3.分野別合計・当月・手数料・主担当
    row = start_row
    for dt in cat_data:
        sheet.write(
            row,
            4,
            "=SUMIF(INDIRECT("
            + '"'
            + "リスト主担当!B:B"
            + '"'
            + ")"
            + ", "
            + dt["cat_cd"]
            + ", INDIRECT("
            + '"'
            + "リスト主担当!S:S"
            + '"'
            + "))",
            cf_r12_comma,
        )
        row += 1

    # G4.分野別合計・当月・手数料・副担当
    row = start_row
    for dt in cat_data:
        sheet.write(
            row,
            5,
            "=SUMIF(INDIRECT("
            + '"'
            + "リスト副担当!B:B"
            + '"'
            + ")"
            + ", "
            + dt["cat_cd"]
            + ", INDIRECT("
            + '"'
            + "リスト副担当!S:S"
            + '"'
            + "))",
            cf_r12_comma,
        )
        row += 1

    # G5.分野別合計・当月・手数料・担当合計
    row = start_row
    calc = ""
    calc_row = 5
    for dt in cat_data:
        calc = "=E" + str(calc_row) + "+F" + str(calc_row)
        sheet.write(
            row,
            6,
            calc,
            cf_r12_comma,
        )
        calc_row += 1
        row += 1

    # G6.分野別合計・当月・手数料・提携
    row = start_row
    for dt in cat_data:
        sheet.write(
            row,
            7,
            "=SUMIF(INDIRECT("
            + '"'
            + "リスト提携!B:B"
            + '"'
            + ")"
            + ", "
            + dt["cat_cd"]
            + ", INDIRECT("
            + '"'
            + "リスト提携!S:S"
            + '"'
            + "))",
            cf_r12_comma,
        )
        row += 1

    # G7.分野別合計・当月・手数料・総合計
    row = start_row
    calc = ""
    calc_row = 5
    for dt in cat_data:
        calc = "=G" + str(calc_row) + "+H" + str(calc_row)
        sheet.write(
            row,
            8,
            calc,
            cf_r12_comma,
        )
        calc_row += 1
        row += 1

    # S1.分野別合計・当月・件数
    sheet.write(row, 0, "", cf_l11_bor_top)
    sheet.write(row, 1, "", cf_l11_bor_top)
    sheet.write(row, 2, "総合計", cf_l11_bor_top)
    sheet.write(row, 3, "=SUM(D5:D7)", cf_r14_comma_bor_top)

    # S3.分野別合計・当月・手数料・主担当
    sheet.write(row, 4, "=SUM(E5:E7)", cf_r14_comma_bor_top)

    # S4.分野別合計・当月・手数料・副担当
    sheet.write(row, 5, "=SUM(F5:F7)", cf_r14_comma_bor_top)

    # S5.分野別合計・当月・手数料・担当合計
    sheet.write(row, 6, "=SUM(G5:G7)", cf_r14_comma_bor_top)

    # S6.分野別合計・当月・手数料・提携
    sheet.write(row, 7, "=SUM(H5:H7)", cf_r14_comma_bor_top)

    # S7.分野別合計・当月・手数料・総合計
    sheet.write(row, 8, "=SUM(I5:I7)", cf_r14_comma_bor_top)

    # ---------------------------------------------------
    # 保険会社別
    # ---------------------------------------------------

    # init
    start_row = row + 2

    # L2.当月・件数
    row = start_row
    calc = ""
    calc_row = row + 1
    for cdt in cat_data:
        left_number = 1
        sql_data = fee_stf_sql_common.mz_sql_coltd(cdt["cat_cd"])
        for dt in sql_data:
            calc = "B" + str(calc_row)
            sheet.write(row, 0, left_number, cf_c11_bor)
            sheet.write(row, 1, dt["coltd_cd"], cf_c11_bor)
            sheet.write(row, 2, dt["name_simple"], cf_l11_bor)
            sheet.write(
                row,
                3,
                "=COUNTIF(INDIRECT(" + '"' + "リスト主担当!C:C" + '"' + ")" + "," + calc + ")",
                cf_r12_comma,
            )
            left_number += 1
            calc_row += 1
            row += 1

        calc_row += 1
        row += 1

    # L3.当月・手数料・主担当
    row = start_row
    calc = ""
    calc_row = row + 1
    for cdt in cat_data:
        sql_data = fee_stf_sql_common.mz_sql_coltd(cdt["cat_cd"])
        for dt in sql_data:
            calc = "B" + str(calc_row)
            sheet.write(
                row,
                4,
                "=SUMIF(INDIRECT("
                + '"'
                + "リスト主担当!C:C"
                + '"'
                + ")"
                + ", "
                + calc
                + ", INDIRECT("
                + '"'
                + "リスト主担当!S:S"
                + '"'
                + "))",
                cf_r12_comma,
            )
            calc_row += 1
            row += 1
        calc_row += 1
        row += 1

    # L4.当月・手数料・副担当
    row = start_row
    calc = ""
    calc_row = row + 1
    for cdt in cat_data:
        sql_data = fee_stf_sql_common.mz_sql_coltd(cdt["cat_cd"])
        for dt in sql_data:
            calc = "B" + str(calc_row)
            sheet.write(
                row,
                5,
                "=SUMIF(INDIRECT("
                + '"'
                + "リスト副担当!C:C"
                + '"'
                + ")"
                + ", "
                + calc
                + ", INDIRECT("
                + '"'
                + "リスト副担当!S:S"
                + '"'
                + "))",
                cf_r12_comma,
            )
            calc_row += 1
            row += 1
        calc_row += 1
        row += 1

    # L5.当月・手数料・担当合計
    row = start_row
    calc = ""
    calc_row = row + 1
    for cdt in cat_data:
        sql_data = fee_stf_sql_common.mz_sql_coltd(cdt["cat_cd"])
        for dt in sql_data:
            calc = "=E" + str(calc_row) + "+F" + str(calc_row)
            sheet.write(
                row,
                6,
                calc,
                cf_r12_comma,
            )
            calc_row += 1
            row += 1
        calc_row += 1
        row += 1

    # L6.当月・手数料・提携
    row = start_row
    calc = ""
    calc_row = row + 1
    for cdt in cat_data:
        sql_data = fee_stf_sql_common.mz_sql_coltd(cdt["cat_cd"])
        for dt in sql_data:
            calc = "B" + str(calc_row)
            sheet.write(
                row,
                7,
                "=SUMIF(INDIRECT("
                + '"'
                + "リスト提携!C:C"
                + '"'
                + ")"
                + ", "
                + calc
                + ", INDIRECT("
                + '"'
                + "リスト提携!S:S"
                + '"'
                + "))",
                cf_r12_comma,
            )
            calc_row += 1
            row += 1
        calc_row += 1
        row += 1

    # L7.当月・手数料・総合計
    row = start_row
    calc = ""
    calc_row = row + 1
    for cdt in cat_data:
        sql_data = fee_stf_sql_common.mz_sql_coltd(cdt["cat_cd"])
        for dt in sql_data:
            calc = "=G" + str(calc_row) + "+H" + str(calc_row)
            sheet.write(
                row,
                8,
                calc,
                cf_r12_comma,
            )
            calc_row += 1
            row += 1
        calc_row += 1
        row += 1

    return sheet, row
