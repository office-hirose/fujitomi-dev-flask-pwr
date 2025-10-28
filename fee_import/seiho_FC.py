# -------------------------------------------------------------------
#  FC メットライフ生命
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

    # 「手数料（単位円）」が手数料税抜。
    # 【初年度次年度/難易度=高】手数料種別と契約年月日から想定する。

    syoken = 10  # col J 証券番号
    fee_notax = 18  # col R 手数料税抜
    temp1 = 21  # col U 手数料種別
    temp2 = 12  # col L 契約年月日

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
    cell_list_M = new_sheet.range(f"K2:K{row_len}")  # 消費税率
    for i, cell in enumerate(cell_list_H):
        temp_tax_per = (int(cell_list_M[i].value) / 100) + 1  # 消費税率
        cell.value = round(int(cell_list_I[i].value) * (temp_tax_per))  # 税込
    new_sheet.update_cells(cell_list_H)  # update

    # 消費税額 J
    cell_list_H = new_sheet.range(f"H2:H{row_len}")  # 税込
    cell_list_I = new_sheet.range(f"I2:I{row_len}")  # 税抜
    cell_list_J = new_sheet.range(f"J2:J{row_len}")  # 消費税額
    for i, cell in enumerate(cell_list_J):
        cell.value = int(cell_list_H[i].value) - int(cell_list_I[i].value)
    new_sheet.update_cells(cell_list_J)  # update

    # 手数料種別 N
    new_sheet.update_cell(1, 14, "手数料種別")
    temp1_data = original_sheet.col_values(temp1)[y:]
    cell_list = new_sheet.range(f"N2:N{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp1_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 契約年月日 O
    new_sheet.update_cell(1, 15, "契約年月日")
    temp2_data = original_sheet.col_values(temp2)[y:]
    cell_list = new_sheet.range(f"O2:O{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = temp2_data[i]
    new_sheet.update_cells(cell_list)  # update

    # 新契約 = 1
    # 初年度2回目以降 = 1または2
    # グループ初年度コミッション = 1
    # 次年度以降 = 2
    # グループ次年度コミッション = 2
    # 第二保険年度追加手数料 = 2

    # 同じ証券番号でも初年度、次年度の場合あり。
    # 例として「初年度2回目以降」は次年度扱いの場合もある。
    # 理由は、満期を延長しているから。
    # なので、「初年度2回目以降」はこのクエリで確認する。

    # ChatGPT あなたはプログラムの先生です。下記のSQLに証券番号を当てはめてSQLを完成させてください

    # SELECT syoken_cd_main, gyotei1_cd
    # FROM sql_order_store
    # WHERE
    # syoken_cd_main = 証券番号 OR

    # -証券番号
    # 3X15036928(sample)
    # 3X15036930(sample)

    # 初年度次年度：参照=N列：セット=M列：初年度=1、戻入=1、次年度=2、それ以外=0
    cell_list_N = new_sheet.range(f"N2:N{row_len}")
    cell_list_M = new_sheet.range(f"M2:M{row_len}")
    for i, cell in enumerate(cell_list_N):
        if cell.value is not None and cell.value.strip() != "":
            if cell.value == "新契約":
                cell_list_M[i].value = 1
            elif cell.value == "初年度2回目以降":
                cell_list_M[i].value = 1
                format_cell_range(new_sheet, f"M{i+2}", cell_pink)  # ピンク
            elif cell.value == "グループ初年度コミッション":
                cell_list_M[i].value = 1
            elif cell.value == "次年度以降":
                cell_list_M[i].value = 2
            elif cell.value == "グループ次年度コミッション":
                cell_list_M[i].value = 2
            elif cell.value == "第二保険年度追加手数料":
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
