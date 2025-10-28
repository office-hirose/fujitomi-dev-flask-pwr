# -------------------------------------------------------------------
#  04 三井住友海上火災
# -------------------------------------------------------------------
# from gspread_formatting import format_cell_range
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
    syoken = 5  # col E 証券番号
    fee_withtax = 10  # col J 税込
    kaime = 9  # col I 回目
    kanjib = 31  # col AE 漢字備考、手数料種類、消費税率を判定する

    # syokenデータを2行目から取得
    y = 2 - 1
    row_len = len(original_sheet.col_values(syoken)[y:]) + 1

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

    # original sheet
    org_list_syoken = original_sheet.col_values(syoken)[y:]
    org_list_withtax = original_sheet.col_values(fee_withtax)[y:]
    org_list_kaime = original_sheet.col_values(kaime)[y:]
    org_list_kanjib = original_sheet.col_values(kanjib)[y:]

    # original sheet cnt 縦セルの最後のブランクを除いた数
    # org_list_syoken_cnt = len(org_list_syoken)
    # org_list_withtax_cnt = len(org_list_withtax)
    # org_list_tax_num_cnt = len(org_list_tax_num)
    org_list_kaime_cnt = len(org_list_kaime)
    org_list_kanjib_cnt = len(org_list_kanjib)

    # new sheet
    new_list_kind = new_sheet.range(f"E2:E{row_len}")  # 手数料種類
    new_list_syoken = new_sheet.range(f"F2:F{row_len}")  # 証券番号
    new_list_kaime = new_sheet.range(f"L2:L{row_len}")  # 回目
    new_list_withtax = new_sheet.range(f"H2:H{row_len}")  # 税込
    new_list_notax = new_sheet.range(f"I2:I{row_len}")  # 税抜
    new_list_tax_num = new_sheet.range(f"J2:J{row_len}")  # 消費税額
    new_list_tax_per = new_sheet.range(f"K2:K{row_len}")  # 消費税率
    new_list_first_next_year = new_sheet.range(f"M2:M{row_len}")  # 初年度次年度
    new_list_kanjib = new_sheet.range(f"N2:N{row_len}")  # 漢字備考
    new_sheet.update_cell(1, 14, "漢字備考")

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

        # 漢字備考 N
        if i < org_list_kanjib_cnt:
            kanjib_value = org_list_kanjib[i]
            if kanjib_value:
                new_list_kanjib[i].value = kanjib_value.strip()
            else:
                new_list_kanjib[i].value = ""

        # 消費税率 K, 手数料種類 E
        # 振替手数料＝口振
        # 取扱手数料＝コンビニなど
        # クレ等手数料＝クレジットカード
        if kanjib_value.strip() == "振替手数料":
            new_list_kind[i].value = 2
            new_list_tax_per[i].value = 10
        elif kanjib_value.strip() == "取扱手数料":
            new_list_kind[i].value = 2
            new_list_tax_per[i].value = 10
        elif kanjib_value.strip() == "クレ等手数料":
            new_list_kind[i].value = 2
            new_list_tax_per[i].value = 0
        else:
            new_list_kind[i].value = 1
            new_list_tax_per[i].value = 10

        # 税抜 I
        if new_list_tax_per[i].value == 10:
            # 四捨五入 decimalモジュール使用
            new_list_notax[i].value = mod_decimal.round_half_up((new_list_withtax[i].value) / 1.1)
        else:
            new_list_notax[i].value = new_list_withtax[i].value

        # 消費税額 J
        if new_list_tax_per[i].value == 10:
            new_list_tax_num[i].value = int(new_list_withtax[i].value) - int(new_list_notax[i].value)
        else:
            new_list_tax_num[i].value = 0

        # 初年度次年度 M
        new_list_first_next_year[i].value = 0

        # 値が2の時に背景色をピンクに設定、しかしGoogle API 制限回数制限があるため、エラーが出る場合がある
        # if new_list_kind[i].value == 2:
        #     format_cell_range(new_sheet, f"E{i+2}", cell_pink)

    # update
    new_sheet.update_cells(new_list_kind)
    new_sheet.update_cells(new_list_syoken)
    new_sheet.update_cells(new_list_kaime)
    new_sheet.update_cells(new_list_withtax)
    new_sheet.update_cells(new_list_notax)
    new_sheet.update_cells(new_list_tax_num)
    new_sheet.update_cells(new_list_tax_per)
    new_sheet.update_cells(new_list_first_next_year)
    new_sheet.update_cells(new_list_kanjib)

    # 手数料種類 E が 2 の場合は背景色をピンクにする。しかし、Google API 制限オーバーとなる。
    # kind_data = new_sheet.col_values(5)[y:]
    # for i in range(len(kind_data)):
    #     kind_value = int(kind_data[i])
    #     if kind_value == 2:
    #         format_cell_range(new_sheet, f"E{i+2}", cell_pink)

    # Set format
    SET_BASIC.set_format(new_sheet, row_len)

    return new_sheet_url
