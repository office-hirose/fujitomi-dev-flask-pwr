from _mod import mod_datetime

from gspread_formatting import CellFormat, Color, TextFormat, format_cell_range


# シート情報
def set_sheet_config(sheet_dic):
    # original file, original sheet
    spreadsheet_file = sheet_dic["spreadsheet_file"]
    original_sheet = spreadsheet_file.sheet1

    # new_sheet_name
    new_sheet_name = "import_" + mod_datetime.mz_tnow("for_datetime_underbar")

    # new_sheet
    new_sheet = spreadsheet_file.add_worksheet(title=new_sheet_name, rows="10", cols="20")

    # セルの幅
    col_widths = {
        1: 60,  # A
        2: 60,  # B
        3: 60,  # C
        4: 80,  # D
        5: 100,  # E
        6: 120,  # F
        7: 40,  # G
        8: 70,  # H
        9: 70,  # I
        10: 60,  # J
        11: 60,  # K
        12: 40,  # L
        13: 90,  # M
        14: 120,  # N 以降は、テンポラリー、空白
        15: 120,  # O
        16: 120,  # P
        17: 120,  # Q
        18: 120,  # R
        19: 120,  # S
        20: 120,  # T
    }

    # 列の幅を設定するためのリクエストを作成
    requests = []
    for col, width in col_widths.items():
        requests.append(
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": new_sheet.id,
                        "dimension": "COLUMNS",
                        "startIndex": col - 1,  # 0から始まるインデックス
                        "endIndex": col,
                    },
                    "properties": {"pixelSize": width},
                    "fields": "pixelSize",
                }
            }
        )

    # リクエストを実行
    spreadsheet_file.batch_update({"requests": requests})

    # new_sheet URL
    new_sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_file.id}/edit#gid={new_sheet.id}"

    return original_sheet, new_sheet, new_sheet_url


# ヘッダー
def set_header(new_sheet):
    header_data = [
        "入金年度",
        "入金年月",
        "保険分類\n1=生保\n2=損保\n3=少短",
        "保険会社CD",
        "手数料種類\n1=通常\n2=口座振替など",
        "証券番号",
        "枝番",
        "税込",
        "税抜",
        "消費税額",
        "消費税率",
        "回目",
        "初年度次年度\n0=不明\n1=初年度\n2=次年度以降",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ]
    header_cell_list = new_sheet.range("A1:T1")
    for i, cell in enumerate(header_cell_list):
        cell.value = header_data[i]
    new_sheet.update_cells(header_cell_list)
    new_sheet.freeze(1)  # 1行目を固定

    # ヘッダーの書式設定
    fmt_header = CellFormat(
        backgroundColor=Color(1, 1, 0),  # RGB color for yellow
        textFormat=TextFormat(fontSize=9, fontFamily="Arial"),
        horizontalAlignment="LEFT",
        verticalAlignment="MIDDLE",
    )
    format_cell_range(new_sheet, "A1:T1", fmt_header)

    # Set background color of cell N1:T1 to white
    fmt_color = CellFormat(backgroundColor=Color(1, 1, 1))
    format_cell_range(new_sheet, "N1:T1", fmt_color)

    return


# 基本項目
def set_body(new_sheet, sheet_dic, row_len):
    # nyu_nendo - 基本全て同じ
    cell_list = new_sheet.range(f"A2:A{row_len}")
    for cell in cell_list:
        cell.value = sheet_dic["nyu_nendo"]
    new_sheet.update_cells(cell_list)

    # nyu_date - 基本全て同じ
    cell_list = new_sheet.range(f"B2:B{row_len}")
    for cell in cell_list:
        cell.value = sheet_dic["nyu_date"]
    new_sheet.update_cells(cell_list)

    # cat_cd - 基本全て同じ
    cell_list = new_sheet.range(f"C2:C{row_len}")
    for cell in cell_list:
        cell.value = int(sheet_dic["cat_cd"])
    new_sheet.update_cells(cell_list)

    # coltd_cd - 基本全て同じ、一部を除く
    cell_list = new_sheet.range(f"D2:D{row_len}")
    for cell in cell_list:
        cell.value = sheet_dic["coltd_cd"]
    new_sheet.update_cells(cell_list)

    # kind_cd - 基本全て同じ
    cell_list = new_sheet.range(f"E2:E{row_len}")
    for cell in cell_list:
        cell.value = int(sheet_dic["kind_cd"])
    new_sheet.update_cells(cell_list)

    # syoken_cd_sub - 基本全て同じ、一部を除く
    cell_list = new_sheet.range(f"G2:G{row_len}")
    for cell in cell_list:
        cell.value = sheet_dic["syoken_cd_sub"]
    new_sheet.update_cells(cell_list)

    # fee_withtax - 基本全て同じ、一部を除く
    cell_list = new_sheet.range(f"H2:H{row_len}")
    for cell in cell_list:
        cell.value = int(sheet_dic["fee_withtax"])
    new_sheet.update_cells(cell_list)

    # fee_tax_num - 基本全て同じ、一部を除く
    cell_list = new_sheet.range(f"J2:J{row_len}")
    for cell in cell_list:
        cell.value = int(sheet_dic["fee_tax_num"])
    new_sheet.update_cells(cell_list)

    # fee_tax_per - 基本全て同じ、一部を除く
    cell_list = new_sheet.range(f"K2:K{row_len}")
    for cell in cell_list:
        cell.value = int(sheet_dic["fee_tax_per"])
    new_sheet.update_cells(cell_list)

    return


# 書式を全てにセット
def set_format(new_sheet, row_len):
    # Set the font, font size, alignment for all cells
    fmt_all = CellFormat(
        textFormat=TextFormat(fontSize=10, fontFamily="Arial"),
        horizontalAlignment="LEFT",
        verticalAlignment="MIDDLE",
    )
    format_cell_range(new_sheet, "A2:T" + str(row_len), fmt_all)

    # 実収手数料の列、数字のフォーマット
    # fmt_number = cellFormat(numberFormat=numberFormat("NUMBER", pattern="###0"))
    # format_cell_range(new_sheet, "H2:H" + str(row_len), fmt_number)

    return


# セルのカラー
def set_cell_color():
    # イエロー
    cell_yellow = CellFormat(
        backgroundColor=Color(1.0, 1.0, 0.0),
    )
    # ピンク
    cell_pink = CellFormat(
        backgroundColor=Color(1.0, 0.4, 0.7),
    )
    return cell_yellow, cell_pink
