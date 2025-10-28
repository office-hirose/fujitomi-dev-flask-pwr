# -------------------------------------------------------------------
#  DW SOMPOひまわり生命
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
    syoken = 18  # col R 証券番号
    fee_withtax = 32  # col AF 税込
    tax = 33  # col AG 消費税額
    temp1 = 37  # col AK 保険年度
    temp2 = 7  # col G 成立年月
    temp3 = 38  # col AL 保険年度内回数

    # syokenデータを2行目から取得
    y = 2 - 1
    row_len = len(original_sheet.col_values(syoken)[y:]) + 1

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

    # 証券番号
    syoken_data = original_sheet.col_values(syoken)[y:]
    cell_list = new_sheet.range(f"F2:F{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = syoken_data[i].replace("*", "")  # replace '*' with ''
    new_sheet.update_cells(cell_list)  # update

    # 税込 H
    fee_data = original_sheet.col_values(fee_withtax)[y:]
    cell_list = new_sheet.range(f"H2:H{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = int(fee_data[i].replace(",", ""))
        except ValueError:
            print(f"Unable to convert '{fee_data[i]}' to a number")
    new_sheet.update_cells(cell_list)  # update

    # 消費税額 J
    tax_data = original_sheet.col_values(tax)[y:]
    cell_list = new_sheet.range(f"J2:J{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = int(tax_data[i].replace(",", ""))
        except ValueError:
            print(f"Unable to convert '{tax_data[i]}' to a number")
    new_sheet.update_cells(cell_list)  # update

    # 税抜 I
    cell_list_H = new_sheet.range(f"H2:H{row_len}")  # 税込
    cell_list_J = new_sheet.range(f"J2:J{row_len}")  # 消費税額
    cell_list_I = new_sheet.range(f"I2:I{row_len}")  # 税抜
    for i, cell in enumerate(cell_list_I):
        temp_fee_withtax = int(cell_list_H[i].value)
        temp_tax_num = int(cell_list_J[i].value)
        cell.value = temp_fee_withtax - temp_tax_num  # 税抜をセルに追加
    new_sheet.update_cells(cell_list_I)  # update

    # 保険年度 N
    new_sheet.update_cell(1, 14, "保険年度")
    temp1_data = original_sheet.col_values(temp1)[y:]
    cell_list = new_sheet.range(f"N2:N{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp1_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 成立年月 O
    new_sheet.update_cell(1, 15, "成立年月")
    temp2_data = original_sheet.col_values(temp2)[y:]
    cell_list = new_sheet.range(f"O2:O{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp2_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 保険年度内回数 P
    new_sheet.update_cell(1, 16, "保険年度内回数")
    temp3_data = original_sheet.col_values(temp3)[y:]
    cell_list = new_sheet.range(f"P2:P{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp3_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 初年度次年度：参照=N列：セット=M列：1以下=1、2以上=2、それ以外=0
    cell_list_N = new_sheet.range(f"N2:N{row_len}")  # 保険年度
    cell_list_M = new_sheet.range(f"M2:M{row_len}")  # 初年度次年度
    for i, cell in enumerate(cell_list_N):
        #
        if cell.value is not None and cell.value.strip() != "":
            if int(cell.value) <= 1:
                cell_list_M[i].value = 1
            elif int(cell.value) >= 2:
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
