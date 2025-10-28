from salary import salary_excel_sql_nendo_section


# title
def mz_title(sheet, row, cf_dic):
    cf_c10_bor = cf_dic["cf_c10_bor"]

    col = 1
    sheet.set_column(col, col, 20)
    sheet.write(row, col, "セクション", cf_c10_bor)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(row, col, "①手数料税抜", cf_c10_bor)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(row, col, "②固定月額(累計)", cf_c10_bor)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(row, col, "支払率", cf_c10_bor)

    col += 1
    sheet.set_column(col, col, 18)
    sheet.write(row, col, "③成績比例分税抜", cf_c10_bor)

    col += 1
    sheet.set_column(col, col, 13)
    sheet.write(row, col, "④消費税", cf_c10_bor)

    col += 1
    sheet.set_column(col, col, 13)
    sheet.write(row, col, "⑤消費税×0.2", cf_c10_bor)

    col += 1
    sheet.set_column(col, col, 23)
    sheet.write(row, col, "⑥合計額(②+③+⑤)", cf_c10_bor)

    col += 1
    sheet.set_column(col, col, 23)
    sheet.write(row, col, "⑦手数料との差額(①-⑥)", cf_c10_bor)

    return sheet, row


# data write
def mz_data(
    sheet,
    row,
    cf_dic,
    salary_date_int,
    nendo,
):
    # format
    cf_l12_bor = cf_dic["cf_l12_bor"]
    cf_c12_bor = cf_dic["cf_c12_bor"]
    cf_r12_comma_bor = cf_dic["cf_r12_comma_bor"]
    cf_l12_bor_top = cf_dic["cf_l12_bor_top"]
    cf_r12_comma_bor_top = cf_dic["cf_r12_comma_bor_top"]

    # init
    row += 1
    total_fee_no_tax = 0
    total_fee_kotei = 0
    total_fee_hirei_no_tax = 0
    total_fee_hirei_tax = 0
    total_fee_hirei_tax_20 = 0
    total_fee_total = 0
    total_fee_total_sagaku = 0

    # sql_data
    sql_data_cnt = 0
    sql_data = salary_excel_sql_nendo_section.mz_sql_salary_store(salary_date_int, nendo)
    sql_data_cnt = len(sql_data)

    for dt in sql_data:

        # section_name
        section_name = salary_excel_sql_nendo_section.mz_sql_section_name(dt["staff_section_cd"])

        col = 1
        sheet.write(row, col, section_name, cf_l12_bor)

        col += 1
        sheet.write(row, col, dt["fee_no_tax"], cf_r12_comma_bor)

        col += 1
        sheet.write(row, col, dt["fee_kotei"], cf_r12_comma_bor)

        col += 1
        sheet.write(row, col, "", cf_c12_bor)

        col += 1
        sheet.write(row, col, dt["fee_hirei_no_tax"], cf_r12_comma_bor)

        col += 1
        sheet.write(row, col, dt["fee_hirei_tax"], cf_r12_comma_bor)

        col += 1
        sheet.write(row, col, dt["fee_hirei_tax_20"], cf_r12_comma_bor)

        col += 1
        sheet.write(row, col, dt["fee_total"], cf_r12_comma_bor)

        col += 1
        sheet.write(row, col, dt["fee_total_sagaku"], cf_r12_comma_bor)

        row += 1

        total_fee_no_tax += dt["fee_no_tax"]
        total_fee_kotei += dt["fee_kotei"]
        total_fee_hirei_no_tax += dt["fee_hirei_no_tax"]
        total_fee_hirei_tax += dt["fee_hirei_tax"]
        total_fee_hirei_tax_20 += dt["fee_hirei_tax_20"]
        total_fee_total += dt["fee_total"]
        total_fee_total_sagaku += dt["fee_total_sagaku"]

    # 合計
    col = 1
    sheet.write(row, col, "合計", cf_l12_bor_top)

    col += 1
    sheet.write(row, col, total_fee_no_tax, cf_r12_comma_bor_top)

    col += 1
    sheet.write(row, col, total_fee_kotei, cf_r12_comma_bor_top)

    col += 1
    sheet.write(row, col, "", cf_r12_comma_bor_top)

    col += 1
    sheet.write(row, col, total_fee_hirei_no_tax, cf_r12_comma_bor_top)

    col += 1
    sheet.write(row, col, total_fee_hirei_tax, cf_r12_comma_bor_top)

    col += 1
    sheet.write(row, col, total_fee_hirei_tax_20, cf_r12_comma_bor_top)

    col += 1
    sheet.write(row, col, total_fee_total, cf_r12_comma_bor_top)

    col += 1
    sheet.write(row, col, total_fee_total_sagaku, cf_r12_comma_bor_top)

    return sheet, row, sql_data_cnt
