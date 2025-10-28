# -------------------------------------------------------------------
#  09 東京海上日動火災
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

    # -----------------------------------------------------------------------
    # 保険会社別設定
    # -----------------------------------------------------------------------

    # 「代理店手数料」ー「代手消費税」＝手数料税抜。
    # 枝番は全て0000に置き換える。

    syoken = 13  # col M 証券番号
    fee_withtax = 24  # col X 代理店手数料 税込
    # fee_tax_num = 34  # col AH 代手消費税 しかし使えない
    kaime = 29  # col AC 回目
    komidasi = 37  # col AK 小見出し区分

    # syokenデータを2行目から取得
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

    # 税込 H
    fee_withtax_data = original_sheet.col_values(fee_withtax)[y:]
    cell_list = new_sheet.range(f"H2:H{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = int(fee_withtax_data[i].replace(",", ""))
        except ValueError:
            print(f"Unable to convert '{fee_withtax_data[i]}' to a number")
    new_sheet.update_cells(cell_list)  # update

    # 回目 L、ブランクもCOPYされるようにする
    kaime_data = original_sheet.col_values(kaime)[y:]
    cell_list_L = new_sheet.range(f"L2:L{row_len}")
    for i in range(len(kaime_data)):
        kaime_value = str(kaime_data[i])
        if kaime_value is not None and kaime_value.strip() != "":
            cell_list_L[i].value = kaime_value
        else:
            cell_list_L[i].value = ""
    new_sheet.update_cells(cell_list_L)  # update

    # 小見出し区分 N - 手数料種類を設定するため
    new_sheet.update_cell(1, 14, "手数料種別")
    komidasi_data = original_sheet.col_values(komidasi)[y:]
    cell_list_N = new_sheet.range(f"N2:N{row_len}")
    for i in range(len(komidasi_data)):
        cell_list_N[i].value = str(komidasi_data[i])
    new_sheet.update_cells(cell_list_N)  # update

    # 手数料種類、参照=N列、手数料種類=E列、税率＝K列
    # J=1、通常手数料、10%
    # G=1、通常手数料、10%
    # K=1、通常手数料、10%
    # L=2、振替手数料、10%
    # N=2、振替手数料、10%
    # O=2、振替手数料、10%
    # M=2、振替手数料、0%
    # それ以外=0

    cell_list_E = new_sheet.range(f"E2:E{row_len}")  # 手数料種類
    cell_list_K = new_sheet.range(f"K2:K{row_len}")  # 税率
    cell_list_N = new_sheet.range(f"N2:N{row_len}")  # 小見出し区分

    cell_list_H = new_sheet.range(f"H2:H{row_len}")  # 税込
    cell_list_I = new_sheet.range(f"I2:I{row_len}")  # 税抜
    cell_list_J = new_sheet.range(f"J2:J{row_len}")  # 消費税金額

    for i, cell in enumerate(cell_list_N):
        if cell.value is not None and cell.value.strip() != "":
            if cell.value == "J":
                cell_list_E[i].value = 1
                cell_list_K[i].value = 10
            elif cell.value == "G":
                cell_list_E[i].value = 1
                cell_list_K[i].value = 10
            elif cell.value == "K":
                cell_list_E[i].value = 1
                cell_list_K[i].value = 10
            elif cell.value == "L":
                cell_list_E[i].value = 2
                cell_list_K[i].value = 10
            elif cell.value == "N":
                cell_list_E[i].value = 2
                cell_list_K[i].value = 10
            elif cell.value == "O":
                cell_list_E[i].value = 2
                cell_list_K[i].value = 10
            elif cell.value == "M":
                cell_list_E[i].value = 2
                cell_list_K[i].value = 0
            else:
                cell_list_E[i].value = 0
                cell_list_K[i].value = 10
        else:
            cell_list_E[i].value = 0

        # 消費税金額 J
        if cell.value == "M":
            cell_list_J[i].value = 0
        else:
            cell_list_J[i].value = round(int(cell_list_H[i].value) * 0.1)

        # 税抜 I
        cell_list_I[i].value = int(cell_list_H[i].value) - int(cell_list_J[i].value)

        # 値が0の時に背景色をピンクに設定
        if cell_list_E[i].value == 0:
            format_cell_range(new_sheet, f"E{i+2}", cell_pink)

    new_sheet.update_cells(cell_list_E)  # update
    new_sheet.update_cells(cell_list_K)  # update
    new_sheet.update_cells(cell_list_J)  # update
    new_sheet.update_cells(cell_list_I)  # update

    # 初年度次年度：0
    cell_list = new_sheet.range(f"M2:M{row_len}")
    for cell in cell_list:
        cell.value = 0
    new_sheet.update_cells(cell_list)  # update

    # Set format
    SET_BASIC.set_format(new_sheet, row_len)

    return new_sheet_url
