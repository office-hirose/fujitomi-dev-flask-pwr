# -------------------------------------------------------------------
#  16 AIG損保
# -------------------------------------------------------------------
from fee_import import set_basic as SET_BASIC


# データ
def set_sheet(sheet_dic):
    # cell color
    # cell_yellow, cell_pink = SET_BASIC.set_cell_color()

    # Set sheet config
    original_sheet, new_sheet, new_sheet_url = SET_BASIC.set_sheet_config(sheet_dic)

    # Set header
    SET_BASIC.set_header(new_sheet)

    # 保険会社別設定

    # dmy
    row_len = 10

    # Set body
    SET_BASIC.set_body(new_sheet, sheet_dic, row_len)

    # 手数料税抜とりあえず0
    cell_list = new_sheet.range(f"I2:I{row_len}")
    for i, cell in enumerate(cell_list):
        cell.value = 0
    new_sheet.update_cells(cell_list)  # update

    # Set format
    SET_BASIC.set_format(new_sheet, row_len)

    return new_sheet_url
