# cell setting セルの設定をする
def mz_setting(sheet):
    sheet.set_default_row(25)  # height
    sheet.set_column(0, 0, 8)
    sheet.set_column(1, 1, 8)
    sheet.set_column(2, 2, 8)
    sheet.set_column(3, 3, 38)
    sheet.set_column(4, 4, 68)
    sheet.set_column(5, 5, 13)
    sheet.set_column(6, 6, 13)
    sheet.set_column(7, 7, 13)
    sheet.set_column(8, 8, 13)
    sheet.set_column(9, 9, 13)
    sheet.set_column(10, 10, 13)
    return sheet


# head ヘッダーを作成する
def mz_head_title(sheet, row_cnt, cf_dic, invoice_sta_name, pay_date_str, start_time):
    sheet.set_row(row_cnt, 30)  # height
    sheet.write(row_cnt, 0, "業務提携料支払リスト(経理用)_" + invoice_sta_name, cf_dic["cf_l14"])
    sheet.write(row_cnt, 10, "保険事業部　" + pay_date_str + "　支払分", cf_dic["cf_r14"])
    row_cnt += 1
    sheet.write(row_cnt, 10, "作成時刻:" + start_time, cf_dic["cf_r10"])
    return sheet, row_cnt


# sign 署名を入力するBOXを作成する
def mz_sign(sheet, row_cnt, cf_dic):
    sheet.set_row(row_cnt, 25)  # height
    sheet.write(row_cnt, 8, "担当印", cf_dic["cf_c10_bor"])
    sheet.write(row_cnt, 9, "担当印", cf_dic["cf_c10_bor"])
    sheet.write(row_cnt, 10, "承認印", cf_dic["cf_c10_bor"])
    row_cnt += 1
    sheet.set_row(row_cnt, 25)  # height
    sheet.merge_range(row_cnt, 8, row_cnt + 2, 8, "", cf_dic["cf_c10_bor"])
    sheet.merge_range(row_cnt, 9, row_cnt + 2, 9, "", cf_dic["cf_c10_bor"])
    sheet.merge_range(row_cnt, 10, row_cnt + 2, 10, "", cf_dic["cf_c10_bor"])
    return sheet, row_cnt


# header normal 通常のリストのラベル
def mz_header_title_normal(sheet, row_cnt, cf_dic):
    sheet.set_row(row_cnt, 27)  # height
    sheet.write(row_cnt, 0, "No", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 1, "営業所", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 2, "管理CD", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 3, "委託先名", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 4, "振込口座", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 5, "小計(税抜)", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 6, "消費税", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 7, "控除額", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 8, "小計(税込)", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 9, "源泉徴収額", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 10, "合計(税込)", cf_dic["cf_c10_bor_line_double"])
    return sheet, row_cnt


# シートの合計を作成するときのラベル
def mz_header_title_sheet_total(sheet, row_cnt, cf_dic):
    sheet.set_row(row_cnt, 27)  # height
    sheet.write(row_cnt, 0, "件数合計", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 5, "小計(税抜)", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 6, "消費税", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 7, "控除額", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 8, "小計(税込)", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 9, "源泉徴収額", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 10, "合計(税込)", cf_dic["cf_c10_bor_line_double"])
    return sheet, row_cnt


# 総合計のシートを作成するときのラベル
def mz_header_title_all_total(sheet, row_cnt, cf_dic):
    sheet.set_row(row_cnt, 27)  # height
    sheet.write(row_cnt, 5, "小計(税抜)", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 6, "消費税", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 7, "控除額", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 8, "小計(税込)", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 9, "源泉徴収額", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row_cnt, 10, "合計(税込)", cf_dic["cf_c10_bor_line_double"])
    return sheet, row_cnt
