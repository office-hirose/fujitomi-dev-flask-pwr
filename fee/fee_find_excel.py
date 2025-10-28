import io
import sys
from flask import request
from _mod import mod_base, mod_datetime
from _mod_fis import mod_xlsxwriter
from fee import fee_find_sql
import xlsxwriter
import urllib.parse


def fee_excel():
    # form data
    jwtg = eval(request.form["jwtg"])

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        create_file = ""
        mime_type = ""
        file_name = ""
    else:
        # form data
        key_list = eval(request.form["fee_excel_key_data"])

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()
        book = xlsxwriter.Workbook(output, {"in_memory": True})

        # リスト作成
        cf_dic = mod_xlsxwriter.mz_cf(book)
        sheet = book.add_worksheet("実収手数料リスト")
        sheet = mz_title(sheet, cf_dic)
        sheet = mz_data(sheet, cf_dic, key_list)

        # close workbook
        book.close()

        # rewind the buffer
        output.seek(0)

        # create excel
        create_file = output.getvalue()
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        file_name_temp = "実収手数料リスト-" + mod_datetime.mz_tnow("for_filename_yyyy_mmdd_hhmm") + ".xlsx"
        file_name = urllib.parse.quote(file_name_temp)

    return create_file, mime_type, file_name


# setting, title
def mz_title(sheet, cf_dic):
    cf_c10_bor_yellow = cf_dic["cf_c10_bor_yellow"]  # format
    sheet.set_paper(9)  # A4 size paper
    sheet.set_row(0, 25)  # height
    sheet.freeze_panes(1, 0)  # 1行目固定

    col = 0
    sheet.set_column(col, col, 5)
    sheet.write(0, col, "No", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "実収入金年月", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "始期日", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "満期日", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "営業所", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 40)
    sheet.write(0, col, "保険会社", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "証券番号", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "枝番", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 60)
    sheet.write(0, col, "契約者名", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "手数料合計", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "払込方法", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "回目", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "種類", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "担当", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "提携", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "手数料配分(率)", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "手数料配分(円)", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 40)
    sheet.write(0, col, "生保提携1年経過など", cf_c10_bor_yellow)

    return sheet


# write data
def mz_data(sheet, cf_dic, key_list):
    sheet.set_row(0, 25)  # height
    # cf_l11_bor = cf_dic["cf_l11_bor"]
    cf_c11_bor = cf_dic["cf_c11_bor"]
    cf_r12_comma = cf_dic["cf_r12_comma"]
    row = 1

    # write sheet
    for fis_cd in key_list:
        # sql
        sql_data = fee_find_sql.excel_sql(fis_cd)
        for dt in sql_data:
            nyu_date = mod_datetime.mz_mum2str_yymmdd_nen_tuki(dt["nyu_date"])
            siki_date = mod_datetime.mz_num2date_hyphen(dt["siki_date"])
            manki_date = mod_datetime.mz_num2date_hyphen(dt["manki_date"])
            section_name = dt["section_name"]

            coltd_name = dt["coltd_name"]
            syoken_cd_main = dt["syoken_cd_main"]
            syoken_cd_sub = dt["syoken_cd_sub"]
            kei_name = dt["kei_name"]

            fee_num = dt["fee_num"]
            pay_num_name = dt["pay_num_name"]
            kaime = dt["kaime"]
            kind_name = dt["kind_name"]

            staff_name = dt["staff_name"]

            gyotei_name = dt["gyotei_name"]
            if gyotei_name is None:
                gyotei_name = ""

            pay_fee_per = str(dt["pay_fee_per"]) + "%"
            pay_fee_yen = dt["pay_fee_yen"]

            pay_gyotei_1year_over_name = dt["pay_gyotei_1year_over_name"]

            # write -----------------------------

            col = 0
            sheet.write(row, col, row, cf_c11_bor)

            col += 1
            sheet.write(row, col, nyu_date, cf_c11_bor)

            col += 1
            sheet.write(row, col, siki_date, cf_c11_bor)

            col += 1
            sheet.write(row, col, manki_date, cf_c11_bor)

            col += 1
            sheet.write(row, col, section_name, cf_c11_bor)

            col += 1
            sheet.write(row, col, coltd_name, cf_c11_bor)

            col += 1
            sheet.write(row, col, syoken_cd_main, cf_c11_bor)

            col += 1
            sheet.write(row, col, syoken_cd_sub, cf_c11_bor)

            col += 1
            sheet.write(row, col, kei_name, cf_c11_bor)

            col += 1
            sheet.write(row, col, fee_num, cf_r12_comma)

            col += 1
            sheet.write(row, col, pay_num_name, cf_c11_bor)

            col += 1
            sheet.write(row, col, kaime, cf_c11_bor)

            col += 1
            sheet.write(row, col, kind_name, cf_c11_bor)

            col += 1
            sheet.write(row, col, staff_name, cf_c11_bor)

            col += 1
            sheet.write(row, col, gyotei_name, cf_c11_bor)

            col += 1
            sheet.write(row, col, pay_fee_per, cf_c11_bor)

            col += 1
            sheet.write(row, col, pay_fee_yen, cf_r12_comma)

            col += 1
            sheet.write(row, col, pay_gyotei_1year_over_name, cf_c11_bor)

        row += 1
    return sheet
