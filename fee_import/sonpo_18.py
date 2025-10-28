# -------------------------------------------------------------------
#  18 楽天損保
# -------------------------------------------------------------------
from _mod import mod_decimal
from fee_import import set_basic as SET_BASIC


# データ
def set_sheet(sheet_dic):
    # cell color
    # cell_yellow, cell_pink = SET_BASIC.set_cell_color()

    # Set sheet config
    original_sheet, new_sheet, new_sheet_url = SET_BASIC.set_sheet_config(sheet_dic)

    # Set header
    SET_BASIC.set_header(new_sheet)

    # 保険会社別設定
    syoken = 7  # col G 証券番号
    fee_withtax = 14  # col N 税込
    kaime = 11  # col K 回目

    # syokenデータを2行目から取得
    y = 2 - 1
    row_len = len(original_sheet.col_values(syoken)[y:]) + 1

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

    # original sheet
    org_list_syoken = original_sheet.col_values(syoken)[y:]
    org_list_withtax = original_sheet.col_values(fee_withtax)[y:]
    org_list_kaime = original_sheet.col_values(kaime)[y:]

    # original sheet cnt 縦セルの最後のブランクを除いた数
    org_list_kaime_cnt = len(org_list_kaime)

    # new sheet
    new_list_kind = new_sheet.range(f"E2:E{row_len}")  # 手数料種類
    new_list_syoken = new_sheet.range(f"F2:F{row_len}")  # 証券番号
    new_list_kaime = new_sheet.range(f"L2:L{row_len}")  # 回目
    new_list_withtax = new_sheet.range(f"H2:H{row_len}")  # 税込
    new_list_notax = new_sheet.range(f"I2:I{row_len}")  # 税抜
    new_list_tax_num = new_sheet.range(f"J2:J{row_len}")  # 消費税額
    new_list_tax_per = new_sheet.range(f"K2:K{row_len}")  # 消費税率
    new_list_first_next_year = new_sheet.range(f"M2:M{row_len}")  # 初年度次年度

    # リストにセットする
    for i in range(row_len - 1):
        # 証券番号 F
        syoken_value = org_list_syoken[i]
        if syoken_value:
            new_list_syoken[i].value = syoken_value.strip()
        else:
            new_list_syoken[i].value = ""

        # 税込 H
        try:
            new_list_withtax[i].value = int(org_list_withtax[i].replace(",", ""))
        except ValueError:
            print(f"org_list_withtax convert error '{org_list_withtax[i]}' to a number")

        # 回目 L
        if i < org_list_kaime_cnt:
            kaime_value = org_list_kaime[i]
            if kaime_value:
                new_list_kaime[i].value = kaime_value.strip()
            else:
                new_list_kaime[i].value = ""
        else:
            new_list_kaime[i].value = ""

        # 税抜 I、四捨五入 decimalモジュール使用
        new_list_notax[i].value = mod_decimal.round_half_up((new_list_withtax[i].value) / 1.1)

        # 消費税額 J
        new_list_tax_num[i].value = int(new_list_withtax[i].value) - int(new_list_notax[i].value)

        # 初年度次年度 M
        new_list_first_next_year[i].value = 0

    # update
    new_sheet.update_cells(new_list_kind)
    new_sheet.update_cells(new_list_syoken)
    new_sheet.update_cells(new_list_kaime)
    new_sheet.update_cells(new_list_withtax)
    new_sheet.update_cells(new_list_notax)
    new_sheet.update_cells(new_list_tax_num)
    new_sheet.update_cells(new_list_tax_per)
    new_sheet.update_cells(new_list_first_next_year)

    # Set format
    SET_BASIC.set_format(new_sheet, row_len)

    return new_sheet_url
