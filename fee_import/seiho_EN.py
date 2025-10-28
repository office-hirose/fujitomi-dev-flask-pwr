# -------------------------------------------------------------------
#  EN FWD生命
# -------------------------------------------------------------------
from gspread_formatting import format_cell_range
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

    # 区分でSORTしてブランクを取り込む。証券番号は前ゼロ10桁で埋める。「手数料」は税込なので計算必要。
    # 初年度次年度=代手種類と年度回目から想定する。

    syoken = 4  # col D 証券番号・変換前
    fee_withtax = 13  # col M 手数料税込
    temp1 = 12  # col L 代手種類
    temp2 = 10  # col J 年度回目

    # syokenデータを2行目から取得
    y = 2 - 1
    row_len = len(original_sheet.col_values(syoken)[y:]) + 1

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

    # 証券番号・変換前 N
    new_sheet.update_cell(1, 14, "証券番号・変換前")
    syoken_data = original_sheet.col_values(syoken)[y:]
    cell_list = new_sheet.range(f"N2:N{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = syoken_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 代手種類 O
    new_sheet.update_cell(1, 15, "代手種類")
    temp1_data = original_sheet.col_values(temp1)[y:]
    cell_list = new_sheet.range(f"O2:O{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = temp1_data[i]
        except ValueError:
            print(f"Unable to convert '{temp1_data[i]}'")
    new_sheet.update_cells(cell_list)  # update

    # 年度回目を回目に入れる L
    temp2_data = original_sheet.col_values(temp2)[y:]
    cell_list = new_sheet.range(f"L2:L{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = temp2_data[i]
        except ValueError:
            print(f"Unable to convert '{temp2_data[i]}'")
    new_sheet.update_cells(cell_list)  # update

    # 証券番号を前ゼロ10桁で埋める
    cell_list_N = new_sheet.range(f"N2:N{row_len}")  # 証券番号・変換前
    values_F = []
    for i, cell in enumerate(cell_list_N):
        try:
            value_N = str(cell_list_N[i].value)
        except ValueError:
            print(f"Row {i+2}: Invalid error format")
            continue  # 次のループへ

        if len(value_N) < 10:
            value_N = "0" * (10 - len(value_N)) + value_N

        value_F = value_N  # 証券番号・変換後
        values_F.append(value_F)  # 証券番号をリストに追加

    # 証券番号 F
    cell_list_F = new_sheet.range(f"F2:F{row_len}")
    for i, cell in enumerate(cell_list_F):
        cell.value = values_F[i]
    new_sheet.update_cells(cell_list_F)  # update

    # 税込 H
    fee_data = original_sheet.col_values(fee_withtax)[y:]
    cell_list = new_sheet.range(f"H2:H{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = int(fee_data[i].replace(",", ""))
        except ValueError:
            print(f"Unable to convert '{fee_data[i]}' to a number")
    new_sheet.update_cells(cell_list)  # update

    # 手数料税抜計算
    cell_list_H = new_sheet.range(f"H2:H{row_len}")  # 税込
    values_I = []
    for i, cell in enumerate(cell_list_H):
        try:
            value_H = int(cell_list_H[i].value)
        except ValueError:
            print(f"Row {i+2}: Invalid number format")
            continue  # 次のループへ
        value_I = int(float(value_H) / 1.1)  # 税抜  小数点以下切り捨て
        values_I.append(value_I)  # 税抜をリストに追加

    # 税抜 I
    cell_list_I = new_sheet.range(f"I2:I{row_len}")
    for i, cell in enumerate(cell_list_I):
        cell.value = values_I[i]
    new_sheet.update_cells(cell_list_I)  # update

    # 消費税額 J
    cell_list_H = new_sheet.range(f"H2:H{row_len}")  # 税込
    cell_list_I = new_sheet.range(f"I2:I{row_len}")  # 税抜
    cell_list_J = new_sheet.range(f"J2:J{row_len}")  # 消費税額
    for i, cell in enumerate(cell_list_J):
        cell.value = int(cell_list_H[i].value) - int(cell_list_I[i].value)
    new_sheet.update_cells(cell_list_J)  # update

    # 初年度次年度：参照=O列：セット=M列：Ｌ字初年度=1、Ｌ字継続=2、それ以外=0
    cell_list_O = new_sheet.range(f"O2:O{row_len}")
    cell_list_M = new_sheet.range(f"M2:M{row_len}")
    for i, cell in enumerate(cell_list_O):
        if cell.value is not None and cell.value.strip() != "":
            if cell.value == "Ｌ字初年度":
                cell_list_M[i].value = 1
            elif cell.value == "Ｌ字継続":
                cell_list_M[i].value = 2
            else:
                cell_list_M[i].value = 0
        else:
            cell_list_M[i].value = 0

        # 値が0の時に背景色をピンクに設定
        if cell_list_M[i].value == 0:
            format_cell_range(new_sheet, f"M{i+2}", cell_pink)

    new_sheet.update_cells(cell_list_M)  # update

    # Set format
    SET_BASIC.set_format(new_sheet, row_len)

    return new_sheet_url
