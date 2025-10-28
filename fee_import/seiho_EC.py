# -------------------------------------------------------------------
#  EC エヌエヌ生命
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
    syoken = 12  # col L 証券番号
    fee_notax = 30  # col AD 手数料税抜、「手数料 (円）」が手数料税抜
    temp1 = 8  # col H 手数料区分

    # syokenデータの2行目から長さを取得
    y = 2 - 1
    row_len = len(original_sheet.col_values(syoken)[y:]) + 1

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

    # 証券番号 F
    syoken_data = original_sheet.col_values(syoken)[y:]
    cell_list = new_sheet.range(f"F2:F{row_len}")
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

    # 手数料区分 N
    new_sheet.update_cell(1, 14, "手数料区分")
    temp1_data = original_sheet.col_values(temp1)[y:]
    cell_list = new_sheet.range(f"N2:N{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = temp1_data[i]
        except ValueError:
            print(f"Unable to convert '{temp1_data[i]}'")
    new_sheet.update_cells(cell_list)  # update

    # 初年度次年度：参照=N列：セット=M列：初年度手数料（初回を除く）=1, 次年度以降手数料=2、早期失効解約等戻入=1, それ以外=0
    cell_list_N = new_sheet.range(f"N2:N{row_len}")
    cell_list_M = new_sheet.range(f"M2:M{row_len}")
    for i, cell in enumerate(cell_list_N):
        if cell.value is not None and cell.value.strip() != "":
            if cell.value == "初年度手数料（初回を除く）":
                cell_list_M[i].value = 1
            elif cell.value == "次年度以降手数料":
                cell_list_M[i].value = 2
            elif cell.value == "早期失効解約等戻入":
                cell_list_M[i].value = 1
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
