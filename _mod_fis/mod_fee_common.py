# ------------------------------------------------------------------------------------------------------------
# fee率からfee円を計算
# 1.生保で次年度以降(first_next_year=2)、提携のステータスが1（１年のみ）の場合、手数料が０になり、提携の配分は、担当、その他の提携に割り振られる
# 2.ボーナスの場合の提携を0円にして再計算する---現在実行していない
# ------------------------------------------------------------------------------------------------------------


def mz_fee_per_yen(fee_send_dic):
    cat_cd = fee_send_dic["cat_cd"]
    fee_num = float(fee_send_dic["fee_num"])

    fee_staff1 = float(fee_send_dic["fee_staff1"])
    fee_staff2 = float(fee_send_dic["fee_staff2"])
    fee_staff3 = float(fee_send_dic["fee_staff3"])

    fee_gyotei1 = float(fee_send_dic["fee_gyotei1"])
    fee_gyotei2 = float(fee_send_dic["fee_gyotei2"])
    fee_gyotei3 = float(fee_send_dic["fee_gyotei3"])

    # bonus_cd = fee_send_dic["bonus_cd"]
    first_next_year = fee_send_dic["first_next_year"]

    fee_staff1_yen = 0
    fee_staff2_yen = 0
    fee_staff3_yen = 0

    fee_gyotei1_yen = 0
    fee_gyotei2_yen = 0
    fee_gyotei3_yen = 0

    pay_kikan1 = int(fee_send_dic["pay_kikan1"])
    pay_kikan2 = int(fee_send_dic["pay_kikan2"])
    pay_kikan3 = int(fee_send_dic["pay_kikan3"])

    pay_gyotei_1year_over = 0

    # 生保で、次年度以降の場合(first_next_year=2)、配分を再計算
    if cat_cd == "1" and first_next_year == 2:
        if pay_kikan1 == 1:
            stf_fee = 100 - fee_gyotei1
            fee_staff2 = round((fee_staff2 / stf_fee) * 100, 1)
            fee_staff3 = round((fee_staff3 / stf_fee) * 100, 1)
            fee_gyotei1 = 0.0
            fee_gyotei2 = round((fee_gyotei2 / stf_fee) * 100, 1)
            fee_gyotei3 = round((fee_gyotei3 / stf_fee) * 100, 1)
            fee_staff1 = round(
                100 - (fee_staff2 + fee_staff3 + fee_gyotei1 + fee_gyotei2 + fee_gyotei3),
                1,
            )
            pay_gyotei_1year_over += 1

        if pay_kikan2 == 1:
            stf_fee = 100 - fee_gyotei2
            fee_staff2 = round((fee_staff2 / stf_fee) * 100, 1)
            fee_staff3 = round((fee_staff3 / stf_fee) * 100, 1)
            fee_gyotei1 = round((fee_gyotei1 / stf_fee) * 100, 1)
            fee_gyotei2 = 0.0
            fee_gyotei3 = round((fee_gyotei3 / stf_fee) * 100, 1)
            fee_staff1 = round(
                100 - (fee_staff2 + fee_staff3 + fee_gyotei1 + fee_gyotei2 + fee_gyotei3),
                1,
            )
            pay_gyotei_1year_over += 2

        if pay_kikan3 == 1:
            stf_fee = 100 - fee_gyotei3
            fee_staff2 = round((fee_staff2 / stf_fee) * 100, 1)
            fee_staff3 = round((fee_staff3 / stf_fee) * 100, 1)
            fee_gyotei1 = round((fee_gyotei1 / stf_fee) * 100, 1)
            fee_gyotei2 = round((fee_gyotei2 / stf_fee) * 100, 1)
            fee_gyotei3 = 0.0
            fee_staff1 = round(
                100 - (fee_staff2 + fee_staff3 + fee_gyotei1 + fee_gyotei2 + fee_gyotei3),
                1,
            )
            pay_gyotei_1year_over += 5

    # ボーナスの場合 gyotei1
    # if bonus_cd == 1 and fee_gyotei1 != 0:
    #     stf_fee = 100 - fee_gyotei1
    #     fee_staff2 = round((fee_staff2 / stf_fee) * 100, 1)
    #     fee_staff3 = round((fee_staff3 / stf_fee) * 100, 1)
    #     fee_gyotei1 = 0.0
    #     fee_gyotei2 = round((fee_gyotei2 / stf_fee) * 100, 1)
    #     fee_gyotei3 = round((fee_gyotei3 / stf_fee) * 100, 1)
    #     fee_staff1 = round(
    #         100 - (fee_staff2 + fee_staff3 + fee_gyotei1 + fee_gyotei2 + fee_gyotei3), 1
    #     )

    # ボーナスの場合 gyotei2
    # if bonus_cd == 1 and fee_gyotei2 != 0:
    #     stf_fee = 100 - fee_gyotei2
    #     fee_staff2 = round((fee_staff2 / stf_fee) * 100, 1)
    #     fee_staff3 = round((fee_staff3 / stf_fee) * 100, 1)
    #     fee_gyotei1 = round((fee_gyotei1 / stf_fee) * 100, 1)
    #     fee_gyotei2 = 0.0
    #     fee_gyotei3 = round((fee_gyotei3 / stf_fee) * 100, 1)
    #     fee_staff1 = round(
    #         100 - (fee_staff2 + fee_staff3 + fee_gyotei1 + fee_gyotei2 + fee_gyotei3), 1
    #     )

    # ボーナスの場合 gyotei3
    # if bonus_cd == 1 and fee_gyotei3 != 0:
    #     stf_fee = 100 - fee_gyotei3
    #     fee_staff2 = round((fee_staff2 / stf_fee) * 100, 1)
    #     fee_staff3 = round((fee_staff3 / stf_fee) * 100, 1)
    #     fee_gyotei1 = round((fee_gyotei1 / stf_fee) * 100, 1)
    #     fee_gyotei2 = round((fee_gyotei2 / stf_fee) * 100, 1)
    #     fee_gyotei3 = 0.0
    #     fee_staff1 = round(
    #         100 - (fee_staff2 + fee_staff3 + fee_gyotei1 + fee_gyotei2 + fee_gyotei3), 1
    #     )

    # 円 ------------------------------------------------------------------------------------
    fee_staff1_yen = int(round((fee_num * fee_staff1) / 100))
    fee_staff2_yen = int(round((fee_num * fee_staff2) / 100))
    fee_staff3_yen = int(round((fee_num * fee_staff3) / 100))
    fee_gyotei1_yen = int(round((fee_num * fee_gyotei1) / 100))
    fee_gyotei2_yen = int(round((fee_num * fee_gyotei2) / 100))
    fee_gyotei3_yen = int(round((fee_num * fee_gyotei3) / 100))

    fee_rtn_dic = {
        "fee_staff1": fee_staff1,
        "fee_staff2": fee_staff2,
        "fee_staff3": fee_staff3,
        "fee_gyotei1": fee_gyotei1,
        "fee_gyotei2": fee_gyotei2,
        "fee_gyotei3": fee_gyotei3,
        "fee_staff1_yen": fee_staff1_yen,
        "fee_staff2_yen": fee_staff2_yen,
        "fee_staff3_yen": fee_staff3_yen,
        "fee_gyotei1_yen": fee_gyotei1_yen,
        "fee_gyotei2_yen": fee_gyotei2_yen,
        "fee_gyotei3_yen": fee_gyotei3_yen,
        "pay_gyotei_1year_over": pay_gyotei_1year_over,
    }

    return fee_rtn_dic
