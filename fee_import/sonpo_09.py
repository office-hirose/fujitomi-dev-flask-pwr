# -------------------------------------------------------------------
#  09 東京海上日動火災
# -------------------------------------------------------------------
# from gspread_formatting import format_cell_range
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

    # 「代理店手数料」ー「代手消費税」＝手数料税抜。
    # 枝番は全て0000に置き換える。

    syoken = 13  # col M 証券番号
    fee_withtax = 24  # col X 税込
    fee_tax_num = 34  # col AH 消費税
    kaime = 29  # col AC 回目
    komidasi = 37  # col AK 小見出し区分

    # syokenデータを2行目から取得
    y = 2 - 1
    row_len = len(original_sheet.col_values(syoken)[y:]) + 1

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

    # original sheet
    org_list_syoken = original_sheet.col_values(syoken)[y:]
    org_list_withtax = original_sheet.col_values(fee_withtax)[y:]
    org_list_tax_num = original_sheet.col_values(fee_tax_num)[y:]
    org_list_kaime = original_sheet.col_values(kaime)[y:]
    org_list_komidasi = original_sheet.col_values(komidasi)[y:]

    # original sheet cnt 縦セルの最後のブランクを除いた数
    org_list_kaime_cnt = len(org_list_kaime)
    org_list_komidasi_cnt = len(org_list_komidasi)

    # new sheet
    new_list_kind = new_sheet.range(f"E2:E{row_len}")  # 手数料種類
    new_list_syoken = new_sheet.range(f"F2:F{row_len}")  # 証券番号
    new_list_kaime = new_sheet.range(f"L2:L{row_len}")  # 回目
    new_list_withtax = new_sheet.range(f"H2:H{row_len}")  # 税込
    new_list_notax = new_sheet.range(f"I2:I{row_len}")  # 税抜
    new_list_tax_num = new_sheet.range(f"J2:J{row_len}")  # 消費税額
    new_list_tax_per = new_sheet.range(f"K2:K{row_len}")  # 消費税率
    new_list_first_next_year = new_sheet.range(f"M2:M{row_len}")  # 初年度次年度
    new_list_komidasi = new_sheet.range(f"N2:N{row_len}")  # 手数料種別-小見出し区分
    new_sheet.update_cell(1, 14, "手数料種別-小見出し区分")

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

        # 小見出し区分 N - 手数料種類を設定するため

        # 手数料種類、参照=N列、手数料種類=E列、税率＝K列
        # J=1、通常手数料、10%
        # G=1、通常手数料、10%
        # K=1、通常手数料、10%
        # L=2、振替手数料、10%
        # N=2、振替手数料、10%
        # O=2、振替手数料、10%
        # M=2、振替手数料、0%
        # それ以外=0

        if i < org_list_komidasi_cnt:
            komidasi_value = org_list_komidasi[i]
            if komidasi_value:
                komidasi_value = komidasi_value.strip()
                new_list_komidasi[i].value = komidasi_value

                if komidasi_value == "J":
                    new_list_kind[i].value = 1
                    new_list_tax_per[i].value = 10
                elif komidasi_value == "G":
                    new_list_kind[i].value = 1
                    new_list_tax_per[i].value = 10
                elif komidasi_value == "K":
                    new_list_kind[i].value = 1
                    new_list_tax_per[i].value = 10
                elif komidasi_value == "L":
                    new_list_kind[i].value = 2
                    new_list_tax_per[i].value = 10
                elif komidasi_value == "N":
                    new_list_kind[i].value = 2
                    new_list_tax_per[i].value = 10
                elif komidasi_value == "O":
                    new_list_kind[i].value = 2
                    new_list_tax_per[i].value = 10
                elif komidasi_value == "M":
                    new_list_kind[i].value = 2
                    new_list_tax_per[i].value = 0
                else:
                    new_list_kind[i].value = 1
                    new_list_tax_per[i].value = 10
            else:
                new_list_komidasi[i].value = ""
                new_list_kind[i].value = 1
                new_list_tax_per[i].value = 10
        else:
            new_list_komidasi[i].value = ""
            new_list_kind[i].value = 1
            new_list_tax_per[i].value = 10

        # 消費税金額 J
        try:
            tax_num_value = int(org_list_tax_num[i].replace(",", ""))

            # 税込がプラス、消費税がプラスの場合
            if new_list_withtax[i].value > 0 and tax_num_value > 0:
                new_list_tax_num[i].value = tax_num_value
            # 税込がプラス、消費税がマイナスの場合
            elif new_list_withtax[i].value > 0 and tax_num_value < 0:
                new_list_tax_num[i].value = tax_num_value * -1
            # 税込がマイナス、消費税がマイナスの場合
            elif new_list_withtax[i].value < 0 and tax_num_value < 0:
                new_list_tax_num[i].value = tax_num_value
            # 税込がマイナス、消費税がプラスの場合
            elif new_list_withtax[i].value < 0 and tax_num_value > 0:
                new_list_tax_num[i].value = tax_num_value * -1

        except ValueError:
            print(f"org_list_tax_num convert error '{org_list_tax_num[i]}' to a number")

        # 税抜 I
        new_list_notax[i].value = int(new_list_withtax[i].value) - int(new_list_tax_num[i].value)

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
    new_sheet.update_cells(new_list_komidasi)

    # Set format
    SET_BASIC.set_format(new_sheet, row_len)

    return new_sheet_url
