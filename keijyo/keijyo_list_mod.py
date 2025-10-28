from typing import Any, Dict, List, Union

from _mod_fis import mod_common
from keijyo import keijyo_list_sql


# setting, title
def mz_title(sheet, row, cf_dic):
    cf_c10_bor_yellow = cf_dic["cf_c10_bor_yellow"]  # format
    sheet.set_paper(9)  # A4 size paper
    sheet.set_default_row(25)  # height
    sheet.freeze_panes(1, 0)  # 1行目固定

    col = 0
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "営業所", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "社内計上月", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "始期", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "満期", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "契約状況", cf_c10_bor_yellow)

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
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "分類", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "保険会社", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険種目", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険種類", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "契約者名", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "メモ", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "払込方法", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険料", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険料年換算", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "[損]手数料", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "[生]手数料支払年数", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "[生]初年度手数料", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "[生]次年度以降の年間手数料", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "異動解約日", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "異動解約保険料", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "担当1", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "担当2", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "担当3", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "提携1", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "提携2", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "提携3", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "担当1[率]", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "担当2[率]", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "担当3[率]", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "提携1[率]", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "提携2[率]", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "提携3[率]", cf_c10_bor_yellow)

    return sheet, row


# data write
def mz_data(keijyo_date_int, section_cd, staff_cd, stf_key, sheet, row, cf_dic):
    # format
    cf_l10_bor = cf_dic["cf_l10_bor"]
    cf_c10_bor = cf_dic["cf_c10_bor"]
    cf_r12_comma = cf_dic["cf_r12_comma"]
    cf_r12_comma_decimal = cf_dic["cf_r12_comma_decimal"]

    # init
    row += 1

    # sql_data
    sql_data: Union[List[Dict[str, Any]], str] = keijyo_list_sql.mz_sql_order_store(
        keijyo_date_int, section_cd, staff_cd, stf_key
    )
    if isinstance(sql_data, str):
        return sheet, row, 0

    sql_data_cnt = len(sql_data)

    # write
    for dt in sql_data:
        col = 0
        sheet.write(row, col, dt["sec_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, mod_common.mz_keijyo_date_str(dt["keijyo_date"]), cf_c10_bor)

        col += 1
        sheet.write(row, col, mod_common.mz_num2date_slash(dt["siki_date"]), cf_c10_bor)

        col += 1
        sheet.write(row, col, mod_common.mz_num2date_slash(dt["manki_date"]), cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["keiyaku_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["syoken_cd_main"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["syoken_cd_sub"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["old_syoken_cd_main"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["old_syoken_cd_sub"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["mosikomi"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["cat_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["coltd_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["kind_name_main"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["kind_name_sub"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["kei_name"], cf_l10_bor)

        col += 1
        sheet.write(row, col, dt["memo"], cf_l10_bor)

        col += 1
        sheet.write(row, col, dt["pay_num_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["hoken_ryo"], cf_r12_comma)

        col += 1
        sheet.write(row, col, dt["hoken_ryo_year"], cf_r12_comma)

        col += 1
        sheet.write(row, col, dt["fee_sonpo_yen"], cf_r12_comma)

        col += 1
        sheet.write(row, col, dt["fee_seiho_kikan"], cf_r12_comma)

        col += 1
        sheet.write(row, col, dt["fee_seiho_first"], cf_r12_comma)

        col += 1
        sheet.write(row, col, dt["fee_seiho_next"], cf_r12_comma)

        col += 1
        sheet.write(row, col, mod_common.mz_num2date_slash(dt["ido_kai_date"]), cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["ido_kai_hoken_ryo"], cf_r12_comma)

        col += 1
        sheet.write(row, col, dt["staff1_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["staff2_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["staff3_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["gyotei1_name"], cf_l10_bor)

        col += 1
        sheet.write(row, col, dt["gyotei2_name"], cf_l10_bor)

        col += 1
        sheet.write(row, col, dt["gyotei3_name"], cf_l10_bor)

        col += 1
        sheet.write(row, col, dt["fee_staff1"], cf_r12_comma_decimal)

        col += 1
        sheet.write(row, col, dt["fee_staff2"], cf_r12_comma_decimal)

        col += 1
        sheet.write(row, col, dt["fee_staff3"], cf_r12_comma_decimal)

        col += 1
        sheet.write(row, col, dt["fee_gyotei1"], cf_r12_comma_decimal)

        col += 1
        sheet.write(row, col, dt["fee_gyotei2"], cf_r12_comma_decimal)

        col += 1
        sheet.write(row, col, dt["fee_gyotei3"], cf_r12_comma_decimal)

        row += 1

    return sheet, row, sql_data_cnt
