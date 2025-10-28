import io
import sys
from flask import request
from _mod import mod_base, mod_datetime
from _mod_fis import mod_xlsxwriter, mod_common
from store import store_sql
import xlsxwriter
import urllib.parse


def store_excel():
    # form data
    jwtg = eval(request.form["jwtg"])
    key_list = eval(request.form["store_excel_key_data"])

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        create_file = ""
        mime_type = ""
        file_name = ""
    else:
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()
        book = xlsxwriter.Workbook(output, {"in_memory": True})

        # リスト作成
        cf_dic = mod_xlsxwriter.mz_cf(book)
        sheet = book.add_worksheet("契約リスト")
        sheet = mz_title(sheet, cf_dic)
        sheet = mz_data(sheet, cf_dic, key_list)

        # close workbook
        book.close()

        # rewind the buffer
        output.seek(0)

        # create excel
        create_file = output.getvalue()
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        file_name_temp = "契約リスト-" + mod_datetime.mz_tnow("for_filename_yyyy_mmdd_hhmm") + ".xlsx"
        file_name = urllib.parse.quote(file_name_temp)

        # base - level 2 - access log only
        acc_page_name = sys._getframe().f_code.co_name
        mod_base.mz_base(2, jwtg, acc_page_name)

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
    sheet.write(0, col, "契約状況", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "始期日", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "満期日", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "異動解約日", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "証券番号", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "枝番", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "旧証券番号", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "旧枝番", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "申込番号", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "営業所", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "社内計上月", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 40)
    sheet.write(0, col, "保険会社", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "保険種目", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "保険種類", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 60)
    sheet.write(0, col, "契約者名", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 40)
    sheet.write(0, col, "メモ", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "払込方法", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "保険料", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "保険料年換算", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "異動/解約/保険料", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "担当1", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "担当2", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "担当3", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "提携1", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "提携2", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "提携3", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "担当1(％)", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "担当2(％)", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "担当3(％)", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "提携1(％)", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "提携2(％)", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "提携3(％)", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "[少短]手数料率", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "[生保]継続手数料支払年数", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "[生保]初年度手数料(円)", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 40)
    sheet.write(0, col, "[生保]継続手数料(円)次年度以降の年間手数料", cf_c10_bor_yellow)
    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "FIS_CD", cf_c10_bor_yellow)
    return sheet


# write data
def mz_data(sheet, cf_dic, key_list):
    sheet.set_row(0, 25)  # height
    cf_l11_bor = cf_dic["cf_l11_bor"]
    cf_c11_bor = cf_dic["cf_c11_bor"]
    cf_r12_comma = cf_dic["cf_r12_comma"]
    row = 1

    # write sheet
    for fis_cd in key_list:
        # sql
        sql_data = store_sql.excel_sql(fis_cd)
        for dt in sql_data:
            keiyaku_name = dt["keiyaku_name"]  # 契約状況
            siki_date = str(dt["siki_date"])  # 始期、満期、異動解約日
            manki_date = str(dt["manki_date"])
            ido_kai_date = str(dt["ido_kai_date"])
            syoken_cd_main = dt["syoken_cd_main"]  # 証券番号
            syoken_cd_sub = dt["syoken_cd_sub"]  # 証券番号(枝番)
            old_syoken_cd_main = dt["old_syoken_cd_main"]  # 旧証券番号
            old_syoken_cd_sub = dt["old_syoken_cd_sub"]  # 旧証券番号(枝番)
            mosikomi_cd = dt["mosikomi_cd"]  # 申込番号
            section_name = dt["section_name"]  # 営業所
            keijyo_date_str = mod_common.mz_keijyo_date_str(dt["keijyo_date"])  # 計上年月
            coltd_name_simple = dt["coltd_name"]  # 保険会社
            kind_name_main = dt["kind_name_main"]  # 保険種類main
            kind_name_sub = dt["kind_name_sub"]  # 保険種類sub
            kei_name = dt["kei_name"]  # 契約者名
            memo = dt["memo"]  # メモ
            pay_num_name = dt["pay_num_name"]  # 払込方法
            hoken_ryo = str(dt["hoken_ryo"])  # 保険料
            hoken_ryo_year = str(dt["hoken_ryo_year"])  # 保険料年換算
            ido_kai_hoken_ryo = str(dt["ido_kai_hoken_ryo"])  # 異動/解約/保険料
            staff1_name_simple = dt["staff1_name"]  # 担当、業務提携
            staff2_name_simple = dt["staff2_name"]
            staff3_name_simple = dt["staff3_name"]
            gyotei1_name = dt["gyotei1_name"]
            gyotei2_name = dt["gyotei2_name"]
            gyotei3_name = dt["gyotei3_name"]
            fee_staff1 = str(dt["fee_staff1"])
            fee_staff2 = str(dt["fee_staff2"])
            fee_staff3 = str(dt["fee_staff3"])
            fee_gyotei1 = str(dt["fee_gyotei1"])
            fee_gyotei2 = str(dt["fee_gyotei2"])
            fee_gyotei3 = str(dt["fee_gyotei3"])
            fee_ritu_str = str(dt["fee_ritu"]) + "％"  # 少額短期・損保手数料
            fee_seiho_kikan = str(dt["fee_seiho_kikan"])  # 生保手数料
            fee_seiho_first = str(dt["fee_seiho_first"])
            fee_seiho_next = str(dt["fee_seiho_next"])
            fis_cd = str(dt["fis_cd"])  # fis CD
            col = 0
            sheet.write(row, col, row, cf_c11_bor)
            col += 1
            sheet.write(row, col, keiyaku_name, cf_c11_bor)
            col += 1
            sheet.write(row, col, siki_date, cf_c11_bor)
            col += 1
            sheet.write(row, col, manki_date, cf_c11_bor)
            col += 1
            sheet.write(row, col, ido_kai_date, cf_c11_bor)
            col += 1
            sheet.write(row, col, syoken_cd_main, cf_c11_bor)
            col += 1
            sheet.write(row, col, syoken_cd_sub, cf_c11_bor)
            col += 1
            sheet.write(row, col, old_syoken_cd_main, cf_c11_bor)
            col += 1
            sheet.write(row, col, old_syoken_cd_sub, cf_c11_bor)
            col += 1
            sheet.write(row, col, mosikomi_cd, cf_c11_bor)
            col += 1
            sheet.write(row, col, section_name, cf_c11_bor)
            col += 1
            sheet.write(row, col, keijyo_date_str, cf_c11_bor)
            col += 1
            sheet.write(row, col, coltd_name_simple, cf_c11_bor)
            col += 1
            sheet.write(row, col, kind_name_main, cf_c11_bor)
            col += 1
            sheet.write(row, col, kind_name_sub, cf_c11_bor)
            col += 1
            sheet.write(row, col, kei_name, cf_l11_bor)
            col += 1
            sheet.write(row, col, memo, cf_l11_bor)
            col += 1
            sheet.write(row, col, pay_num_name, cf_c11_bor)
            col += 1
            sheet.write(row, col, hoken_ryo, cf_r12_comma)
            col += 1
            sheet.write(row, col, hoken_ryo_year, cf_r12_comma)
            col += 1
            sheet.write(row, col, ido_kai_hoken_ryo, cf_r12_comma)
            col += 1
            sheet.write(row, col, staff1_name_simple, cf_c11_bor)
            col += 1
            sheet.write(row, col, staff2_name_simple, cf_c11_bor)
            col += 1
            sheet.write(row, col, staff3_name_simple, cf_c11_bor)
            col += 1
            sheet.write(row, col, gyotei1_name, cf_c11_bor)
            col += 1
            sheet.write(row, col, gyotei2_name, cf_c11_bor)
            col += 1
            sheet.write(row, col, gyotei3_name, cf_c11_bor)
            col += 1
            sheet.write(row, col, fee_staff1, cf_c11_bor)
            col += 1
            sheet.write(row, col, fee_staff2, cf_c11_bor)
            col += 1
            sheet.write(row, col, fee_staff3, cf_c11_bor)
            col += 1
            sheet.write(row, col, fee_gyotei1, cf_c11_bor)
            col += 1
            sheet.write(row, col, fee_gyotei2, cf_c11_bor)
            col += 1
            sheet.write(row, col, fee_gyotei3, cf_c11_bor)
            col += 1
            sheet.write(row, col, fee_ritu_str, cf_c11_bor)
            col += 1
            sheet.write(row, col, fee_seiho_kikan, cf_c11_bor)
            col += 1
            sheet.write(row, col, fee_seiho_first, cf_r12_comma)
            col += 1
            sheet.write(row, col, fee_seiho_next, cf_r12_comma)
            col += 1
            sheet.write(row, col, fis_cd, cf_c11_bor)
        row += 1
    return sheet
