# -------------------------------------------------------------------
#  17 損保ジャパン
# -------------------------------------------------------------------
# from gspread_formatting import format_cell_range
import jaconv
from fee_import import set_basic as SET_BASIC

# from _mod import mod_decimal


# データ
def set_sheet(sheet_dic):
    # 最初のシートを除く全てのシート名をリストに保存。スライスを使って最初のシートを除外。
    sh = sheet_dic["spreadsheet_file"]
    sheet_name_list = [ws.title for ws in sh.worksheets()[1:]]

    # cell color
    # cell_yellow, cell_pink = SET_BASIC.set_cell_color()

    # Set sheet config
    original_sheet, new_sheet, new_sheet_url = SET_BASIC.set_sheet_config(sheet_dic)

    # Set header
    SET_BASIC.set_header(new_sheet)

    # 保険会社別設定

    # init
    syoken_list_all = []
    eda_list_all = []
    fee_komi_list_all = []
    fee_nuki_list_all = []
    fee_tax_num_list_all = []
    fee_tax_per_list_all = []
    kaime_list_all = []
    name_list_all = []
    cat_list_all = []
    sta_list_all = []

    # main
    (
        sta_list,
        syoken_list,
        eda_list,
        fee_komi_list,
        fee_nuki_list,
        fee_tax_num_list,
        fee_tax_per_list,
        kaime_list,
        cat_list,
        name_list,
    ) = main_exe(original_sheet)

    # all
    sta_list_all = sta_list
    syoken_list_all = syoken_list
    eda_list_all = eda_list
    fee_komi_list_all = fee_komi_list
    fee_nuki_list_all = fee_nuki_list
    fee_tax_num_list_all = fee_tax_num_list
    fee_tax_per_list_all = fee_tax_per_list
    kaime_list_all = kaime_list
    cat_list_all = cat_list
    name_list_all = name_list

    # sub
    for sn in sheet_name_list:
        (
            sta_list,
            syoken_list,
            eda_list,
            fee_komi_list,
            fee_nuki_list,
            fee_tax_num_list,
            fee_tax_per_list,
            kaime_list,
            cat_list,
            name_list,
        ) = sub_exe(sn, sheet_dic["spreadsheet_file"])

        # all
        sta_list_all = sta_list_all + sta_list
        syoken_list_all = syoken_list_all + syoken_list
        eda_list_all = eda_list_all + eda_list
        fee_komi_list_all = fee_komi_list_all + fee_komi_list
        fee_nuki_list_all = fee_nuki_list_all + fee_nuki_list
        fee_tax_num_list_all = fee_tax_num_list_all + fee_tax_num_list
        fee_tax_per_list_all = fee_tax_per_list_all + fee_tax_per_list
        kaime_list_all = kaime_list_all + kaime_list
        cat_list_all = cat_list_all + cat_list
        name_list_all = name_list_all + name_list

    # row_len
    row_len = len(syoken_list_all) + 1

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

    # 証券番号, 回目, cat
    new_sheet.update_cell(1, 14, "cat")
    new_sheet.update_cell(1, 15, "名前")

    sta_cell_list = new_sheet.range(f"E2:E{row_len}")
    syoken_cell_list = new_sheet.range(f"F2:F{row_len}")
    eda_cell_list = new_sheet.range(f"G2:G{row_len}")
    fee_komi_cell_list = new_sheet.range(f"H2:H{row_len}")
    fee_nuki_cell_list = new_sheet.range(f"I2:I{row_len}")
    fee_tax_num_cell_list = new_sheet.range(f"J2:J{row_len}")
    fee_tax_per_cell_list = new_sheet.range(f"K2:K{row_len}")
    kaime_cell_list = new_sheet.range(f"L2:L{row_len}")
    cat_cell_list = new_sheet.range(f"N2:N{row_len}")
    name_cell_list = new_sheet.range(f"O2:O{row_len}")

    # row_len - 1を使用する理由は、syoken_listとsyoken_dataの長さが1つずれているから
    for i in range(row_len - 1):
        sta_cell_list[i].value = int(sta_list_all[i])
        syoken_cell_list[i].value = syoken_list_all[i]
        eda_cell_list[i].value = eda_list_all[i]
        fee_komi_cell_list[i].value = int(fee_komi_list_all[i])
        fee_nuki_cell_list[i].value = int(fee_nuki_list_all[i])
        fee_tax_num_cell_list[i].value = int(fee_tax_num_list_all[i])
        fee_tax_per_cell_list[i].value = int(fee_tax_per_list_all[i])
        kaime_cell_list[i].value = kaime_list_all[i]
        cat_cell_list[i].value = cat_list_all[i]
        name_cell_list[i].value = name_list_all[i]

        # 手数料種類の値が2の時に背景色をピンクに設定、しかしAPIの制限を超えてしまうのか、エラーになる
        # if int(sta_cell_list[i].value) == 2:
        #     format_cell_range(new_sheet, f"E{i+2}", cell_pink)
        # 消費税率の値が10以外の時に背景色をピンクに設定、しかしAPIの制限を超えてしまうのか、エラーになる
        # if int(fee_tax_per_cell_list[i].value) != 10:
        #     format_cell_range(new_sheet, f"K{i+2}", cell_pink)

    # Update cells in bulk
    new_sheet.update_cells(sta_cell_list)
    new_sheet.update_cells(syoken_cell_list)
    new_sheet.update_cells(eda_cell_list)
    new_sheet.update_cells(fee_komi_cell_list)
    new_sheet.update_cells(fee_nuki_cell_list)
    new_sheet.update_cells(fee_tax_num_cell_list)
    new_sheet.update_cells(fee_tax_per_cell_list)
    new_sheet.update_cells(kaime_cell_list)
    new_sheet.update_cells(cat_cell_list)
    new_sheet.update_cells(name_cell_list)

    # 初年度次年度：0
    cell_list = new_sheet.range(f"M2:M{row_len}")
    for cell in cell_list:
        cell.value = 0
    new_sheet.update_cells(cell_list)

    # Set format
    SET_BASIC.set_format(new_sheet, row_len)

    return new_sheet_url


def main_exe(original_sheet):
    # ・契約者名が「ｺｳﾌﾘ」の合計と、別シートの振替手数料の合計を比較確認する。ともに税込。比較差異が数百円程度であればOKとする。
    # ・契約者名が「ｶ-ﾄﾞ ﾃｽｳﾘﾖｳ」は、そのままステータスを2にセットして証券番号を利用する。非課税とする。
    # ・契約者名が「ｺﾝﾋﾞﾆﾄｳ」は、メインのシートから削除する。
    # ・契約者名が「ｺｳﾌﾘ」は、メインのシートから削除する。
    # ・証券番号でSORTする。「全国建設業労災互助会」の98で始まる証券番号の枝番を置き換える。

    # init
    syoken = 11  # col K 証券番号
    # eda = 24  # col x 枝番
    fee_komi = 36  # col AJ 手数料
    kaime = 32  # col AF 分割回目
    name = 28  # col AB 契約者名（漢字）

    # 2行目から取得
    y = 2 - 1

    sta_list = []
    syoken_list = []
    eda_list = []
    fee_komi_list = []
    fee_nuki_list = []
    fee_tax_num_list = []
    fee_tax_per_list = []
    kaime_list = []
    cat_list = []
    name_list = []

    syoken_data = original_sheet.col_values(syoken)[y:]
    fee_komi_data = original_sheet.col_values(fee_komi)[y:]
    kaime_data = original_sheet.col_values(kaime)[y:]
    name_data = original_sheet.col_values(name)[y:]

    # 証券番号などをセットする
    for i in range(len(syoken_data)):  # syoken_dataの長さを基準にする
        syoken_value = str(syoken_data[i])

        # fee_komi_data の範囲チェックと値の取得
        if i < len(fee_komi_data) and fee_komi_data[i] is not None and str(fee_komi_data[i]).replace(",", "").strip():
            fee_komi_value = int(str(fee_komi_data[i]).replace(",", ""))
            fee_nuki_value = int(float(fee_komi_value) / 1.1)  # 小数点以下切り捨て
        else:
            fee_komi_value = 0
            fee_nuki_value = 0

        # kaime_data の範囲チェックと値の取得
        if i < len(kaime_data) and kaime_data[i] is not None:
            kaime_value = str(kaime_data[i])
        else:
            kaime_value = ""

        # name_data の範囲チェックと値の取得
        name_value = ""  # デフォルト値を空文字に
        if i < len(name_data) and name_data[i] is not None and str(name_data[i]).strip():
            current_name_data = name_data[i]
            # jaconv.h2zの呼び出しはcurrent_name_dataがNoneでないことを確認してから行う
            name_value = jaconv.h2z(str(current_name_data), kana=True, digit=False, ascii=False)

        # 空白防止
        if syoken_value is not None and syoken_value.strip() != "":
            # 条件設定
            if "コウフリ" in name_value or "コンビニトウ" in name_value:
                pass
            else:
                fee_komi_list.append(fee_komi_value)
                # fee_tax_num_list.append(fee_tax_num_value)
                kaime_list.append(kaime_value)
                cat_list.append("main")
                name_list.append(name_value)

                if "全国建設業労災互助会" in name_value:
                    # ハイフンの位置を見つける
                    index = syoken_value.find("-")

                    # syoken_valueのハイフン以降を削除して、syoken_resに格納
                    syoken_res = syoken_value[:index]

                    # eda_valueのハイフン以降の数字の前に"0"を付けてedaに格納
                    # eda_res = "0" + syoken_value[index + 1 :]
                    eda_res = "0" + syoken_value[index + 1 :]

                    syoken_list.append(syoken_res)
                    eda_list.append(eda_res)
                else:
                    syoken_list.append(syoken_value)
                    eda_list.append("0000")

                if "カ-ド" in name_value:
                    sta_list.append(2)
                    fee_nuki_list.append(fee_komi_value)
                    fee_tax_num_list.append(0)
                    fee_tax_per_list.append(0)
                else:
                    sta_list.append(1)
                    fee_nuki_list.append(fee_nuki_value)
                    fee_tax_num_list.append(int(fee_komi_value - fee_nuki_value))
                    fee_tax_per_list.append(10)

    return (
        sta_list,
        syoken_list,
        eda_list,
        fee_komi_list,
        fee_nuki_list,
        fee_tax_num_list,
        fee_tax_per_list,
        kaime_list,
        cat_list,
        name_list,
    )


def sub_exe(sheet_name, spreadsheet_file):
    # get sheet
    original_sheet = spreadsheet_file.worksheet(sheet_name)

    syoken = 11  # col K 証券番号
    kaime = 19  # col S 回目
    fee_komi = 22  # col V 収納等手数料

    # 2行目から取得
    y = 2 - 1

    sta_list = []
    syoken_list = []
    eda_list = []
    fee_komi_list = []
    fee_nuki_list = []
    fee_tax_num_list = []
    fee_tax_per_list = []
    kaime_list = []
    cat_list = []
    name_list = []

    syoken_data = original_sheet.col_values(syoken)[y:]
    fee_komi_data = original_sheet.col_values(fee_komi)[y:]
    kaime_data = original_sheet.col_values(kaime)[y:]

    # 証券番号などをセットする
    for i in range(len(syoken_data)):
        sta_list.append(2)
        syoken_value = str(syoken_data[i])

        # fee_komi_data の範囲チェックと値の取得
        if i < len(fee_komi_data) and fee_komi_data[i] is not None and str(fee_komi_data[i]).strip():
            fee_komi_value = int(str(fee_komi_data[i]))
            # fee_nuki_value は fee_komi_value が有効な場合のみ計算
            fee_nuki_value = int(float(fee_komi_value) / 1.1)  # 小数点以下切り捨て
        else:
            fee_komi_value = 0
            fee_nuki_value = 0

        fee_tax_num_value = int(fee_komi_value - fee_nuki_value)
        fee_tax_per_list.append(10)

        # kaime_data の範囲チェックと値の取得
        if i < len(kaime_data) and kaime_data[i] is not None:
            kaime_value = str(kaime_data[i])
        else:
            kaime_value = ""

        syoken_list.append(syoken_value)
        eda_list.append("0000")
        fee_komi_list.append(fee_komi_value)
        fee_nuki_list.append(fee_nuki_value)
        fee_tax_num_list.append(fee_tax_num_value)
        kaime_list.append(kaime_value)
        cat_list.append(sheet_name)
        name_list.append(sheet_name)

    return (
        sta_list,
        syoken_list,
        eda_list,
        fee_komi_list,
        fee_nuki_list,
        fee_tax_num_list,
        fee_tax_per_list,
        kaime_list,
        cat_list,
        name_list,
    )
