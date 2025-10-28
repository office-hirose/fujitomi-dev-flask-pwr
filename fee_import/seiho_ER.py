# -------------------------------------------------------------------
#  ER ネオファースト生命
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

    # "支払額"が、手数料額税抜。証券番号にハイフンが含まれているので削除する。入金回数が回目。
    # 初年度次年度=区分から想定する。

    syoken_cd_main = 7  # col G 証券番号・変換前
    fee_notax = 24  # col X 支払額＝手数料税抜
    fee_modori = 25  # col Y 戻入額
    temp1 = 26  # col Z 入金回数
    temp2 = 27  # col AA 区分

    # syokenデータを2行目から取得
    y = 2 - 1
    row_len = len(original_sheet.col_values(syoken_cd_main)[y:]) + 1

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

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

    # 入金回数を回目に入れる L
    temp1_data = original_sheet.col_values(temp1)[y:]
    cell_list = new_sheet.range(f"L2:L{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp1_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 証券番号・変換前 N
    new_sheet.update_cell(1, 14, "証券番号・変換前")
    syoken_data = original_sheet.col_values(syoken_cd_main)[y:]
    cell_list = new_sheet.range(f"N2:N{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = syoken_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 区分 O
    new_sheet.update_cell(1, 15, "区分")
    temp2_data = original_sheet.col_values(temp2)[y:]
    cell_list = new_sheet.range(f"O2:O{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp2_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 戻入額 P
    new_sheet.update_cell(1, 16, "戻入額")
    fee_modori_data = original_sheet.col_values(fee_modori)[y:]
    cell_list = new_sheet.range(f"P2:P{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = int(fee_modori_data[i].replace(",", ""))
        except ValueError:
            print(f"Unable to convert '{fee_modori_data[i]}' to a number")
    new_sheet.update_cells(cell_list)  # update

    # 証券番号のハイフンを取り除く
    cell_list_N = new_sheet.range(f"N2:N{row_len}")  # 証券番号・変換前
    values_F = []
    for i, cell in enumerate(cell_list_N):
        value_N = str(cell_list_N[i].value)
        value_F = value_N.replace("-", "")  # ハイフンを取り除く
        values_F.append(value_F)  # 証券番号をリストに追加

    cell_list_F = new_sheet.range(f"F2:F{row_len}")
    for i, cell in enumerate(cell_list_F):
        cell.value = values_F[i]
    new_sheet.update_cells(cell_list_F)  # update

    # 初年度次年度：参照=O列：セット=M列：初年度=1、戻入=1、次年度=2、それ以外=0
    cell_list_O = new_sheet.range(f"O2:O{row_len}")
    cell_list_M = new_sheet.range(f"M2:M{row_len}")
    for i, cell in enumerate(cell_list_O):
        if cell.value is not None and cell.value.strip() != "":
            if cell.value == "初年度":
                cell_list_M[i].value = 1
            elif cell.value == "戻入":
                cell_list_M[i].value = 1
                format_cell_range(new_sheet, f"M{i+2}", cell_pink)  # ピンク
            elif cell.value == "次年度":
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
