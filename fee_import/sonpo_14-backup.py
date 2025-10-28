# -------------------------------------------------------------------
#  14 日新火災
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

    # -----------------------------------------------------------------------
    # 保険会社別設定
    # -----------------------------------------------------------------------

    syoken = 9  # col I 証券番号
    fee_withtax = 16  # col P 税込
    kaime = 12  # col L 回目
    tori_num = 21  # col U 取扱手数料、手数料種類を判定する、一部例外あり。0円以外は振替費用

    # syokenデータを2行目から取得
    y = 2 - 1
    row_len = len(original_sheet.col_values(syoken)[y:]) + 1

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

    # original sheet
    syoken_data = original_sheet.col_values(syoken)[y:]
    fee_withtax_data = original_sheet.col_values(fee_withtax)[y:]
    kaime_data = original_sheet.col_values(kaime)[y:]
    tori_num_data = original_sheet.col_values(tori_num)[y:]

    # new sheet
    cell_list_E = new_sheet.range(f"E2:E{row_len}")  # 手数料種類
    cell_list_F = new_sheet.range(f"F2:F{row_len}")  # 証券番号
    cell_list_L = new_sheet.range(f"L2:L{row_len}")  # 回目
    cell_list_H = new_sheet.range(f"H2:H{row_len}")  # 税込
    cell_list_I = new_sheet.range(f"I2:I{row_len}")  # 税抜
    cell_list_J = new_sheet.range(f"J2:J{row_len}")  # 消費税額
    cell_list_M = new_sheet.range(f"M2:M{row_len}")  # 初年度次年度
    cell_list_N = new_sheet.range(f"N2:N{row_len}")  # 取扱手数料
    new_sheet.update_cell(1, 14, "取扱手数料")

    # リストにセットする
    for i in range(len(syoken_data)):
        # 証券番号 F
        syoken_value = str(syoken_data[i])
        if syoken_value is not None and syoken_value.strip() != "":
            cell_list_F[i].value = syoken_value
        else:
            cell_list_F[i].value = ""

        # 税込 H
        try:
            cell_list_H[i].value = int(fee_withtax_data[i].replace(",", ""))
        except ValueError:
            print(f"Unable to convert '{fee_withtax_data[i]}' to a number")

        # 回目 L
        kaime_value = str(kaime_data[i])
        if kaime_value is not None and kaime_value.strip() != "":
            cell_list_L[i].value = kaime_value
        else:
            cell_list_L[i].value = ""

        # 税抜 I
        cell_list_I[i].value = int(round(cell_list_H[i].value) / 1.1)

        # 消費税額 J
        cell_list_J[i].value = int(cell_list_H[i].value) - int(cell_list_I[i].value)

        # 初年度次年度 M
        cell_list_M[i].value = 0

        # 取扱手数料 N
        try:
            cell_list_N[i].value = int(tori_num_data[i].replace(",", ""))
        except ValueError:
            print(f"Unable to convert '{tori_num_data[i]}' to a number")

        # 手数料種類 E
        if int(cell_list_N[i].value) == 0:
            cell_list_E[i].value = 1
        else:
            cell_list_E[i].value = 2

    # update
    new_sheet.update_cells(cell_list_E)
    new_sheet.update_cells(cell_list_F)
    new_sheet.update_cells(cell_list_L)
    new_sheet.update_cells(cell_list_H)
    new_sheet.update_cells(cell_list_I)
    new_sheet.update_cells(cell_list_J)
    new_sheet.update_cells(cell_list_M)
    new_sheet.update_cells(cell_list_N)

    # 手数料種類 E が 2 の場合は背景色をピンクにする。しかし、Google API 制限オーバーとなる。
    # kind_data = new_sheet.col_values(5)[y:]
    # for i in range(len(kind_data)):
    #     kind_value = int(kind_data[i])
    #     if kind_value == 2:
    #         format_cell_range(new_sheet, f"E{i+2}", cell_pink)

    # Set format
    SET_BASIC.set_format(new_sheet, row_len)

    return new_sheet_url
