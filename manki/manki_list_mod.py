from dateutil.relativedelta import relativedelta

# from typing import Any, Dict, List, Tuple, Union
from typing import Any, Dict, List, Union

from _mod import mod_datetime
from _mod_fis import mod_common
from manki import manki_list_sql


# setting, title
def mz_title(sheet, row, cf_dic):
    cf_c10_bor_yellow = cf_dic["cf_c10_bor_yellow"]  # format
    sheet.set_paper(9)  # A4 size paper
    sheet.set_default_row(25)  # height
    sheet.freeze_panes(1, 0)  # 1行目固定

    col = 0
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "契約状況", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 17)
    sheet.write(0, col, "証券番号", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 7)
    sheet.write(0, col, "枝番", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 17)
    sheet.write(0, col, "旧証券番号", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 7)
    sheet.write(0, col, "旧枝番", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "始期", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "満期", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "早期更改29日前", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "早期更改15日前", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "異動解約日", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "保険会社", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険種目", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "保険種類", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 40)
    sheet.write(0, col, "契約者名", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "保険料", cf_c10_bor_yellow)

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

    return sheet, row


# data write
def mz_data(manki_date_int, section_cd, staff_cd, stf_key, sheet, row, cf_dic):
    # format
    cf_l10_bor = cf_dic["cf_l10_bor"]
    cf_c10_bor = cf_dic["cf_c10_bor"]
    cf_r10_comma_bor = cf_dic["cf_r10_comma_bor"]

    # init
    row += 1

    # sql_data
    sql_data: Union[List[Dict[str, Any]], str] = manki_list_sql.mz_sql_order_store(
        manki_date_int, section_cd, staff_cd, stf_key
    )
    if isinstance(sql_data, str):
        return sheet, row, 0

    sql_data_cnt = len(sql_data)

    # write
    for dt in sql_data:
        # 未使用/解約チェック res = normal or kaiyaku
        # res = manki_list_sql.mz_kaiyaku_chk(dt['syoken_cd_main'], dt['syoken_cd_sub'])
        # if res == 'normal':

        # 早期更改4週間前 = 満期日 - 29日
        temp29 = mod_datetime.mz_mum2date_yymmdd(dt["manki_date"]) + relativedelta(days=-29)
        souki_koukai_29 = mod_datetime.mz_dt2str_yymmdd_slash(temp29)

        # 早期更改2週間前 = 満期日 - 15日
        temp15 = mod_datetime.mz_mum2date_yymmdd(dt["manki_date"]) + relativedelta(days=-15)
        souki_koukai_15 = mod_datetime.mz_dt2str_yymmdd_slash(temp15)

        col = 0
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
        sheet.write(row, col, mod_common.mz_num2date_slash(dt["siki_date"]), cf_c10_bor)

        col += 1
        sheet.write(row, col, mod_common.mz_num2date_slash(dt["manki_date"]), cf_c10_bor)

        col += 1
        sheet.write(row, col, souki_koukai_29, cf_c10_bor)

        col += 1
        sheet.write(row, col, souki_koukai_15, cf_c10_bor)

        col += 1
        sheet.write(
            row,
            col,
            mod_common.mz_num2date_slash_normal(dt["ido_kai_date"]),
            cf_c10_bor,
        )

        col += 1
        sheet.write(row, col, dt["coltd_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["kind_name_main"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["kind_name_sub"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["kei_name"], cf_l10_bor)

        col += 1
        sheet.write(row, col, dt["hoken_ryo"], cf_r10_comma_bor)

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

        row += 1

    return sheet, row, sql_data_cnt
