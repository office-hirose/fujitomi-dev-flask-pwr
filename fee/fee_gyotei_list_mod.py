from _mod_fis import mod_coltd, mod_kind, mod_pay_num, mod_siki_manki, mod_staff
from fee import fee_gyotei_list_sql


# setting
def mz_setting(sheet):
    sheet.set_default_row(25)  # height
    sheet.set_column(0, 0, 5)
    sheet.set_column(1, 1, 15)
    sheet.set_column(2, 2, 25)
    sheet.set_column(3, 3, 15)
    sheet.set_column(4, 4, 20)
    sheet.set_column(5, 5, 15)
    sheet.set_column(6, 6, 15)
    sheet.set_column(7, 7, 37)
    sheet.set_column(8, 8, 14)
    sheet.set_column(9, 9, 14)
    sheet.set_column(10, 10, 14)
    sheet.set_column(11, 11, 12)
    sheet.set_column(12, 12, 10)
    sheet.set_column(13, 13, 12)
    return sheet


# header
def mz_header(sheet, row, cf_dic, header_dic):
    # header_dic
    gyotei_name = header_dic["gyotei_name"]
    pay_date_str = header_dic["pay_date_str"]
    section_name = header_dic["section_name"]
    kanri_cd = str(header_dic["kanri_cd"])

    sheet.set_row(row, 34)  # height
    sheet.merge_range(row, 5, row, 7, "業務提携料支払明細", cf_dic["cf_c24"])
    row += 2

    sheet.set_row(row, 30)  # height
    sheet.write(row, 13, "株式会社フジトミ", cf_dic["cf_r20"])
    row += 2

    sheet.set_row(row, 30)  # height
    sheet.write(row, 3, "支払先：" + gyotei_name + "　様", cf_dic["cf_c20"])
    # sheet.merge_range(
    #     row,
    #     8,
    #     row,
    #     13,
    #     pay_date_str + " 支払分" + "：" + section_name + "-" + kanri_cd,
    #     cf_dic["cf_r20"],
    # )
    sheet.write(
        row,
        13,
        pay_date_str + " 支払分" + "：" + section_name + "-" + kanri_cd,
        cf_dic["cf_r20"],
    )
    row += 1

    return sheet, row


# bank
def mz_bank(sheet, row, cf_dic, bank_dic):
    # bank_dic
    bank_account_all = bank_dic["bank_account_all"]
    bank_account_name = bank_dic["bank_account_name"]

    sheet.set_row(row, 30)  # height
    sheet.write(row, 2, "振込口座", cf_dic["cf_c12_bor"])
    sheet.merge_range(row, 3, row, 6, bank_account_all, cf_dic["cf_c12_bor"])
    row += 1

    sheet.set_row(row, 30)  # height
    sheet.write(row, 2, "口座名義", cf_dic["cf_c12_bor"])

    # 口座名義の文字数によってフォントサイズを変更する
    if len(bank_account_name) >= 34:
        # 文字数が34文字以上の場合
        sheet.merge_range(row, 3, row, 6, bank_account_name, cf_dic["cf_c8_bor"])
    elif len(bank_account_name) >= 28:
        # 文字数が28文字以上34文字未満の場合
        sheet.merge_range(row, 3, row, 6, bank_account_name, cf_dic["cf_c10_bor"])
    else:
        # 文字数が28文字未満の場合
        sheet.merge_range(row, 3, row, 6, bank_account_name, cf_dic["cf_c12_bor"])

    row += 1

    sheet.set_row(row, 30)  # height
    sheet.write(row, 2, "振込金額", cf_dic["cf_c12_bor"])
    sheet.write(row, 6, "円", cf_dic["cf_l12_bor_yen"])
    sheet.merge_range(row, 3, row, 5, "=K16", cf_dic["cf_r20_comma_bor"])

    row += 2

    sheet.set_row(row, 25)  # height
    sheet.write(
        row,
        2,
        "※明細表項目の支払額欄にマイナス金額がある場合は次の内容が考えられます。ご留意ください。",
        cf_dic["cf_l12"],
    )
    row += 1
    sheet.write(row, 2, "①前月までの手数料(支払額)支払済契約の振替手数料", cf_dic["cf_l12"])
    row += 1
    sheet.write(row, 2, "②契約内容変更による保険料減額の手数料(支払額)戻入", cf_dic["cf_l12"])
    row += 1
    sheet.write(row, 2, "③解約・解除による手数料(支払額)戻入", cf_dic["cf_l12"])

    return sheet, row


# total
def mz_total(sheet, row, cf_dic, total_dic):
    # total_dic
    gensen_cd = total_dic["gensen_cd"]
    kojo_fee = total_dic["kojo_fee"]

    sheet.set_row(row, 30)  # height
    sheet.write(row, 8, "", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 9, "手数料", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 10, "支払手数料額", cf_dic["cf_c12_bor_line_double"])
    row += 1

    sheet.set_row(row, 45)  # height
    sheet.write(row, 8, "件数", cf_dic["cf_c12_bor"])
    sheet.write_formula(row, 9, "=COUNT(J26:J9999)", cf_dic["cf_r14_comma_bor"])
    sheet.write_formula(row, 10, "=COUNT(K26:K9999)", cf_dic["cf_r14_comma_bor"])
    row += 1

    sheet.set_row(row, 45)  # height
    sheet.write(row, 8, "小計(税抜)", cf_dic["cf_c12_bor"])
    sheet.write_formula(row, 9, "=SUM(J26:J9999)", cf_dic["cf_r14_comma_bor"])
    sheet.write_formula(row, 10, "=SUM(K26:K9999)", cf_dic["cf_r14_comma_bor"])
    row += 1

    sheet.set_row(row, 45)  # height
    sheet.write(row, 8, "消費税", cf_dic["cf_c12_bor"])
    sheet.write_formula(row, 9, "=ROUNDDOWN(J11*0.1, 0)", cf_dic["cf_r14_comma_bor"])
    sheet.write_formula(row, 10, "=ROUNDDOWN(K11*0.1, 0)", cf_dic["cf_r14_comma_bor"])
    row += 1

    sheet.set_row(row, 45)  # height
    sheet.write(row, 8, "控除額", cf_dic["cf_c12_bor"])
    sheet.write_formula(row, 9, "0", cf_dic["cf_r14_comma_bor"])
    kojo_fee = str(int(kojo_fee) * (-1))
    sheet.write_formula(row, 10, kojo_fee, cf_dic["cf_r14_comma_bor"])
    row += 1

    sheet.set_row(row, 45)  # height
    sheet.write(row, 8, "小計(税込)", cf_dic["cf_c12_bor_line_bold"])
    sheet.write(row, 9, "=SUM(J11:J13)", cf_dic["cf_r14_comma_bor_line_bold"])
    sheet.write(row, 10, "=SUM(K11:K13)", cf_dic["cf_r14_comma_bor_line_bold"])
    row += 1

    sheet.set_row(row, 45)  # height
    sheet.write(row, 8, "源泉徴収額", cf_dic["cf_c12_bor"])
    sheet.write_formula(row, 9, "0", cf_dic["cf_r14_comma_bor"])

    # 源泉徴収額
    if gensen_cd == "on":

        # sheet.write_formula(
        #     row,
        #     10,
        #     "=IF(SUM(K20:K9999)>1000000,
        # (ROUNDDOWN(SUM(K20:K9999)*0.2042, 0)*(-1))+102100, ROUNDDOWN(SUM(K20:K9999)*0.1021, 0)*(-1))",
        #     cf_dic["cf_r14_comma_bor"],
        # )

        sheet.write_formula(
            row,
            10,
            "=IF(K14>1000000, (ROUNDDOWN(K14*0.2042, 0)*(-1))+102100, ROUNDDOWN(K14*0.1021, 0)*(-1))",
            cf_dic["cf_r14_comma_bor"],
        )
    else:
        sheet.write_formula(row, 10, "0", cf_dic["cf_r14_comma_bor"])

    row += 1

    sheet.set_row(row, 45)  # height
    sheet.write(row, 8, "合計(税込)", cf_dic["cf_c12_bor_line_bold"])
    sheet.write_formula(row, 9, "=J14+J15", cf_dic["cf_r14_comma_bor_line_bold"])
    sheet.write_formula(row, 10, "=K14+K15", cf_dic["cf_r14_comma_bor_line_bold"])
    row += 1

    return sheet, row


# sign
def mz_sign(sheet, row, cf_dic):
    # sheet.set_row(row, 25)  # height
    # sheet.write(row, 9, '担当印', cf_dic['cf_c12_bor'])
    # sheet.write(row, 10, '承認印', cf_dic['cf_c12_bor'])
    # sheet.write(row, 10, '検　印', cf_dic['cf_c12_bor'])
    row += 1

    # sheet.set_row(row, 25)  # height
    # sheet.merge_range(row, 9, row + 2, 9, '', cf_dic['cf_c12_bor'])
    # sheet.merge_range(row, 10, row + 2, 10, '', cf_dic['cf_c12_bor'])
    # sheet.merge_range(row, 10, row + 2, 10, '', cf_dic['cf_c12_bor'])
    row += 1

    return sheet, row


# header list
def mz_header_list(sheet, row, cf_dic, header_list_dic):
    # header_list_dic
    gyotei_name = header_list_dic["gyotei_name"]
    pay_date_str = header_list_dic["pay_date_str"]
    section_name = header_list_dic["section_name"]
    kanri_cd = header_list_dic["kanri_cd"]

    sheet.set_row(row, 25)  # height
    sheet.write(row, 1, "業務提携料支払明細", cf_dic["cf_l16"])
    sheet.write(row, 13, "株式会社フジトミ", cf_dic["cf_r16"])
    row += 2
    sheet.write(row, 1, "支払先：" + gyotei_name + "　様", cf_dic["cf_l16"])
    sheet.write(
        row,
        13,
        pay_date_str + " 支払分" + "：" + section_name + "-" + str(kanri_cd),
        cf_dic["cf_r16"],
    )
    row += 1

    return sheet, row


# title list
def mz_title_list(sheet, row, cf_dic):
    row += 1
    sheet.set_row(row, 27)  # height
    sheet.write(row, 0, "No", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 1, "証券番号", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 2, "保険会社", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 3, "保険種類", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 4, "払込方法", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 5, "保険始期", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 6, "保険満期", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 7, "契約者", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 8, "保険料", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 9, "税抜手数料", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 10, "支払額", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 11, "支払回", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 12, "担当者", cf_dic["cf_c12_bor_line_double"])
    sheet.write(row, 13, "メモ", cf_dic["cf_c12_bor_line_double"])
    return sheet, row


# sheet write
def mz_data_write(sheet, row, cf_dic, data_write_dic):
    # data_write_dic
    pagebreak_cnt = data_write_dic["pagebreak_cnt"]
    pagebreak_list = data_write_dic["pagebreak_list"]
    all_list = data_write_dic["all_list"]
    gyotei_name = data_write_dic["gyotei_name"]
    pay_date_str = data_write_dic["pay_date_str"]
    section_name = data_write_dic["section_name"]
    kanri_cd = data_write_dic["kanri_cd"]

    counter = 0
    for dt in all_list:
        sheet.set_row(row, 25)  # height
        sheet.write(row, 0, dt[0], cf_dic["cf_c12_bor"])
        sheet.write(row, 1, dt[1], cf_dic["cf_c12_bor"])
        sheet.write(row, 2, dt[2], cf_dic["cf_c10_bor"])
        sheet.write(row, 3, dt[3], cf_dic["cf_c10_bor"])
        sheet.write(row, 4, dt[4], cf_dic["cf_c10_bor"])
        sheet.write(row, 5, dt[5], cf_dic["cf_c12_bor"])
        sheet.write(row, 6, dt[6], cf_dic["cf_c12_bor"])

        # 契約者
        if len(dt[7]) >= 15:
            sheet.write(row, 7, dt[7], cf_dic["cf_l8_bor"])
        else:
            sheet.write(row, 7, dt[7], cf_dic["cf_l12_bor"])

        sheet.write(row, 8, dt[8], cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 9, dt[9], cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 10, dt[10], cf_dic["cf_r14_comma_bor"])
        sheet.write(row, 11, dt[11], cf_dic["cf_c12_bor"])
        sheet.write(row, 12, dt[12], cf_dic["cf_c12_bor"])
        sheet.write(row, 13, dt[13], cf_dic["cf_c10_bor"])

        row += 1
        counter += 1

        if counter == 25:
            header_list_dic = {
                "gyotei_name": gyotei_name,
                "pay_date_str": pay_date_str,
                "section_name": section_name,
                "kanri_cd": kanri_cd,
            }
            row += 2
            sheet, row = mz_header_list(sheet, row, cf_dic, header_list_dic)
            sheet, row = mz_title_list(sheet, row, cf_dic)
            pagebreak_cnt += 32
            pagebreak_list.append(pagebreak_cnt)
            row += 1
            counter = 0

    return sheet, row


# data create
def mz_data_create(nyu_date_int, gyotei_cd):
    # init
    all_list = []  # all list
    left_number = 0  # 左のナンバー
    fee_agt_yen_total = 0  # 代理店合計計算
    fee_gyotei_yen_total = 0  # 提携合計計算

    # fee data
    fee_data = fee_gyotei_list_sql.mz_sql_fee_order_store(nyu_date_int, gyotei_cd)
    for fdt in fee_data:
        # init, tuple
        dt_tuple = ()

        # create data
        left_number += 1
        syoken_cd_main = fdt["syoken_cd_main"]
        coltd_name = mod_coltd.mz_coltd_name_simple(fdt["coltd_cd"])

        if fdt["cat_cd"] == "1":
            kind_name = mod_kind.mz_kind_cd_sub2name(
                fdt["cat_cd"], fdt["coltd_cd"], fdt["kind_cd_main"], fdt["kind_cd_sub"]
            )
        if fdt["cat_cd"] != "1":
            kind_name = mod_kind.mz_kind_cd_main2name(fdt["kind_cd_main"])

        pay_num_name = mod_pay_num.mz_pay_num_name(fdt["pay_num_cd"])
        hoken_siki = mod_siki_manki.mz_siki_manki_date_str(fdt["siki_date"])

        hoken_manki_temp = mod_siki_manki.mz_siki_manki_date_str(fdt["manki_date"])
        if hoken_manki_temp == "0":
            hoken_manki = "終身"
        else:
            hoken_manki = hoken_manki_temp

        # keiyaku_name = (fdt['kei_name'])[0:21]  # 契約者名 slice 20文字
        keiyaku_name = fdt["kei_name"]  # 契約者名 slice なし
        hoken_ryo = fdt["hoken_ryo"]

        fee_num = fdt["fee_num"]  # 保険会社からの手数料
        fee_gyotei_yen = fdt["pay_fee_yen"]  # 提携支払手数料円

        kaime = fdt["kaime"]
        staff_name = mod_staff.mz_staff_name_simple(fdt["pay_person_cd"])

        if fdt["kind_cd"] == 1:
            fee_memo = fdt["fee_memo"]
        if fdt["kind_cd"] == 2:
            fee_memo = fdt["fee_memo"] + "(振替手数料)"

        # 合計計算
        fee_agt_yen_total = fee_agt_yen_total + fee_num
        fee_gyotei_yen_total = fee_gyotei_yen_total + fee_gyotei_yen

        # create, tuple, all_list
        dt_tuple = (
            left_number,
            syoken_cd_main,
            coltd_name,
            kind_name,
            pay_num_name,
            hoken_siki,
            hoken_manki,
            keiyaku_name,
            hoken_ryo,
            fee_num,
            fee_gyotei_yen,
            kaime,
            staff_name,
            fee_memo,
        )
        all_list.append(dt_tuple)

    return all_list, fee_agt_yen_total, fee_gyotei_yen_total
