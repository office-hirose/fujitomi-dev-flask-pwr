# from python._mod_fis import mod_common
from keijyo import keijyo_list_all_sql


# setting, title
def mz_title(sheet, row, cf_dic):
    cf_c10_bor_yellow = cf_dic["cf_c10_bor_yellow"]  # format
    sheet.set_paper(9)  # A4 size paper
    sheet.set_default_row(25)  # height
    sheet.freeze_panes(1, 0)  # 1行目固定

    col = 0
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "営業所CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "営業所名", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険分野CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険分野", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "契約状況CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "契約状況", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "申込番号", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "証券番号main", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "証券番号sub", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "旧証券番号main", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "旧証券番号sub", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険会社CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険会社", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "種目CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "種目名", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "種類CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "社内計上年月", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "始期年月日", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "満期年月日", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "異動解約日", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険期間CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険期間", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "払込方法CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "払込方法", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "年間支払回数", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "払込金額", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "払込金額_年換算", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "異動解約保険料", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "担当1", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "担当2", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "担当3", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "提携1", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "提携2", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "提携3", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "担当1配分", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "担当2配分", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "担当3配分", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "提携1配分", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "提携2配分", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "提携3配分", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "損保手数料率円", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "損保手数料率", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "損保手数料金額", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "手数料cd_all", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "生保継続手数料支払年数", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "生保初年度手数料", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "生保継続手数料", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "法人個人CD", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "契約者氏名漢字", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "契約者氏名ひらがな", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "契約者郵便番号", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "契約者住所漢字", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "契約者電話番号", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "fis_cd", cf_c10_bor_yellow)

    return sheet, row


# data write
def mz_data(keijyo_date_int, sheet, row, cf_dic):
    # format
    cf_l10_bor = cf_dic["cf_l10_bor"]
    cf_c10_bor = cf_dic["cf_c10_bor"]

    # init
    row += 1

    # sql_data
    sql_data_cnt = 0
    sql_data = keijyo_list_all_sql.mz_sql_order_store(keijyo_date_int)
    sql_data_cnt = len(sql_data)

    # write
    for dt in sql_data:
        col = 0
        sheet.write(row, col, dt["section_cd"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["section_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["cat_cd"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["cat_name_simple"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["keiyaku_cd"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["keiyaku_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["mosikomi_cd"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["syoken_cd_main"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["syoken_cd_sub"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["old_syoken_cd_main"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["old_syoken_cd_sub"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["coltd_cd"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["coltd_name"], cf_l10_bor)

        col += 1
        sheet.write(row, col, dt["kind_cd_main"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["kind_name_main"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["kind_cd_sub"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["keijyo_date"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["siki_date"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["manki_date"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["ido_kai_date"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["hoken_kikan_cd"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["hoken_kikan_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["pay_num_cd"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["pay_num_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["keisu_year"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["hoken_ryo"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["hoken_ryo_year"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["ido_kai_hoken_ryo"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["staff1_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["staff2_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["staff3_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["gyotei1_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["gyotei2_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["gyotei3_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fee_staff1"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fee_staff2"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fee_staff3"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fee_gyotei1"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fee_gyotei2"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fee_gyotei3"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fee_cat"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fee_ritu"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fee_yen"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fee_cd_all"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fee_seiho_kikan"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fee_seiho_first"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fee_seiho_next"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["hojin_kojin_cd"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["kei_name"], cf_l10_bor)

        col += 1
        sheet.write(row, col, dt["kei_name_hira"], cf_l10_bor)

        col += 1
        sheet.write(row, col, dt["kei_post"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["kei_address"], cf_l10_bor)

        col += 1
        sheet.write(row, col, dt["kei_tel"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["fis_cd"], cf_c10_bor)

        row += 1

    return sheet, row, sql_data_cnt
