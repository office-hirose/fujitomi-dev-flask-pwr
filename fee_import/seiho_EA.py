# -------------------------------------------------------------------
#  EA オリックス生命
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

    # 手数料額ー手数料消費税＝手数料税抜
    # 支払年度区分名と支払月数から想定する。初年度でも支払月数が13以上の場合あり注意。

    syoken = 14  # col N 証券番号
    fee_withtax = 25  # col Y 手数料額　税込
    fee_tax_num = 26  # col Z 手数料消費税　消費税額
    temp1 = 12  # col L 支払年度区分名
    temp2 = 30  # col AD 支払月数

    # syokenデータを2行目から取得
    y = 2 - 1
    row_len = len(original_sheet.col_values(syoken)[y:]) + 1

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

    # 証券番号
    syoken_data = original_sheet.col_values(syoken)[y:]
    cell_list = new_sheet.range(f"F2:F{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = syoken_data[i]
    new_sheet.update_cells(cell_list)

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
    tax_data = original_sheet.col_values(fee_tax_num)[y:]
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
        cell.value = int(cell_list_H[i].value) - int(cell_list_J[i].value)  # 税抜
    new_sheet.update_cells(cell_list_I)  # update

    # 支払年度区分名
    new_sheet.update_cell(1, 14, "支払年度区分名")
    temp1_data = original_sheet.col_values(temp1)[y:]
    cell_list = new_sheet.range(f"N2:N{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp1_data[i]
    new_sheet.update_cells(cell_list)

    # 支払月数
    new_sheet.update_cell(1, 15, "支払月数")
    temp2_data = original_sheet.col_values(temp2)[y:]
    cell_list = new_sheet.range(f"O2:O{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp2_data[i]
    new_sheet.update_cells(cell_list)

    # 初年度次年度：参照=N列：セット=M列：初年度=1、次年度以降=2、それ以外=0
    cell_list_N = new_sheet.range(f"N2:N{row_len}")
    cell_list_M = new_sheet.range(f"M2:M{row_len}")
    for i, cell in enumerate(cell_list_N):
        if cell.value is not None and cell.value.strip() != "":
            if cell.value == "初年度":
                cell_list_M[i].value = 1
            elif cell.value == "次年度以降":
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
