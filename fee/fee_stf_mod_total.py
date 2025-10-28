from _mod_fis import mod_section, mod_staff
from fee import fee_stf_sql_total
from decimal import Decimal


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
    sheet.set_default_row(27)  # height
    sheet.set_column(0, 0, 27)
    sheet.set_column(1, 1, 15)
    sheet.set_column(2, 2, 15)
    sheet.set_column(3, 3, 15)
    sheet.set_column(4, 4, 15)
    sheet.set_column(5, 5, 15)

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
    total_all = 0

    # 嶋田さん以外 --------------------------------------------------------------------------------------

    if staff_email != "shimada.y@fujitomi.jp":
        stf_data = mod_staff.mz_staff_for_fee(staff_email)
        for dt in stf_data:
            staff_name_full = dt["name"]
            pay_rate = dt["pay_rate"]
            pay_rate_str = str(pay_rate) + "%"
            kojo_fee = dt["kojo_fee"] * (-1)
            break

        tan_fee_yen = fee_stf_sql_total.mz_sql_total(str(nyu_date_int), staff_email)
        tan_fee_no_tax, tan_fee_tax, tan_fee_total = mz_tan_fee_no_tax(tan_fee_yen, pay_rate)
        total_all += tan_fee_total

        # data write
        row += 1
        sheet.set_row(row, 45)  # height
        sheet.write(row, 0, staff_name_full, cf_dic["cf_c12_bor"])
        sheet.write(row, 1, tan_fee_yen, cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 2, pay_rate_str, cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 3, tan_fee_no_tax, cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 4, tan_fee_tax, cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 5, tan_fee_total, cf_dic["cf_r14_comma_bor"])

    # 嶋田さん専用 --------------------------------------------------------------------------------------

    if staff_email == "shimada.y@fujitomi.jp":
        section_list = ["1", "5", "3"]
        for section_cd in section_list:
            stf_data = mod_staff.mz_staff_for_fee(staff_email)
            for dt in stf_data:
                if dt["section_cd"] == section_cd:
                    staff_name_full = dt["name"] + "(" + mod_section.mz_section_name(section_cd) + ")"
                    pay_rate = dt["pay_rate"]
                    pay_rate_str = str(pay_rate) + "%"

                    tan_fee_yen = fee_stf_sql_total.mz_sql_total_section(str(nyu_date_int), staff_email, section_cd)
                    tan_fee_no_tax, tan_fee_tax, tan_fee_total = mz_tan_fee_no_tax(tan_fee_yen, pay_rate)
                    total_all += tan_fee_total

                    # 小計
                    row += 1
                    sheet.set_row(row, 45)  # height
                    sheet.write(row, 0, staff_name_full, cf_dic["cf_l10_bor"])
                    sheet.write(row, 1, tan_fee_yen, cf_dic["cf_r14_comma_bor"])
                    sheet.write(row, 2, pay_rate_str, cf_dic["cf_r14_comma_bor"])
                    sheet.write(row, 3, tan_fee_no_tax, cf_dic["cf_r14_comma_bor"])
                    sheet.write(row, 4, tan_fee_tax, cf_dic["cf_r14_comma_bor"])
                    sheet.write(row, 5, tan_fee_total, cf_dic["cf_r14_comma_bor"])

        # 熊本2は、main嶋田(65)とsub嶋田(100)で区別する必要がある
        stf_data = mod_staff.mz_staff_for_fee(staff_email)
        for dt in stf_data:
            if dt["section_cd"] == "4":
                # main嶋田
                staff_name_full = dt["name"] + "(熊本2担当1)"
                pay_rate = dt["pay_rate"]
                pay_rate_str = str(pay_rate) + "%"

                tan_fee_yen = fee_stf_sql_total.mz_sql_total_main_shimada(str(nyu_date_int), staff_email, "4")
                tan_fee_no_tax, tan_fee_tax, tan_fee_total = mz_tan_fee_no_tax(tan_fee_yen, pay_rate)
                total_all += tan_fee_total

                # 小計
                row += 1
                sheet.set_row(row, 45)  # height
                sheet.write(row, 0, staff_name_full, cf_dic["cf_l10_bor"])
                sheet.write(row, 1, tan_fee_yen, cf_dic["cf_r14_comma_bor"])
                sheet.write(row, 2, pay_rate_str, cf_dic["cf_r14_comma_bor"])
                sheet.write(row, 3, tan_fee_no_tax, cf_dic["cf_r14_comma_bor"])
                sheet.write(row, 4, tan_fee_tax, cf_dic["cf_r14_comma_bor"])
                sheet.write(row, 5, tan_fee_total, cf_dic["cf_r14_comma_bor"])

                # 副担当 嶋田のみ
                staff_name_full = dt["name"] + "(熊本2担当2)"
                pay_rate = 100
                pay_rate_str = str(pay_rate) + "%"
                kojo_fee = dt["kojo_fee"] * (-1)

                tan_fee_yen = fee_stf_sql_total.mz_sql_total_sub_shimada(str(nyu_date_int), staff_email, "4")
                tan_fee_no_tax, tan_fee_tax, tan_fee_total = mz_tan_fee_no_tax(tan_fee_yen, pay_rate)
                total_all += tan_fee_total

                # 小計
                row += 1
                sheet.set_row(row, 45)  # height
                sheet.write(row, 0, staff_name_full, cf_dic["cf_l10_bor"])
                sheet.write(row, 1, tan_fee_yen, cf_dic["cf_r14_comma_bor"])
                sheet.write(row, 2, pay_rate_str, cf_dic["cf_r14_comma_bor"])
                sheet.write(row, 3, tan_fee_no_tax, cf_dic["cf_r14_comma_bor"])
                sheet.write(row, 4, tan_fee_tax, cf_dic["cf_r14_comma_bor"])
                sheet.write(row, 5, tan_fee_total, cf_dic["cf_r14_comma_bor"])

    # 合計セクション
    row += 2
    sheet.set_row(row, 45)  # height
    sheet.write(row, 0, "", cf_dic["cf_c12"])
    sheet.write(row, 1, "", cf_dic["cf_c12"])
    sheet.write(row, 2, "", cf_dic["cf_c12"])
    sheet.write(row, 3, "", cf_dic["cf_c12"])
    sheet.write(row, 4, "控除前合計(税込)", cf_dic["cf_c10_bor"])
    sheet.write(row, 5, total_all, cf_dic["cf_r14_comma_bor"])

    row += 1
    sheet.set_row(row, 45)  # height
    sheet.write(row, 0, "", cf_dic["cf_c12"])
    sheet.write(row, 1, "", cf_dic["cf_c12"])
    sheet.write(row, 2, "", cf_dic["cf_c12"])
    sheet.write(row, 3, "", cf_dic["cf_c12"])
    sheet.write(row, 4, "控除額", cf_dic["cf_c10_bor"])
    sheet.write(row, 5, kojo_fee, cf_dic["cf_r14_comma_bor"])

    row += 1
    sheet.set_row(row, 45)  # height
    sheet.write(row, 0, "", cf_dic["cf_c12"])
    sheet.write(row, 1, "", cf_dic["cf_c12"])
    sheet.write(row, 2, "", cf_dic["cf_c12"])
    sheet.write(row, 3, "", cf_dic["cf_c12"])
    sheet.write(row, 4, "総合計(税込)", cf_dic["cf_c12_bor"])
    sheet.write(row, 5, total_all + kojo_fee, cf_dic["cf_r14_comma_bor"])

    # サイン
    row += 2
    sheet.set_row(row, 27)  # height
    sheet.write(row, 3, "担当印", cf_dic["cf_c10_bor"])
    sheet.write(row, 4, "担当印", cf_dic["cf_c10_bor"])
    sheet.write(row, 5, "承認印", cf_dic["cf_c10_bor"])
    row += 1
    sheet.set_row(row, 45)  # height
    sheet.write(row, 3, "", cf_dic["cf_c10_bor"])
    sheet.write(row, 4, "", cf_dic["cf_c10_bor"])
    sheet.write(row, 5, "", cf_dic["cf_c10_bor"])

    return sheet


# 税込 = 税抜 + 消費税
def mz_tan_fee_no_tax(tan_fee_yen, pay_rate):
    tan_fee_no_tax = round(Decimal(str(tan_fee_yen)) * (Decimal(str(pay_rate)) * Decimal("0.01")))
    tan_fee_tax = round(Decimal(str(tan_fee_no_tax)) * Decimal("0.1"))
    tan_fee_total = tan_fee_no_tax + tan_fee_tax
    return tan_fee_no_tax, tan_fee_tax, tan_fee_total
