from fee_import import fee_hikaku_sql_list


# title
def mz_title(sheet, cf_dic):
    # A4 size paper
    sheet.set_paper(9)

    # 1行目固定
    sheet.freeze_panes(1, 0)

    # height
    sheet.set_default_row(25)

    # format
    cf_c10_bor_yellow = cf_dic["cf_c10_bor_yellow"]

    col = 0
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "保険会社CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "保険会社名", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "確定/notax", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "データ/notax", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "調整", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "差異", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "件数", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "経理用/notax", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "経理用/withtax", cf_c10_bor_yellow)

    return sheet


# data
def mz_data(sheet, cf_dic, nyu_date_int, nyu_date_str):
    # format
    cf_l10_bor = cf_dic["cf_l10_bor"]
    cf_c10_bor = cf_dic["cf_c10_bor"]
    cf_l12_bor = cf_dic["cf_l12_bor"]
    cf_r12_comma_bor = cf_dic["cf_r12_comma_bor"]
    # cf_r14_comma_bor = cf_dic["cf_r14_comma_bor"]

    # init
    row_cnt = 1

    # list
    fee_data = fee_hikaku_sql_list.mz_list(nyu_date_int)

    # list total
    # (
    #     fk_total,
    #     fs_total,
    #     bal_total,
    #     sai_total,
    #     fk_total_keiri_notax,
    #     fk_total_keiri_withtax,
    # ) = fee_hikaku_sql_list.mz_total(nyu_date_int)

    # write list
    for dt in fee_data:
        sheet.write(row_cnt, 0, dt["coltd_cd"], cf_c10_bor)
        sheet.write(row_cnt, 1, dt["coltd_name"], cf_l10_bor)
        sheet.write(row_cnt, 2, dt["fk_notax"], cf_r12_comma_bor)
        sheet.write(row_cnt, 3, dt["fs_notax"], cf_r12_comma_bor)
        sheet.write(row_cnt, 4, dt["bal_notax"], cf_r12_comma_bor)
        sheet.write(row_cnt, 5, dt["sai_notax"], cf_r12_comma_bor)
        sheet.write(row_cnt, 6, dt["cnt"], cf_r12_comma_bor)
        sheet.write(row_cnt, 7, dt["fk_keiri_notax"], cf_r12_comma_bor)
        sheet.write(row_cnt, 8, dt["fk_keiri_withtax"], cf_r12_comma_bor)
        row_cnt += 1

    # write total
    sheet.write(row_cnt, 0, "", cf_l12_bor)
    sheet.write(row_cnt, 1, nyu_date_str + " 合計", cf_l12_bor)
    # sheet.write(row_cnt, 2, fk_total, cf_r14_comma_bor)
    # sheet.write(row_cnt, 3, fs_total, cf_r14_comma_bor)
    # sheet.write(row_cnt, 4, bal_total, cf_r14_comma_bor)
    # sheet.write(row_cnt, 5, sai_total, cf_r14_comma_bor)
    # sheet.write(row_cnt, 6, "", cf_r14_comma_bor)
    # sheet.write(row_cnt, 7, fk_total_keiri_notax, cf_r14_comma_bor)
    # sheet.write(row_cnt, 8, fk_total_keiri_withtax, cf_r14_comma_bor)

    return sheet
