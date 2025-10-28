import datetime
from _mod import mod_datetime
from _mod_fis import mod_common, mod_section, mod_coltd
from sum import sum_common_sql


# setting
def mz_setting(sheet):
    sheet.set_default_row(25)  # height
    sheet.set_column(0, 0, 4)  # No.
    sheet.set_column(1, 1, 42)  # 分野/会社名

    sheet.set_column(2, 2, 18)  # 契約件数
    sheet.set_column(3, 3, 18)  # 契約顧客件数
    sheet.set_column(4, 4, 18)  # 保険料[年換算]
    sheet.set_column(5, 5, 18)  # 初年度手数料
    sheet.set_column(6, 6, 18)  # 総手数料

    sheet.set_column(7, 7, 1)  # space

    sheet.set_column(8, 8, 18)  # 契約件数
    sheet.set_column(9, 9, 18)  # 契約顧客件数
    sheet.set_column(10, 10, 18)  # 保険料[年換算]
    sheet.set_column(11, 11, 18)  # 初年度手数料
    sheet.set_column(12, 12, 18)  # 総手数料
    return sheet


# header
def mz_header(sheet, row, cf_dic, title_name):
    cf_l18 = cf_dic["cf_l18"]
    cf_l11_bor_btm = cf_dic["cf_l11_bor_btm"]

    sheet.set_row(row, 40)  # height
    sheet.write(row, 0, title_name, cf_l18)
    sheet.write(row, 11, "担当印", cf_l11_bor_btm)
    sheet.write(row, 12, "確認印", cf_l11_bor_btm)
    row += 1

    # spacer
    sheet.set_row(row, 10)  # height
    sheet.write(row, 0, "")
    row += 1

    return sheet, row


# title
def mz_title(sheet, row, cf_dic):
    cf_l14_bor = cf_dic["cf_l14_bor"]
    cf_c14_bor = cf_dic["cf_c14_bor"]

    sheet.set_row(row, 25)  # height
    sheet.merge_range(row, 0, row + 1, 0, "No", cf_c14_bor)
    sheet.merge_range(row, 1, row + 1, 1, "分野/会社名", cf_l14_bor)

    sheet.merge_range(row, 2, row, 6, "当月", cf_c14_bor)
    sheet.merge_range(row, 8, row, 12, "年度累計", cf_c14_bor)

    row += 1
    sheet.write(row, 2, "契約件数", cf_c14_bor)
    sheet.write(row, 3, "契約顧客件数", cf_c14_bor)
    sheet.write(row, 4, "保険料[年換算]", cf_c14_bor)
    sheet.write(row, 5, "初年度手数料", cf_c14_bor)
    sheet.write(row, 6, "総手数料", cf_c14_bor)

    sheet.write(row, 8, "契約件数", cf_c14_bor)
    sheet.write(row, 9, "契約顧客件数", cf_c14_bor)
    sheet.write(row, 10, "保険料[年換算]", cf_c14_bor)
    sheet.write(row, 11, "初年度手数料", cf_c14_bor)
    sheet.write(row, 12, "総手数料", cf_c14_bor)

    return sheet, row


# cat data
def mz_cat(sheet, row, cf_dic):
    cf_l14_bor = cf_dic["cf_l14_bor"]
    cf_c14_bor = cf_dic["cf_c14_bor"]
    # cf_l12 = cf_dic['cf_l12')

    # init
    row += 1
    left_number = 0

    # データ作成
    sql_data = sum_common_sql.mz_sql_cat()
    for dt in sql_data:
        row += 1
        left_number += 1
        col = -1

        col += 1
        sheet.write(row, col, left_number, cf_c14_bor)

        col += 1
        sheet.write(row, col, dt["cat_name_simple"], cf_l14_bor)

    # 分野の総合計
    row += 1
    col = -1

    col += 1
    sheet.write(row, col, "", cf_c14_bor)

    col += 1
    sheet.write(row, col, "総合計", cf_l14_bor)

    return sheet, row


# 総合計 grand total
def mz_grand(sheet, cf_dic, grand_dic):
    cf_r14_comma_bor = cf_dic["cf_r14_comma_bor"]

    # grand data
    kensu_cnt_sum_grand_tou = grand_dic["kensu_cnt_sum_grand_tou"]
    kensu_cnt_sum_grand_rui = grand_dic["kensu_cnt_sum_grand_rui"]

    keiko_cnt_sum_grand_tou = grand_dic["keiko_cnt_sum_grand_tou"]
    keiko_cnt_sum_grand_rui = grand_dic["keiko_cnt_sum_grand_rui"]

    res_hoken_ryo_year_sum_grand_tou = grand_dic["res_hoken_ryo_year_sum_grand_tou"]
    res_hoken_ryo_year_sum_grand_rui = grand_dic["res_hoken_ryo_year_sum_grand_rui"]

    res_fee_money_sum_grand_tou = grand_dic["res_fee_money_sum_grand_tou"]
    res_fee_money_sum_grand_rui = grand_dic["res_fee_money_sum_grand_rui"]

    # res_fee_money_year_sum_grand_tou = grand_dic["res_fee_money_year_sum_grand_tou"]
    # res_fee_money_year_sum_grand_rui = grand_dic["res_fee_money_year_sum_grand_rui"]

    res_fee_money_total_sum_grand_tou = grand_dic["res_fee_money_total_sum_grand_tou"]
    res_fee_money_total_sum_grand_rui = grand_dic["res_fee_money_total_sum_grand_rui"]

    sheet.set_row(8, 25)  # height

    sheet.write(8, 2, kensu_cnt_sum_grand_tou, cf_r14_comma_bor)
    sheet.write(8, 3, keiko_cnt_sum_grand_tou, cf_r14_comma_bor)

    sheet.write(8, 4, res_hoken_ryo_year_sum_grand_tou, cf_r14_comma_bor)
    sheet.write(8, 5, res_fee_money_sum_grand_tou, cf_r14_comma_bor)
    # sheet.write(8, 5, res_fee_money_year_sum_grand_tou, cf_r14_comma_bor)
    sheet.write(8, 6, res_fee_money_total_sum_grand_tou, cf_r14_comma_bor)

    sheet.write(8, 8, kensu_cnt_sum_grand_rui, cf_r14_comma_bor)
    sheet.write(8, 9, keiko_cnt_sum_grand_rui, cf_r14_comma_bor)

    sheet.write(8, 10, res_hoken_ryo_year_sum_grand_rui, cf_r14_comma_bor)
    sheet.write(8, 11, res_fee_money_sum_grand_rui, cf_r14_comma_bor)
    # sheet.write(8, 11, res_fee_money_year_sum_grand_rui, cf_r14_comma_bor)
    sheet.write(8, 12, res_fee_money_total_sum_grand_rui, cf_r14_comma_bor)

    return sheet


# footer, datetime, user_email
def mz_datetime_user(sheet, row, col, cf_dic, user_email):
    now_datetime_str = mod_datetime.mz_dt2str_yymmddhhmmss_hyphen(datetime.datetime.now() + datetime.timedelta(hours=9))
    cre_date_user = now_datetime_str + "/" + user_email
    row += 2
    sheet.write(row, col, cre_date_user, cf_dic["cf_r10"])
    return sheet, row


# section_cd set to section_list
def moz_section_list():
    section_list = []
    section_list.append("0")
    sql_data = mod_section.mz_section_data_on()
    for dt in sql_data:
        section_list.append(dt["section_cd"])
    return section_list


# 取り扱い保険会社件数、行の位置を上に戻す、扱い保険会社件数プラス1
def moz_tori_back(cat_cd, row):
    cat_data = mod_coltd.mz_coltd_onoff_cat("on", cat_cd)
    cat_tori = len(cat_data)
    cat_tori_back = cat_tori * (-1)
    row += cat_tori_back
    return row


# sum_stf, sum_total, sum_list 共通モジュール
def mz_title_list(sheet, cf_dic):
    sheet.set_row(0, 25)  # height
    sheet.freeze_panes(1, 0)  # 1行目固定
    cf_c10_bor_yellow = cf_dic["cf_c10_bor_yellow"]

    col = 0
    sheet.set_column(col, col, 5)
    sheet.write(0, col, "NO", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "計上月", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "状況", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "営業所", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "分配種別", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "担当者", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "担当者比率", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 10)
    sheet.write(0, col, "分類", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 32)
    sheet.write(0, col, "保険会社", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "証券番号", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険種類main", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 15)
    sheet.write(0, col, "保険種類sub", cf_c10_bor_yellow)

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
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "異動解約日", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 12)
    sheet.write(0, col, "未経過月", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "保険期間（年）", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "保険料", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "保険料（年換算）", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "保険料（合計）", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "損保手数料（率）", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "手数料（初年度）", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "手数料（年間）", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 20)
    sheet.write(0, col, "手数料（合計）", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "契約者", cf_c10_bor_yellow)

    col += 1
    sheet.set_column(col, col, 30)
    sheet.write(0, col, "業務提携", cf_c10_bor_yellow)

    return sheet


# stf list
def mz_data_stf_list(sheet, cf_dic, kei_date_int, keiyaku_grp_cd, staff_email):
    sql_data = sum_common_sql.mz_data_stf_list(kei_date_int, keiyaku_grp_cd, staff_email)
    sheet = mz_write_sheet(sheet, cf_dic, sql_data)
    return sheet


# stf メール送信の件数表示用
def mz_data_stf_kensu_for_email(kei_date_int, keiyaku_grp_cd, staff_email):
    kensu_for_email = sum_common_sql.mz_data_stf_kensu_for_email(kei_date_int, keiyaku_grp_cd, staff_email)
    return kensu_for_email


# total list
def mz_data_total_list(sheet, cf_dic, kei_date_int, keiyaku_grp_cd):
    sql_data = sum_common_sql.mz_data_total_list(kei_date_int, keiyaku_grp_cd)
    sheet = mz_write_sheet(sheet, cf_dic, sql_data)
    return sheet


# total メール送信の件数表示用
def mz_data_total_kensu_for_email(kei_date_int, keiyaku_grp_cd):
    kensu_for_email = sum_common_sql.mz_data_total_kensu_for_email(kei_date_int, keiyaku_grp_cd)
    return kensu_for_email


# list list
def mz_data_list_list(sheet, cf_dic, kei_date_int):
    sql_data = sum_common_sql.mz_data_list_list(kei_date_int)
    sheet = mz_write_sheet(sheet, cf_dic, sql_data)
    return sheet


# list メール送信の件数表示用
def mz_data_list_kensu_for_email(kei_date_int):
    kensu_for_email = sum_common_sql.mz_data_list_kensu_for_email(kei_date_int)
    return kensu_for_email


# write sheet
def mz_write_sheet(sheet, cf_dic, sql_data):
    cf_l10_bor = cf_dic["cf_l10_bor"]
    cf_c10_bor = cf_dic["cf_c10_bor"]
    cf_r10_comma_bor = cf_dic["cf_r10_comma_bor"]
    left_number = 0
    row = 0

    for dt in sql_data:
        left_number += 1
        row += 1
        sheet.set_row(row, 25)  # height

        col = 0
        sheet.write(row, col, left_number, cf_c10_bor)

        col += 1
        sheet.write(row, col, mod_common.mz_keijyo_date_str(dt["keijyo_date"]), cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["keiyaku_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["section_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["person_kind_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["staff_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["staff_fee_per"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["cat_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["coltd_name"], cf_l10_bor)

        col += 1
        sheet.write(row, col, dt["syoken_cd_main"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["kind_name_main"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["kind_name_sub"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["pay_num_name"], cf_c10_bor)

        col += 1
        sheet.write(row, col, mod_common.mz_num2date_slash(dt["siki_date"]), cf_c10_bor)

        col += 1
        sheet.write(row, col, mod_common.mz_num2date_slash(dt["manki_date"]), cf_c10_bor)

        col += 1
        sheet.write(
            row,
            col,
            mod_common.mz_num2date_slash_normal(dt["ido_kai_date"]),
            cf_c10_bor,
        )

        col += 1
        sheet.write(row, col, dt["mikeika_month"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["res_hoken_kikan_year"], cf_c10_bor)

        col += 1
        sheet.write(row, col, dt["res_hoken_ryo"], cf_r10_comma_bor)

        col += 1
        sheet.write(row, col, dt["res_hoken_ryo_year"], cf_r10_comma_bor)

        col += 1
        sheet.write(row, col, dt["res_hoken_ryo_total"], cf_r10_comma_bor)

        col += 1
        sheet.write(row, col, dt["fee_ritu"], cf_r10_comma_bor)

        col += 1
        sheet.write(row, col, dt["res_fee_money"], cf_r10_comma_bor)

        col += 1
        sheet.write(row, col, dt["res_fee_money_year"], cf_r10_comma_bor)

        col += 1
        sheet.write(row, col, dt["res_fee_money_total"], cf_r10_comma_bor)

        col += 1
        sheet.write(row, col, dt["kei_name"], cf_l10_bor)

        col += 1
        sheet.write(row, col, dt["gyotei_name"], cf_l10_bor)

    return sheet
