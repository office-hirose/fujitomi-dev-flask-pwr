from _mod import sql_config


# delete record execute
def mz_sql_sum_store_del(kei_date_int):
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = "DELETE FROM sql_sum_store WHERE keijyo_date = %s;"
        cur = sql_con.cursor()
        cur.execute(sql, (kei_date_int,))
        sql_con.commit()
    return


# create
def mz_sql_order_store(kei_date_int):
    sql1 = """
        SELECT
        os.fis_cd,
        os.keiyaku_cd,
        kei.keiyaku_grp_cd,
        os.cat_cd,
        os.coltd_cd,
        os.kind_cd_main,
        os.kind_cd_sub,
        os.syoken_cd_main,
        os.syoken_cd_sub,
        os.siki_date,
        os.manki_date,
        os.ido_kai_date,
        os.ido_kai_hoken_ryo,
        os.hoken_kikan_cd,
        os.hoken_kikan_year,
        os.pay_num_cd,
        os.fee_ritu,
        os.fee_seiho_kikan,
        os.fee_seiho_first,
        os.fee_seiho_next,
        os.hoken_ryo,
        os.section_cd,
        os.staff1_cd,
        os.staff2_cd,
        os.staff3_cd,
        os.gyotei1_cd,
        os.gyotei2_cd,
        os.gyotei3_cd,
        os.fee_staff1,
        os.fee_staff2,
        os.fee_staff3,
        os.fee_gyotei1,
        os.fee_gyotei2,
        os.fee_gyotei3,
        os.cust_new_old_cd,
        os.hojin_kojin_cd,
        os.kei_name,
        os.kei_name_nospace,
        stf1.staff_email AS staff1_email,
        stf2.staff_email AS staff2_email,
        stf3.staff_email AS staff3_email

        FROM sql_order_store AS os
        LEFT JOIN sql_keiyaku AS kei ON os.keiyaku_cd = kei.keiyaku_cd
        LEFT JOIN sql_staff AS stf1 ON os.staff1_cd = stf1.staff_cd
        LEFT JOIN sql_staff AS stf2 ON os.staff2_cd = stf2.staff_cd
        LEFT JOIN sql_staff AS stf3 ON os.staff3_cd = stf3.staff_cd
    """
    sql2 = (
        " WHERE os.syoken_cd_sub = '0000' AND os.keijyo_date = "
        + str(kei_date_int)
        + " AND kei.keiyaku_grp_cd != '9999';"
    )
    sql = sql1 + sql2
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# keiyaku_cd to keiyaku_grp_cd, 現在使われていない
# def mz_keiyaku_cd2grp(keiyaku_cd):

#     # 1=未設定 ---> 除外する
#     # 2=新規
#     # 3=更改
#     # 4=満期落ち ---> 除外する
#     # 6=解約
#     # 7=異動
#     # 8=不成立 ---> 除外する
#     # 9999=入力ミス ---> 除外する

#     # 新規更改
#     if keiyaku_cd == '2' or keiyaku_cd == '3':
#         keiyaku_grp_cd = '1'

#     # 異動
#     if keiyaku_cd == '7':
#         keiyaku_grp_cd = '2'

#     # 解約
#     if keiyaku_cd == '6':
#         keiyaku_grp_cd = '3'

#     # 除外する、処理されない、mz_sql_order_storeでフィルターされているので基本実行されない、念の為
#     if keiyaku_cd == '1' or keiyaku_cd == '4' or keiyaku_cd == '8' or keiyaku_cd == '9999':
#         keiyaku_grp_cd = '9999'

#     return keiyaku_grp_cd


# res保険期間year
def mz_res_hoken_kikan_year(hoken_kikan_cd, hoken_kikan_year):
    res_hoken_kikan_year = hoken_kikan_year
    if hoken_kikan_cd != "9999":
        res_hoken_kikan_year = 0
        sql = "SELECT * FROM sql_hoken_kikan WHERE hoken_kikan_cd = " + '"' + str(hoken_kikan_cd) + '"' + ";"

        sql_con = sql_config.mz_sql_con()
        with sql_con.cursor() as cur:
            cur.execute(sql)
            sql_data = cur.fetchall()

        for dt in sql_data:
            res_hoken_kikan_year = dt["hoken_kikan_year"]

    return res_hoken_kikan_year


# 計算用の係数を算出
def mz_keisu(pay_num_cd):
    keisu_year = 0
    keisu_month = 0
    sql = "SELECT * FROM sql_pay_num WHERE pay_num_cd = " + '"' + str(pay_num_cd) + '"' + ";"

    sql_data = sql_config.mz_sql(sql)

    for dt in sql_data:
        keisu_year = dt["keisu_year"]
        keisu_month = dt["keisu_month"]
    return keisu_year, keisu_month


# ----------------------------------------------------------------------------------
# 保険料計算
# ----------------------------------------------------------------------------------


# res保険料year grp1 新規更改
def mz_res_hoken_ryo_grp1(pay_num_cd, res_hoken_ryo, res_hoken_kikan_year, keisu_year):
    # 一時払(全期前納含む)
    if pay_num_cd == "00":
        if res_hoken_kikan_year == 0:  # 未設定の場合
            res_hoken_ryo_year = 0
        else:
            res_hoken_ryo_year = round(res_hoken_ryo / res_hoken_kikan_year)

    # 一時払(全期前納含む)以外
    if pay_num_cd != "00":
        res_hoken_ryo_year = res_hoken_ryo * keisu_year

    res_hoken_ryo_total = res_hoken_ryo_year * res_hoken_kikan_year
    return res_hoken_ryo_year, res_hoken_ryo_total


# res保険料year grp2 異動
def mz_res_hoken_ryo_grp2(
    pay_num_cd,
    res_hoken_ryo,
    res_hoken_kikan_year,
    keisu_year,
    keisu_month,
    mikeika_month,
):
    # 一時払(全期前納含む)
    if pay_num_cd == "00":
        if res_hoken_kikan_year == 0:  # 未設定の場合
            res_hoken_ryo_year = 0
        else:
            if mikeika_month == 0:
                one_month = 0
            if mikeika_month != 0:
                one_month = round(res_hoken_ryo / mikeika_month)  # 1ヶ月分を算出
            if mikeika_month > 12:
                res_hoken_ryo_year = one_month * 12  # 1年分を算出
            if mikeika_month == 12:
                res_hoken_ryo_year = one_month * 12  # 1年分を算出
            if mikeika_month < 12:
                res_hoken_ryo_year = res_hoken_ryo  # 1年分を算出、未経過月数が1年以下の場合

    # 一時払(全期前納含む)以外
    if pay_num_cd != "00":
        one_month = round(res_hoken_ryo / keisu_month)  # 1ヶ月分を算出

        if mikeika_month > 12:
            res_hoken_ryo_year = one_month * keisu_year  # 1年分を算出
        if mikeika_month == 12:
            res_hoken_ryo_year = one_month * keisu_year  # 1年分を算出
        if mikeika_month < 12:
            res_hoken_ryo_year = one_month * mikeika_month  # 1年分を算出

    res_hoken_ryo_total = one_month * mikeika_month  # トータルを算出

    return res_hoken_ryo_year, res_hoken_ryo_total


# res保険料year grp3 解約 生保のみ
def mz_res_hoken_ryo_grp3_seiho(
    pay_num_cd,
    res_hoken_ryo,
    res_hoken_kikan_year,
    keisu_year,
    keisu_month,
    mikeika_month,
):
    # 一時払(全期前納含む)
    if pay_num_cd == "00":
        if res_hoken_kikan_year == 0:  # 未設定の場合
            res_hoken_ryo_year = 0
        else:
            if mikeika_month == 0:
                one_month = 0
            if mikeika_month != 0:
                one_month = round(res_hoken_ryo / mikeika_month)  # 1ヶ月分を算出
            if mikeika_month > 12:
                res_hoken_ryo_year = one_month * 12  # 1年分を算出
            if mikeika_month == 12:
                res_hoken_ryo_year = one_month * 12  # 1年分を算出
            if mikeika_month < 12:
                res_hoken_ryo_year = res_hoken_ryo  # 1年分を算出、未経過月数が1年以下の場合

    # 一時払(全期前納含む)以外
    if pay_num_cd != "00":
        one_month = round(res_hoken_ryo / keisu_month)  # 1ヶ月分を算出

        if mikeika_month > 12:
            res_hoken_ryo_year = one_month * keisu_year  # 1年分を算出
        if mikeika_month == 12:
            res_hoken_ryo_year = one_month * keisu_year  # 1年分を算出
        if mikeika_month < 12:
            res_hoken_ryo_year = one_month * mikeika_month  # 1年分を算出

    res_hoken_ryo_total = one_month * mikeika_month  # トータルを算出

    return res_hoken_ryo_year, res_hoken_ryo_total


# ----------------------------------------------------------------------------------
# 手数料計算
# ----------------------------------------------------------------------------------


# res手数料 grp1 新規更改
def mz_res_fee_grp1(
    cat_cd,
    res_hoken_ryo,
    res_hoken_ryo_year,
    res_hoken_ryo_total,
    fee_ritu,
    fee_seiho_kikan,
    fee_seiho_first,
    fee_seiho_next,
):
    if cat_cd == "1":
        res_fee_money = fee_seiho_first
        res_fee_money_year = fee_seiho_first
        res_fee_money_total = fee_seiho_first + ((fee_seiho_kikan - 1) * fee_seiho_next)

    if cat_cd == "2" or cat_cd == "3":
        res_fee_money = round(res_hoken_ryo * fee_ritu * 0.01)  # ここは月換算ではなく初回の手数料のイメージ
        res_fee_money_year = round(res_hoken_ryo_year * fee_ritu * 0.01)
        res_fee_money_total = round(res_hoken_ryo_total * fee_ritu * 0.01)

    return res_fee_money, res_fee_money_year, res_fee_money_total


# res手数料 grp2 異動
def mz_res_fee_grp2(
    cat_cd,
    pay_num_cd,
    res_hoken_ryo,
    res_hoken_ryo_year,
    res_hoken_ryo_total,
    fee_ritu,
    res_hoken_kikan_year,
):
    if cat_cd == "1":
        res_fee_money = 0
        res_fee_money_year = 0
        res_fee_money_total = 0

    if cat_cd == "2" or cat_cd == "3":
        if pay_num_cd == "00":
            if res_hoken_kikan_year == 0:  # 未設定の場合
                res_fee_money = 0
                res_fee_money_year = 0
            else:
                res_fee_money = round(res_hoken_ryo * fee_ritu * 0.01)  # ここは月換算ではなく初回の手数料のイメージ
                res_fee_money_year = round(res_hoken_ryo_year * fee_ritu * 0.01)  # 1年分を算出

        if pay_num_cd != "00":
            res_fee_money = round(res_hoken_ryo * fee_ritu * 0.01)  # ここは月換算ではなく初回の手数料のイメージ
            res_fee_money_year = round(res_hoken_ryo_year * fee_ritu * 0.01)  # 1年分を算出

        res_fee_money_total = round(res_hoken_ryo_total * fee_ritu * 0.01)  # トータル分を算出

    return res_fee_money, res_fee_money_year, res_fee_money_total


# res手数料 grp3 解約 生保
def mz_res_fee_grp3_seiho(pay_num_cd, keisu_month, syoken_cd_main, keika_month):
    # init
    fee_seiho_kikan = 0
    fee_seiho_first = 0
    fee_seiho_next = 0

    # init
    res_fee_money = 0
    res_fee_money_year = 0
    res_fee_money_total = 0

    # [新規]データを検索
    sql = (
        "SELECT * FROM sql_order_store WHERE syoken_cd_main = " + '"' + syoken_cd_main + '"' + " AND keiyaku_cd = '2';"
    )

    sql_data = sql_config.mz_sql(sql)

    for dt in sql_data:
        fee_seiho_kikan = dt["fee_seiho_kikan"]
        fee_seiho_first = dt["fee_seiho_first"]
        fee_seiho_next = dt["fee_seiho_next"]
        break

    # init 手数料最大期間
    kikan_full_month = fee_seiho_kikan * 12

    # init 初年度(月換算)、次年度以降(月換算)
    one_month_fee_first = round(fee_seiho_first / 12) * (-1)
    one_month_fee_next = round(fee_seiho_next / 12) * (-1)

    # 検索結果、レコードなし
    if len(sql_data) == 0:
        pass

    # 検索結果、レコードあり
    if len(sql_data) != 0:
        if fee_seiho_kikan == 0:
            pass

        if fee_seiho_kikan != 0:
            # 経過月数が初年度以内
            if keika_month <= keisu_month and keika_month <= 12:
                res_fee_money = one_month_fee_first * (keisu_month - keika_month)
                res_fee_money_year = res_fee_money
                res_fee_money_total = res_fee_money

            # 経過月数が次年度以降
            if keika_month > keisu_month and keika_month < kikan_full_month and keika_month > 12:
                keika_year_temp = (keika_month / keisu_month) + 1  # 切り上げ
                henkin_month = (keika_year_temp * keisu_month) - keika_month
                res_fee_money = one_month_fee_next * henkin_month
                res_fee_money_year = res_fee_money
                res_fee_money_total = res_fee_money

            if keika_month >= kikan_full_month:
                pass

    return res_fee_money, res_fee_money_year, res_fee_money_total


# res手数料 grp3 解約 損保
def mz_res_fee_grp3_sonpo(res_hoken_ryo, fee_ritu):
    res_fee_money = round(res_hoken_ryo * fee_ritu * 0.01)
    res_fee_money_year = res_fee_money
    res_fee_money_total = res_fee_money
    return res_fee_money, res_fee_money_year, res_fee_money_total
