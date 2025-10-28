# -------------------------------------------------------------------
#  DU ソニー生命
# -------------------------------------------------------------------
# from gspread_formatting import format_cell_range
from fee_import import set_basic as SET_BASIC


# データ
def set_sheet(sheet_dic):
    # cell color
    cell_yellow, cell_pink = SET_BASIC.set_cell_color()

    # Set sheet config
    original_sheet, new_sheet, new_sheet_url = SET_BASIC.set_sheet_config(sheet_dic)

    # Set header
    SET_BASIC.set_header(new_sheet)

    # 保険会社別設定
    syoken = 9  # col I 証券番号
    fee_withtax_temp = 23  # col W 税込
    fee_option = 42  # col AP 品質連動手数料税込
    temp1 = 14  # col N 払方
    temp2 = 15  # col O 入金回数
    temp3 = 29  # col AC 初年度・継続
    temp4 = 10  # col J 契約日

    # syokenデータを3行目から取得
    y = 3 - 1
    row_len = len(original_sheet.col_values(syoken)[y:]) + 1

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

    # tax - 5% 特別、表紙に書いてあるが、消費税調整で帳尻を合わせているらしい。
    cell_list = new_sheet.range(f"K2:K{row_len}")
    for cell in cell_list:
        cell.value = 5
    new_sheet.update_cells(cell_list)  # update

    # 証券番号
    syoken_data = original_sheet.col_values(syoken)[y:]
    cell_list = new_sheet.range(f"F2:F{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = syoken_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 仮税込 in cell N1
    new_sheet.update_cell(1, 14, "仮税込")
    fee_data = original_sheet.col_values(fee_withtax_temp)[y:]
    cell_list = new_sheet.range(f"N2:N{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = int(fee_data[i].replace(",", ""))
        except ValueError:
            print(f"Unable to convert '{fee_data[i]}' to a number")
    new_sheet.update_cells(cell_list)  # update

    # 品質連動手数料税込 in cell O1
    new_sheet.update_cell(1, 15, "品質連動手数料税込")
    fee_option_data = original_sheet.col_values(fee_option)[y:]
    cell_list = new_sheet.range(f"O2:O{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = int(fee_option_data[i].replace(",", ""))
        except ValueError:
            print(f"Unable to convert '{fee_option_data[i]}' to a number")
    new_sheet.update_cells(cell_list)  # update

    # 税込 H1
    cell_list_N = new_sheet.range(f"N2:N{row_len}")  # 仮税込
    cell_list_O = new_sheet.range(f"O2:O{row_len}")  # 品質連動手数料税込
    cell_list_H = new_sheet.range(f"H2:H{row_len}")  # 税込
    for i, cell in enumerate(cell_list_H):
        try:
            # 値が数値でない場合はエラーが発生する
            temp_N = int(cell_list_N[i].value)
            temp_O = int(cell_list_O[i].value)
        except ValueError:
            print(f"Row {i+2}: Invalid number format")
            continue  # 次のループへ

        cell.value = temp_N + temp_O  # 税込をセルに追加
    new_sheet.update_cells(cell_list_H)  # update

    # 税抜 I1
    cell_list_H = new_sheet.range(f"H2:H{row_len}")  # 税込
    cell_list_K = new_sheet.range(f"K2:K{row_len}")  # 消費税率
    cell_list_I = new_sheet.range(f"I2:I{row_len}")  # 税抜

    for i, cell in enumerate(cell_list_I):
        fee_tax_per = cell_list_K[i].value
        temp_tax_per = (int(fee_tax_per) + 100) / 100
        temp_fee_withtax = int(cell_list_H[i].value)
        cell.value = int(round(temp_fee_withtax / temp_tax_per))  # 税抜をセルに追加
    new_sheet.update_cells(cell_list_I)  # update

    # 消費税金額
    # cell_list_J = new_sheet.range(f"J2:J{row_len}")  # 消費税金額
    # for i, cell in enumerate(cell_list_J):
    #     temp_fee_withtax = int(cell_list_H[i].value)
    #     temp_fee_notax = int(cell_list_I[i].value)
    #     cell.value = temp_fee_withtax - temp_fee_notax
    # new_sheet.update_cells(cell_list_J)  # update

    # 払方
    new_sheet.update_cell(1, 16, "払方")
    temp1_data = original_sheet.col_values(temp1)[y:]
    cell_list = new_sheet.range(f"P2:P{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp1_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 入金回数
    new_sheet.update_cell(1, 17, "入金回数")
    temp2_data = original_sheet.col_values(temp2)[y:]
    cell_list = new_sheet.range(f"Q2:Q{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp2_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 初年度・継続
    new_sheet.update_cell(1, 18, "初年度・継続")
    temp3_data = original_sheet.col_values(temp3)[y:]
    cell_list = new_sheet.range(f"R2:R{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp3_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 契約日
    new_sheet.update_cell(1, 19, "契約日")
    temp4_data = original_sheet.col_values(temp4)[y:]
    cell_list = new_sheet.range(f"S2:S{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp4_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 回目：入金回数と同じ
    temp2_data = original_sheet.col_values(temp2)[y:]
    cell_list = new_sheet.range(f"L2:L{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp2_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 初年度次年度：参照=R列：セット=M列：初年度=1、継続=2、それ以外=0
    cell_list_R = new_sheet.range(f"R2:R{row_len}")
    cell_list_M = new_sheet.range(f"M2:M{row_len}")
    for i, cell in enumerate(cell_list_R):
        if cell.value is not None and cell.value.strip() != "":
            if cell.value == "初年度":
                cell_list_M[i].value = 1
            elif cell.value == "継続":
                cell_list_M[i].value = 2
            else:
                cell_list_M[i].value = 0
        else:
            cell_list_M[i].value = 0

        # 値が0,1の時に背景色をピンクに設定、APIの負荷エラーとなるので、コメントアウト
        # if cell_list_M[i].value == 0 or cell_list_M[i].value == 1:
        #     format_cell_range(new_sheet, f"M{i+2}", cell_pink)

    new_sheet.update_cells(cell_list_M)  # update

    # Set format
    SET_BASIC.set_format(new_sheet, row_len)

    return new_sheet_url
