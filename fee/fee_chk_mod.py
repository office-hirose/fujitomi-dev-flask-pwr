from fee import fee_chk_sql
from _mod_fis import mod_coltd


# title
def mz_title(sheet, cf_dic):
    cf_c10_bor_yellow = cf_dic["cf_c10_bor_yellow"]
    sheet.set_paper(9)  # A4 size paper
    sheet.set_row(0, 25)  # height
    sheet.freeze_panes(1, 0)  # 1行目固定

    col = 0
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "分類CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険会社CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "保険会社名", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "証券番号", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "枝番", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "nttgw_dat_cnt", cf_c10_bor_yellow)

    return sheet


# data
def mz_data(sheet, cf_dic, nyu_date_int):
    cf_l11_bor = cf_dic["cf_l11_bor"]
    cf_c11_bor = cf_dic["cf_c11_bor"]

    # init
    row = 1

    # sql data
    sql_data = fee_chk_sql.mz_fee_chk(nyu_date_int)
    sql_data_cnt = len(sql_data)

    for dt in sql_data:
        # height
        sheet.set_row(row, 25)

        col = 0
        sheet.write(row, col, dt["cat_cd"], cf_c11_bor)

        col += 1
        sheet.write(row, col, dt["coltd_cd"], cf_c11_bor)

        col += 1
        coltd_name = mod_coltd.mz_coltd_name_simple(dt["coltd_cd"])
        sheet.write(row, col, coltd_name, cf_l11_bor)

        col += 1
        sheet.write(row, col, dt["syoken_cd_main"], cf_c11_bor)

        col += 1
        sheet.write(row, col, dt["syoken_cd_sub"], cf_c11_bor)

        # nttgw_dat_cnt check
        nttgw_dat_cnt = fee_chk_sql.mz_fee_chk_nttgw_dat(dt["coltd_cd"], dt["syoken_cd_main"], dt["syoken_cd_sub"])

        col += 1
        sheet.write(row, col, nttgw_dat_cnt, cf_c11_bor)

        row += 1

    return sheet, sql_data_cnt
