from salary import salary_excel_sql_month_staff


# title
def mz_title(sheet, row, cf_dic):
    cf_c10_bor = cf_dic["cf_c10_bor"]

    col = 0
    sheet.set_column(col, col, 15)
    sheet.write(row, col, "種別", cf_c10_bor)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(row, col, "担当", cf_c10_bor)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(row, col, "①手数料税抜", cf_c10_bor)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(row, col, "②固定月額", cf_c10_bor)

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
):
    # format
    cf_l12_bor = cf_dic["cf_l12_bor"]
    cf_c12_bor = cf_dic["cf_c12_bor"]
    cf_r12_comma_bor = cf_dic["cf_r12_comma_bor"]

    # init
    row += 1

    # sql_data
    sql_data_cnt = 0
    sql_data = salary_excel_sql_month_staff.mz_sql_salary_store(salary_date_int)
    sql_data_cnt = len(sql_data)

    # write
    prev_section_cd = None  # 前回のセクションコードを保持

    for dt in sql_data:

        # セクションコードが変わった場合、1行空白を挿入
        if prev_section_cd is not None and prev_section_cd != dt["staff_section_cd"]:
            row += 1  # 1行空白を開ける

        prev_section_cd = dt["staff_section_cd"]  # 現在のセクションコードを保存

        salary_kind_name = salary_excel_sql_month_staff.mz_sql_salary_kind_name(dt["salary_kind_cd"])
        # section_name = salary_excel_sql.mz_sql_section_name(dt["staff_section_cd"])

        col = 0
        sheet.write(row, col, salary_kind_name, cf_l12_bor)

        col += 1
        sheet.write(row, col, dt["staff_name"], cf_l12_bor)

        col += 1
        sheet.write(row, col, dt["fee_no_tax"], cf_r12_comma_bor)

        col += 1
        sheet.write(row, col, dt["fee_kotei"], cf_r12_comma_bor)

        col += 1
        sheet.write(row, col, str(dt["fee_pay_ritu"]) + "%", cf_c12_bor)

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

    return sheet, row, sql_data_cnt
