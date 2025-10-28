from _mod_fis import mod_staff

# from decimal import Decimal


# total
def mz_total(
    sheet,
    cf_dic,
    row,
    pay_date_str,
    start_time,
    nyu_date_int,
    staff_email,
):
    sheet.set_paper(9)  # A4 size paper
    sheet.set_tab_color("blue")
    sheet.set_default_row(27)  # height
    sheet.set_column(0, 0, 30)
    sheet.set_column(1, 1, 16)
    sheet.set_column(2, 2, 16)
    sheet.set_column(3, 3, 16)
    sheet.set_column(4, 4, 16)
    sheet.set_column(5, 5, 16)

    sheet.write(row, 0, "支払(経理用)", cf_dic["cf_l14"])
    sheet.write(row, 5, "保険事業部　" + pay_date_str + "　支払分", cf_dic["cf_r14"])
    row += 1
    sheet.write(row, 5, "作成時刻:" + start_time, cf_dic["cf_r10"])

    row += 2
    sheet.write(row, 0, "支払先", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row, 1, "担当合計", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row, 2, "担当レート", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row, 3, "小計", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row, 4, "消費税", cf_dic["cf_c10_bor_line_double"])
    sheet.write(row, 5, "合計(税込)", cf_dic["cf_c10_bor_line_double"])

    # init
    # total_all = 0

    # 嶋田さん以外 --------------------------------------------------------------------------------------

    if staff_email != "shimada.y@fujitomi.jp":
        # init
        stf_data = mod_staff.mz_staff_for_fee(staff_email)
        for dt in stf_data:
            staff_name_full = dt["name"]
            pay_rate = dt["pay_rate"]
            pay_rate_str = str(pay_rate) + "%"
            kojo_fee = dt["kojo_fee"] * (-1)
            break

        # data write
        row += 1
        sheet.set_row(row, 45)
        sheet.write(row, 0, staff_name_full, cf_dic["cf_c12_bor"])
        sheet.write(row, 1, "=保険会社別!G8", cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 2, pay_rate_str, cf_dic["cf_r14_bor"])
        sheet.write(row, 3, "=ROUNDDOWN(B5*C5, 0)", cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 4, "=ROUNDDOWN(D5*0.1, 0)", cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 5, "=D5+E5", cf_dic["cf_r14_comma_bor"])

        # 合計セクション
        row += 2
        sheet.set_row(row, 45)
        sheet.write(row, 0, "", cf_dic["cf_c12"])
        sheet.write(row, 1, "", cf_dic["cf_c12"])
        sheet.write(row, 2, "", cf_dic["cf_c12"])
        sheet.write(row, 3, "", cf_dic["cf_c12"])
        sheet.write(row, 4, "控除前合計(税込)", cf_dic["cf_c10_bor"])
        sheet.write(row, 5, "=F5", cf_dic["cf_r14_comma_bor"])

        row += 1
        sheet.set_row(row, 45)
        sheet.write(row, 0, "", cf_dic["cf_c12"])
        sheet.write(row, 1, "", cf_dic["cf_c12"])
        sheet.write(row, 2, "", cf_dic["cf_c12"])
        sheet.write(row, 3, "", cf_dic["cf_c12"])
        sheet.write(row, 4, "控除額", cf_dic["cf_c10_bor"])
        sheet.write(row, 5, kojo_fee, cf_dic["cf_r14_comma_bor"])

        row += 1
        sheet.set_row(row, 45)
        sheet.write(row, 0, "", cf_dic["cf_c12"])
        sheet.write(row, 1, "", cf_dic["cf_c12"])
        sheet.write(row, 2, "", cf_dic["cf_c12"])
        sheet.write(row, 3, "", cf_dic["cf_c12"])
        sheet.write(row, 4, "総合計(税込)", cf_dic["cf_c12_bor"])
        sheet.write(row, 5, "=F7+F8", cf_dic["cf_r14_comma_bor"])

        # サイン
        row += 2
        sheet.set_row(row, 27)
        sheet.write(row, 3, "担当印", cf_dic["cf_c10_bor"])
        sheet.write(row, 4, "担当印", cf_dic["cf_c10_bor"])
        sheet.write(row, 5, "承認印", cf_dic["cf_c10_bor"])
        row += 1
        sheet.set_row(row, 45)
        sheet.write(row, 3, "", cf_dic["cf_c10_bor"])
        sheet.write(row, 4, "", cf_dic["cf_c10_bor"])
        sheet.write(row, 5, "", cf_dic["cf_c10_bor"])

    # 嶋田さん専用 --------------------------------------------------------------------------------------

    if staff_email == "shimada.y@fujitomi.jp":
        # init
        stf_data = mod_staff.mz_staff_for_fee(staff_email)
        for dt in stf_data:
            staff_name_full = dt["name"]
            pay_rate = dt["pay_rate"]
            pay_rate_str = str(pay_rate) + "%"
            kojo_fee = dt["kojo_fee"] * (-1)
            break

        # 東京
        row += 1
        sheet.set_row(row, 45)
        sheet.write(row, 0, "嶋田 義治(東京・担当2)", cf_dic["cf_c12_bor"])
        sheet.write(
            row,
            1,
            "=SUMIF(INDIRECT("
            + '"'
            + "リスト副担当!W:W"
            + '"'
            + ")"
            + ", 1, INDIRECT("
            + '"'
            + "リスト副担当!S:S"
            + '"'
            + "))",
            cf_dic["cf_r14_comma_bor"],
        )
        sheet.write(row, 2, pay_rate_str, cf_dic["cf_r14_bor"])
        sheet.write(row, 3, "=ROUNDDOWN(B5*C5, 0)", cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 4, "=ROUNDDOWN(D5*0.1, 0)", cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 5, "=D5+E5", cf_dic["cf_r14_comma_bor"])

        # 九州統括
        # row += 1
        # sheet.set_row(row, 45)
        # sheet.write(row, 0, "嶋田 義治(九州統括・担当2)", cf_dic["cf_c12_bor"])
        # sheet.write(
        #     row,
        #     1,
        #     "=SUMIF(INDIRECT("
        #     + '"'
        #     + "リスト副担当!W:W"
        #     + '"'
        #     + ")"
        #     + ", 5, INDIRECT("
        #     + '"'
        #     + "リスト副担当!S:S"
        #     + '"'
        #     + "))",
        #     cf_dic["cf_r14_comma_bor"],
        # )
        # sheet.write(row, 2, pay_rate_str, cf_dic["cf_r14_bor"])
        # sheet.write(row, 3, "=ROUNDDOWN(B6*C6, 0)", cf_dic["cf_r14_comma_bor"])
        # sheet.write(row, 4, "=ROUNDDOWN(D6*0.1, 0)", cf_dic["cf_r14_comma_bor"])
        # sheet.write(row, 5, "=D6+E6", cf_dic["cf_r14_comma_bor"])

        # 熊本1
        # row += 1
        # sheet.set_row(row, 45)
        # sheet.write(row, 0, "嶋田 義治(熊本1・担当2)", cf_dic["cf_c12_bor"])
        # sheet.write(
        #     row,
        #     1,
        #     "=SUMIF(INDIRECT("
        #     + '"'
        #     + "リスト副担当!W:W"
        #     + '"'
        #     + ")"
        #     + ", 3, INDIRECT("
        #     + '"'
        #     + "リスト副担当!S:S"
        #     + '"'
        #     + "))",
        #     cf_dic["cf_r14_comma_bor"],
        # )
        # sheet.write(row, 2, pay_rate_str, cf_dic["cf_r14_bor"])
        # sheet.write(row, 3, "=ROUNDDOWN(B7*C7, 0)", cf_dic["cf_r14_comma_bor"])
        # sheet.write(row, 4, "=ROUNDDOWN(D7*0.1, 0)", cf_dic["cf_r14_comma_bor"])
        # sheet.write(row, 5, "=D7+E7", cf_dic["cf_r14_comma_bor"])

        # 熊本2担当1
        row += 1
        sheet.set_row(row, 45)
        sheet.write(row, 0, "嶋田 義治(熊本2・担当1)", cf_dic["cf_c12_bor"])
        sheet.write(
            row,
            1,
            "=SUM(INDIRECT(" + '"' + "リスト主担当!S:S" + '"' + ")" + ")",
            cf_dic["cf_r14_comma_bor"],
        )
        sheet.write(row, 2, pay_rate_str, cf_dic["cf_r14_bor"])
        # sheet.write(row, 3, "=ROUNDDOWN(B8*C8, 0)", cf_dic["cf_r14_comma_bor"])
        # sheet.write(row, 4, "=ROUNDDOWN(D8*0.1, 0)", cf_dic["cf_r14_comma_bor"])
        # sheet.write(row, 5, "=D8+E8", cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 3, "=ROUNDDOWN(B6*C6, 0)", cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 4, "=ROUNDDOWN(D6*0.1, 0)", cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 5, "=D6+E6", cf_dic["cf_r14_comma_bor"])

        # 熊本2担当2
        row += 1
        sheet.set_row(row, 45)
        sheet.write(row, 0, "嶋田 義治(熊本2・担当2)", cf_dic["cf_c12_bor"])
        sheet.write(
            row,
            1,
            "=SUMIF(INDIRECT("
            + '"'
            + "リスト副担当!W:W"
            + '"'
            + ")"
            + ", 4, INDIRECT("
            + '"'
            + "リスト副担当!S:S"
            + '"'
            + "))",
            cf_dic["cf_r14_comma_bor"],
        )
        sheet.write(row, 2, pay_rate_str, cf_dic["cf_r14_bor"])
        # sheet.write(row, 3, "=ROUNDDOWN(B9*C9, 0)", cf_dic["cf_r14_comma_bor"])
        # sheet.write(row, 4, "=ROUNDDOWN(D9*0.1, 0)", cf_dic["cf_r14_comma_bor"])
        # sheet.write(row, 5, "=D9+E9", cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 3, "=ROUNDDOWN(B7*C7, 0)", cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 4, "=ROUNDDOWN(D7*0.1, 0)", cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 5, "=D7+E7", cf_dic["cf_r14_comma_bor"])

        # 合計セクション
        row += 2
        sheet.set_row(row, 45)
        sheet.write(row, 0, "", cf_dic["cf_c12"])
        sheet.write(row, 1, "", cf_dic["cf_c12"])
        sheet.write(row, 2, "", cf_dic["cf_c12"])
        sheet.write(row, 3, "", cf_dic["cf_c12"])
        sheet.write(row, 4, "控除前合計(税込)", cf_dic["cf_c10_bor"])
        # sheet.write(row, 5, "=SUM(F5:F9)", cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 5, "=SUM(F5:F7)", cf_dic["cf_r14_comma_bor"])

        row += 1
        sheet.set_row(row, 45)
        sheet.write(row, 0, "", cf_dic["cf_c12"])
        sheet.write(row, 1, "", cf_dic["cf_c12"])
        sheet.write(row, 2, "", cf_dic["cf_c12"])
        sheet.write(row, 3, "", cf_dic["cf_c12"])
        sheet.write(row, 4, "控除額", cf_dic["cf_c10_bor"])
        sheet.write(row, 5, kojo_fee, cf_dic["cf_r14_comma_bor"])

        row += 1
        sheet.set_row(row, 45)
        sheet.write(row, 0, "", cf_dic["cf_c12"])
        sheet.write(row, 1, "", cf_dic["cf_c12"])
        sheet.write(row, 2, "", cf_dic["cf_c12"])
        sheet.write(row, 3, "", cf_dic["cf_c12"])
        sheet.write(row, 4, "総合計(税込)", cf_dic["cf_c12_bor"])
        # sheet.write(row, 5, "=F11+F12", cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 5, "=F9+F10", cf_dic["cf_r14_comma_bor"])

        # サイン
        row += 2
        sheet.set_row(row, 27)
        sheet.write(row, 3, "担当印", cf_dic["cf_c10_bor"])
        sheet.write(row, 4, "担当印", cf_dic["cf_c10_bor"])
        sheet.write(row, 5, "承認印", cf_dic["cf_c10_bor"])
        row += 1
        sheet.set_row(row, 45)
        sheet.write(row, 3, "", cf_dic["cf_c10_bor"])
        sheet.write(row, 4, "", cf_dic["cf_c10_bor"])
        sheet.write(row, 5, "", cf_dic["cf_c10_bor"])

    return sheet


# 税込 = 税抜 + 消費税
# def mz_tan_fee_no_tax(tan_fee_yen, pay_rate):
#     tan_fee_no_tax = round(
#         Decimal(str(tan_fee_yen)) * (Decimal(str(pay_rate)) * Decimal("0.01"))
#     )
#     tan_fee_tax = round(Decimal(str(tan_fee_no_tax)) * Decimal("0.1"))
#     tan_fee_total = tan_fee_no_tax + tan_fee_tax
#     return tan_fee_no_tax, tan_fee_tax, tan_fee_total
