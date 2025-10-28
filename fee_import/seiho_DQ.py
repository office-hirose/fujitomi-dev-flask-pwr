# -------------------------------------------------------------------
#  DQ ジブラルタ生命
# -------------------------------------------------------------------
from gspread_formatting import format_cell_range
from datetime import datetime, timedelta
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
    syoken = 7  # col G
    fee_withtax = 22  # col v 税込
    fee_notax = 23  # col W 税抜
    fee_tax_num = 24  # col x 消費税額
    temp1 = 16  # col P 払方区分名称
    temp2 = 19  # col S 支払回数
    temp3 = 6  # col F 契約年月日
    temp4 = 5  # col E 成立年月 データバグありの場合があるので参考程度にする

    # syokenデータを4行目から取得
    y = 4 - 1
    row_len = len(original_sheet.col_values(syoken)[y:]) + 1

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

    # 証券番号
    syoken_data = original_sheet.col_values(syoken)[y:]
    cell_list = new_sheet.range(f"F2:F{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = syoken_data[i]
    new_sheet.update_cells(cell_list)

    # 税込
    fee_data = original_sheet.col_values(fee_withtax)[y:]
    cell_list = new_sheet.range(f"H2:H{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = int(fee_data[i].replace(",", ""))
        except ValueError:
            print(f"Unable to convert '{fee_data[i]}' to a number")
    new_sheet.update_cells(cell_list)

    # 税抜
    fee_data = original_sheet.col_values(fee_notax)[y:]
    cell_list = new_sheet.range(f"I2:I{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = int(fee_data[i].replace(",", ""))
        except ValueError:
            print(f"Unable to convert '{fee_data[i]}' to a number")
    new_sheet.update_cells(cell_list)

    # 消費税
    fee_data = original_sheet.col_values(fee_tax_num)[y:]
    cell_list = new_sheet.range(f"J2:J{row_len}")
    for i, cell in enumerate(cell_list):
        try:
            cell.value = int(fee_data[i].replace(",", ""))
        except ValueError:
            print(f"Unable to convert '{fee_data[i]}' to a number")
    new_sheet.update_cells(cell_list)

    # Set title '払方区分名称' in cell N1
    new_sheet.update_cell(1, 14, "払方区分名称")

    # Set title '支払回数' in cell O1
    new_sheet.update_cell(1, 15, "支払回数")

    # Set title '契約年月日' in cell P1
    new_sheet.update_cell(1, 16, "契約年月日")

    # Set title '成立年月' in cell Q1
    new_sheet.update_cell(1, 17, "成立年月")

    # Set data '払方区分名称'
    temp1_data = original_sheet.col_values(temp1)[y:]
    cell_list = new_sheet.range(f"N2:N{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp1_data[i]
    new_sheet.update_cells(cell_list)

    # Set data '支払回数'
    temp2_data = original_sheet.col_values(temp2)[y:]
    cell_list = new_sheet.range(f"O2:O{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp2_data[i]
    new_sheet.update_cells(cell_list)

    # Set data '契約年月日'
    temp3_data = original_sheet.col_values(temp3)[y:]
    cell_list = new_sheet.range(f"P2:P{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp3_data[i]
    new_sheet.update_cells(cell_list)

    # Set data '成立年月'
    temp4_data = original_sheet.col_values(temp4)[y:]
    cell_list = new_sheet.range(f"Q2:Q{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp4_data[i]
    new_sheet.update_cells(cell_list)

    # Set data '回目' 支払回数と同じ
    temp2_data = original_sheet.col_values(temp2)[y:]
    cell_list = new_sheet.range(f"L2:L{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp2_data[i]
    new_sheet.update_cells(cell_list)

    # 初年度次年度：セルL列、セルM列、セルN列を参照して、セルK列に値を入れる
    cell_list_M = new_sheet.range(f"M2:M{row_len}")  # 初年度次年度
    cell_list_N = new_sheet.range(f"N2:N{row_len}")  # 払方区分名称
    cell_list_O = new_sheet.range(f"O2:O{row_len}")  # 支払回数
    cell_list_P = new_sheet.range(f"P2:P{row_len}")  # 契約年月日

    for i, cell in enumerate(cell_list_N):
        if cell.value is not None and cell.value.strip() != "":
            # 年払
            if cell.value == "年払" and int(cell_list_O[i].value) == 1:
                cell_list_M[i].value = 1
            if cell.value == "年払" and int(cell_list_O[i].value) >= 2:
                cell_list_M[i].value = 2
            # 月払
            if cell.value == "月払" and int(cell_list_O[i].value) <= 12:
                # 契約年月日を日付オブジェクトに変換
                contract_date = datetime.strptime(cell_list_P[i].value, "%Y.%m.%d")
                # 現在日付から1年前の日付を計算
                one_year_ago = datetime.now() - timedelta(days=365)
                # 契約年月日が1年以上前の場合
                if contract_date <= one_year_ago:
                    cell_list_M[i].value = 2
                else:
                    cell_list_M[i].value = 1
                # 目視確認するために、背景色をイエローに設定
                format_cell_range(new_sheet, f"M{i+2}", cell_yellow)
            # 月払
            if cell.value == "月払" and int(cell_list_O[i].value) >= 13:
                cell_list_M[i].value = 2
            # 半年払
            if cell.value == "半年払":
                cell_list_M[i].value = 0
            # 一時払
            if cell.value == "一時払":
                cell_list_M[i].value = 1
                format_cell_range(new_sheet, f"M{i+2}", cell_pink)
        else:
            cell_list_M[i].value = 0

        # 値が0の時に背景色をピンクに設定
        if cell_list_M[i].value == 0:
            format_cell_range(new_sheet, f"M{i+2}", cell_pink)

    new_sheet.update_cells(cell_list_M)

    # Set format
    SET_BASIC.set_format(new_sheet, row_len)

    return new_sheet_url
