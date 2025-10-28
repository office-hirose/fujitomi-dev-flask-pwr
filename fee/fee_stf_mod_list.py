from _mod_fis import mod_common
from fee import fee_stf_sql_list


# setting, title, data
def mz_list(sheet, row, cf_dic, fdate_int, staff_email, main_sub_gyotei_all):
    sheet.set_paper(9)  # A4 size paper
    sheet.set_tab_color("green")
    sheet.set_row(0, 25)  # height
    sheet.freeze_panes(1, 0)  # 1行目固定

    cf_c10_bor_yellow = cf_dic["cf_c10_bor_yellow"]
    cf_l11_bor = cf_dic["cf_l11_bor"]
    cf_c11_bor = cf_dic["cf_c11_bor"]
    cf_r12_comma = cf_dic["cf_r12_comma"]
    cf_r12_comma_decimal = cf_dic["cf_r12_comma_decimal"]

    col = 0
    sheet.set_column(col, col, 5)
    sheet.write(0, col, "No", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 5)
    sheet.write(0, col, "CAT", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 5)
    sheet.write(0, col, "CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 35)
    sheet.write(0, col, "保険会社", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "証券番号", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 7)
    sheet.write(0, col, "枝番", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険種類", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "払込方法", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "始期", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "満期", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "保険料", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 35)
    sheet.write(0, col, "契約者", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "実収手数料(合計)", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "営業所", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "担当種別", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "担当名", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "提携名", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "分配手数料(％)", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "分配手数料(円)", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "手数料メモ", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "備考", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)  # 入金月
    sheet.write(0, col, "入金月", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)  # section_cd
    sheet.write(0, col, "section_cd", cf_c10_bor_yellow)

    # data ----------------------------------------------------------------------------------------

    # init
    row += 1
    left_number = 0

    # fee data
    sql_data = fee_stf_sql_list.mz_sql_fee_store(fdate_int, staff_email, main_sub_gyotei_all)

    # fee data cnt
    sql_data_cnt = fee_stf_sql_list.mz_sql_fee_store_cnt(fdate_int, staff_email)

    # write
    for dt in sql_data:
        left_number += 1
        sheet.set_row(row, 22)  # height
        sheet.write(row, 0, left_number, cf_c11_bor)
        sheet.write(row, 1, dt["cat_cd"], cf_c11_bor)
        sheet.write(row, 2, dt["coltd_cd"], cf_c11_bor)
        sheet.write(row, 3, dt["coltd_name"], cf_l11_bor)
        sheet.write(row, 4, dt["syoken_cd_main"], cf_c11_bor)
        sheet.write(row, 5, dt["syoken_cd_sub"], cf_c11_bor)
        sheet.write(
            row,
            6,
            mod_common.mz_kind_name_main_sub(dt["cat_cd"], dt["kind_name_main"], dt["kind_name_sub"]),
            cf_c11_bor,
        )
        sheet.write(row, 7, dt["pay_num_name"], cf_c11_bor)
        sheet.write(row, 8, mod_common.mz_num2date_slash(dt["siki_date"]), cf_c11_bor)
        sheet.write(row, 9, mod_common.mz_num2date_slash(dt["manki_date"]), cf_c11_bor)
        sheet.write(row, 10, dt["hoken_ryo"], cf_r12_comma)
        sheet.write(row, 11, mod_common.mz_kei_name_slice20(dt["kei_name"]), cf_l11_bor)
        sheet.write(row, 12, dt["fee_num"], cf_r12_comma)
        sheet.write(row, 13, dt["section_name"], cf_c11_bor)
        sheet.write(row, 14, dt["person_kind_name"], cf_c11_bor)
        sheet.write(row, 15, dt["staff_name"], cf_c11_bor)
        sheet.write(row, 16, dt["gyotei_name"], cf_l11_bor)
        sheet.write(row, 17, dt["pay_fee_per"], cf_r12_comma_decimal)
        sheet.write(row, 18, dt["pay_fee_yen"], cf_r12_comma)
        sheet.write(row, 19, dt["fee_memo"], cf_l11_bor)

        if dt["pay_person_kind"] == "sub":
            sheet.write(
                row,
                20,
                fee_stf_sql_list.mz_main_staff_name(dt["coltd_cd"], dt["syoken_cd_main"], dt["syoken_cd_sub"]),
                cf_l11_bor,
            )
        else:
            sheet.write(row, 20, dt["pay_gyotei_1year_over_name"], cf_l11_bor)

        sheet.write(row, 21, mod_common.mz_keijyo_date_str(dt["nyu_date"]), cf_c11_bor)
        sheet.write(row, 22, dt["section_cd"], cf_c11_bor)
        row += 1
    return sheet, sql_data_cnt
