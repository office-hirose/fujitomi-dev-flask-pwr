# -------------------------------------------------------------------
#  EQ マニュライフ生命
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

    # 証券番号は、種類コード(３桁)＋証券番号(前ゼロ７桁)＝証券番号(10桁)に統一する、「手数料」が手数料税抜。
    # 初年度次年度、内訳と契約年月日から想定する。マネジメント手数料は「2」次年度以降にセット。

    kind = 12  # col L 種類コード
    syoken = 13  # col M 証券番号
    fee_notax = 26  # col Z 手数料税抜
    temp1 = 21  # col U 入金回数
    temp2 = 28  # col AB 内訳
    temp3 = 14  # col N 契約年月日

    # syokenデータを2行目から取得
    y = 2 - 1
    row_len = len(original_sheet.col_values(syoken)[y:]) + 1

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

    # 種類コード
    new_sheet.update_cell(1, 14, "種類コード")
    kind_data = original_sheet.col_values(kind)[y:]
    cell_list = new_sheet.range(f"N2:N{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = kind_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 証券番号・変換前 O
    new_sheet.update_cell(1, 15, "証券番号・変換前")
    syoken_data = original_sheet.col_values(syoken)[y:]
    cell_list = new_sheet.range(f"O2:O{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = syoken_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 税抜 I
    fee_data = original_sheet.col_values(fee_notax)[y:]
    cell_list = new_sheet.range(f"I2:I{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = int(fee_data[i].replace(",", ""))
        except ValueError:
            print(f"Unable to convert '{fee_data[i]}' to a number")
    new_sheet.update_cells(cell_list)  # update

    # 税込 H
    cell_list_H = new_sheet.range(f"H2:H{row_len}")  # 税込
    cell_list_I = new_sheet.range(f"I2:I{row_len}")  # 税抜
    cell_list_K = new_sheet.range(f"K2:K{row_len}")  # 消費税率
    for i, cell in enumerate(cell_list_H):
        temp_tax_per = (int(cell_list_K[i].value) / 100) + 1  # 消費税率
        cell.value = round(int(cell_list_I[i].value) * (temp_tax_per))  # 税込
    new_sheet.update_cells(cell_list_H)  # update

    # 消費税額 J
    cell_list_H = new_sheet.range(f"H2:H{row_len}")  # 税込
    cell_list_I = new_sheet.range(f"I2:I{row_len}")  # 税抜
    cell_list_J = new_sheet.range(f"J2:J{row_len}")  # 消費税額
    for i, cell in enumerate(cell_list_J):
        cell.value = int(cell_list_H[i].value) - int(cell_list_I[i].value)
    new_sheet.update_cells(cell_list_J)  # update

    # 入金回数を回目に入れる
    temp1_data = original_sheet.col_values(temp1)[y:]
    cell_list = new_sheet.range(f"L2:L{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = temp1_data[i]
        except ValueError:
            print(f"Unable to convert '{temp1_data[i]}'")
    new_sheet.update_cells(cell_list)  # update

    # 内訳 P
    new_sheet.update_cell(1, 16, "内訳")
    temp2_data = original_sheet.col_values(temp2)[y:]
    cell_list = new_sheet.range(f"P2:P{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = temp2_data[i]
        except ValueError:
            print(f"Unable to convert '{temp2_data[i]}'")
    new_sheet.update_cells(cell_list)  # update

    # 契約年月日 Q
    new_sheet.update_cell(1, 17, "契約年月日")
    temp3_data = original_sheet.col_values(temp3)[y:]
    cell_list = new_sheet.range(f"Q2:Q{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = temp3_data[i]
        except ValueError:
            print(f"Unable to convert '{temp3_data[i]}'")
    new_sheet.update_cells(cell_list)  # update

    # 種類コード + 証券番号を前ゼロ7桁で埋める
    cell_list_N = new_sheet.range(f"N2:N{row_len}")  # 種類コード
    cell_list_O = new_sheet.range(f"O2:O{row_len}")  # 証券番号・変換前
    values_F = []
    for i, cell in enumerate(cell_list_N):
        try:
            value_N = str(cell_list_N[i].value)
            value_O = str(cell_list_O[i].value)
        except ValueError:
            print(f"Row {i+2}: Invalid error format")
            continue  # 次のループへ

        if len(value_O) < 7:
            value_O = "0" * (7 - len(value_O)) + value_O

        value_F = value_N + value_O  # 種類コード + 証券番号・変換後
        values_F.append(value_F)  # 証券番号をリストに追加

    # 証券番号 F Update cells in bulk
    cell_list_F = new_sheet.range(f"F2:F{row_len}")
    for i, cell in enumerate(cell_list_F):
        cell.value = values_F[i]
    new_sheet.update_cells(cell_list_F)  # update

    # 初年度次年度：参照=P列：セット=M列：初年度手数料=1、戻入手数料=1、継続手数料=2、マネジメント手数料(R)=2、それ以外=0
    cell_list_P = new_sheet.range(f"P2:P{row_len}")
    cell_list_M = new_sheet.range(f"M2:M{row_len}")
    for i, cell in enumerate(cell_list_P):
        if cell.value is not None and cell.value.strip() != "":
            if cell.value == "初年度手数料":
                cell_list_M[i].value = 1
            elif cell.value == "戻入手数料":
                cell_list_M[i].value = 1
                format_cell_range(new_sheet, f"M{i+2}", cell_pink)  # ピンク
            elif cell.value == "継続手数料":
                cell_list_M[i].value = 2
            elif cell.value == "マネジメント手数料(R)":
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
