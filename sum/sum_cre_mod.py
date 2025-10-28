from _mod import sql_config, mod_datetime
from _mod_fis import mod_kei_nyu_pay
from sum import sum_cre_sql


# delete
def mz_del(kei_date_int):
    sum_cre_sql.mz_sql_sum_store_del(kei_date_int)
    return


# create
def mz_cre(kei_date_int):
    exe_cnt = 0

    # 計上年度
    kei_data = mod_kei_nyu_pay.mz_kei_nyu_pay_sel_data(kei_date_int)
    for dt in kei_data:
        keijyo_nendo = dt["kei_nendo"]

    # 計上年月
    keijyo_date = kei_date_int

    sql_data = sum_cre_sql.mz_sql_order_store(kei_date_int)
    for dt in sql_data:
        fis_cd = dt["fis_cd"]
        cat_cd = dt["cat_cd"]
        coltd_cd = dt["coltd_cd"]

        kind_cd_main = dt["kind_cd_main"]
        kind_cd_sub = dt["kind_cd_sub"]

        keiyaku_cd = dt["keiyaku_cd"]
        keiyaku_grp_cd = dt["keiyaku_grp_cd"]

        syoken_cd_main = dt["syoken_cd_main"]
        syoken_cd_sub = dt["syoken_cd_sub"]

        siki_date = dt["siki_date"]
        manki_date = dt["manki_date"]
        ido_kai_date = dt["ido_kai_date"]
        ido_kai_hoken_ryo = dt["ido_kai_hoken_ryo"]
        mikeika_month = 0
        pay_num_cd = dt["pay_num_cd"]

        # res保険期間year
        hoken_kikan_cd = dt["hoken_kikan_cd"]
        hoken_kikan_year = dt["hoken_kikan_year"]
        res_hoken_kikan_year = sum_cre_sql.mz_res_hoken_kikan_year(hoken_kikan_cd, hoken_kikan_year)

        # 計算用の係数を算出
        keisu_year, keisu_month = sum_cre_sql.mz_keisu(pay_num_cd)

        # fee_ritu, fee seiho
        fee_ritu = dt["fee_ritu"]
        fee_seiho_kikan = dt["fee_seiho_kikan"]
        fee_seiho_first = dt["fee_seiho_first"]
        fee_seiho_next = dt["fee_seiho_next"]

        # -----------------------------------------------------------------------------------------------------

        all_res_hoken_ryo = 0
        all_res_hoken_ryo_year = 0
        all_res_hoken_ryo_total = 0
        all_res_fee_money = 0
        all_res_fee_money_year = 0
        all_res_fee_money_total = 0

        # 保険料・手数料 grp別に分ける(新規更改=grp1, 異動=grp2, 解約=grp3, 除外=grp9999)

        # 新規更改
        if keiyaku_grp_cd == "1":
            # 未経過月数
            if manki_date == 0:  # 終身の場合、50年とする(600ヶ月)
                mikeika_month = 600

            if manki_date != 0:  # 通常
                mikeika_month = res_hoken_kikan_year * 12

            # res保険料・res保険料year・res手数料
            all_res_hoken_ryo = dt["hoken_ryo"]  # res保険料（最小単位の支払）
            (
                all_res_hoken_ryo_year,
                all_res_hoken_ryo_total,
            ) = sum_cre_sql.mz_res_hoken_ryo_grp1(pay_num_cd, all_res_hoken_ryo, res_hoken_kikan_year, keisu_year)
            (
                all_res_fee_money,
                all_res_fee_money_year,
                all_res_fee_money_total,
            ) = sum_cre_sql.mz_res_fee_grp1(
                cat_cd,
                all_res_hoken_ryo,
                all_res_hoken_ryo_year,
                all_res_hoken_ryo_total,
                fee_ritu,
                fee_seiho_kikan,
                fee_seiho_first,
                fee_seiho_next,
            )

        # 異動
        if keiyaku_grp_cd == "2":
            # 未経過月数
            if manki_date == 0:  # 終身の場合、50年とする
                manki_date_syusin = mod_datetime.mz_num2add_year_kasan(siki_date, ido_kai_date, 50)
                mikeika_month = mod_datetime.mz_num2keika_month(ido_kai_date, manki_date_syusin)

            if manki_date != 0:  # 通常
                mikeika_month = mod_datetime.mz_num2keika_month(ido_kai_date, manki_date)

            # 未経過月数 +1
            mikeika_month += 1

            # res保険料・res保険料year・res手数料
            if ido_kai_hoken_ryo == 0:
                all_res_hoken_ryo = 0  # res保険料（最小単位の支払）
                all_res_hoken_ryo_year = 0
                all_res_hoken_ryo_total = 0
                all_res_fee_money = 0
                all_res_fee_money_year = 0
                all_res_fee_money_total = 0
            else:
                all_res_hoken_ryo = dt["ido_kai_hoken_ryo"]  # res保険料（最小単位の支払）
                (
                    all_res_hoken_ryo_year,
                    all_res_hoken_ryo_total,
                ) = sum_cre_sql.mz_res_hoken_ryo_grp2(
                    pay_num_cd,
                    all_res_hoken_ryo,
                    res_hoken_kikan_year,
                    keisu_year,
                    keisu_month,
                    mikeika_month,
                )
                (
                    all_res_fee_money,
                    all_res_fee_money_year,
                    all_res_fee_money_total,
                ) = sum_cre_sql.mz_res_fee_grp2(
                    cat_cd,
                    pay_num_cd,
                    all_res_hoken_ryo,
                    all_res_hoken_ryo_year,
                    all_res_hoken_ryo_total,
                    fee_ritu,
                    res_hoken_kikan_year,
                )

        # 解約
        if keiyaku_grp_cd == "3":
            # 未経過月数
            if manki_date == 0:  # 終身の場合、50年とする
                manki_date_syusin = mod_datetime.mz_num2add_year_kasan(siki_date, 20300101, 50)
                mikeika_month = mod_datetime.mz_num2keika_month(ido_kai_date, manki_date_syusin)

            if manki_date != 0:  # 通常
                mikeika_month = mod_datetime.mz_num2keika_month(ido_kai_date, manki_date)

            # 未経過月数 +1
            mikeika_month += 1

            # 経過月数
            keika_month = mod_datetime.mz_num2keika_month(siki_date, ido_kai_date)

            # 生保
            if cat_cd == "1":
                # res保険料・res保険料year
                all_res_hoken_ryo = dt["hoken_ryo"] * (
                    -1
                )  # res保険料（生保の場合は、通常の保険料をマイナスにする、最小単位の支払）
                (
                    all_res_hoken_ryo_year,
                    all_res_hoken_ryo_total,
                ) = sum_cre_sql.mz_res_hoken_ryo_grp3_seiho(
                    pay_num_cd,
                    all_res_hoken_ryo,
                    res_hoken_kikan_year,
                    keisu_year,
                    keisu_month,
                    mikeika_month,
                )
                # res手数料
                (
                    all_res_fee_money,
                    all_res_fee_money_year,
                    all_res_fee_money_total,
                ) = sum_cre_sql.mz_res_fee_grp3_seiho(pay_num_cd, keisu_month, syoken_cd_main, keika_month)

            # 損保
            if cat_cd == "2":
                # res保険料・res保険料year
                all_res_hoken_ryo = dt["ido_kai_hoken_ryo"]  # res保険料（最小単位の支払）
                all_res_hoken_ryo_year = all_res_hoken_ryo
                all_res_hoken_ryo_total = all_res_hoken_ryo
                # res手数料
                (
                    all_res_fee_money,
                    all_res_fee_money_year,
                    all_res_fee_money_total,
                ) = sum_cre_sql.mz_res_fee_grp3_sonpo(all_res_hoken_ryo, fee_ritu)

        # その他
        hojin_kojin_cd = dt["hojin_kojin_cd"]
        cust_new_old_cd = dt["cust_new_old_cd"]
        kei_name = dt["kei_name"]
        kei_name_nospace = dt["kei_name_nospace"]
        section_cd = dt["section_cd"]
        create_email = "admin@fujitomi.jp"
        # gyotei_email = mod_staff.mz_staff_gyotei_email(section_cd)

        staff1_email = dt["staff1_email"]
        staff2_email = dt["staff2_email"]
        staff3_email = dt["staff3_email"]
        gyotei1_cd = dt["gyotei1_cd"]
        gyotei2_cd = dt["gyotei2_cd"]
        gyotei3_cd = dt["gyotei3_cd"]
        fee_staff1 = dt["fee_staff1"]
        fee_staff2 = dt["fee_staff2"]
        fee_staff3 = dt["fee_staff3"]
        fee_gyotei1 = dt["fee_gyotei1"]
        fee_gyotei2 = dt["fee_gyotei2"]
        fee_gyotei3 = dt["fee_gyotei3"]

        stf_list = [1, 2, 3, 4, 5, 6]
        insert_exe = "no"

        for stf in stf_list:
            if stf == 1 and fee_staff1 != 0.0:
                insert_exe = "yes"
                staff_kind = "main"
                staff_email = staff1_email
                staff_fee_per = float(fee_staff1)
                gyotei_cd = "99990001"
            if stf == 2 and fee_staff2 != 0.0:
                insert_exe = "yes"
                staff_kind = "sub"
                staff_email = staff2_email
                staff_fee_per = float(fee_staff2)
                gyotei_cd = "99990001"
            if stf == 3 and fee_staff3 != 0.0:
                insert_exe = "yes"
                staff_kind = "sub"
                staff_email = staff3_email
                staff_fee_per = float(fee_staff3)
                gyotei_cd = "99990001"
            if stf == 4 and fee_gyotei1 != 0.0:  # 提携の場合でも主担当をセット
                insert_exe = "yes"
                staff_kind = "gyotei1"
                staff_email = staff1_email
                staff_fee_per = float(fee_gyotei1)
                gyotei_cd = gyotei1_cd
            if stf == 5 and fee_gyotei2 != 0.0:  # 提携の場合でも主担当をセット
                insert_exe = "yes"
                staff_kind = "gyotei2"
                staff_email = staff1_email
                staff_fee_per = float(fee_gyotei2)
                gyotei_cd = gyotei2_cd
            if stf == 6 and fee_gyotei3 != 0.0:  # 提携の場合でも主担当をセット
                insert_exe = "yes"
                staff_kind = "gyotei3"
                staff_email = staff1_email
                staff_fee_per = float(fee_gyotei3)
                gyotei_cd = gyotei3_cd

            # insert sql
            if insert_exe == "yes":
                res_hoken_ryo = int(all_res_hoken_ryo * staff_fee_per * 0.01)
                res_hoken_ryo_year = int(all_res_hoken_ryo_year * staff_fee_per * 0.01)
                res_hoken_ryo_total = int(all_res_hoken_ryo_total * staff_fee_per * 0.01)

                res_fee_money = int(all_res_fee_money * staff_fee_per * 0.01)
                res_fee_money_year = int(all_res_fee_money_year * staff_fee_per * 0.01)
                res_fee_money_total = int(all_res_fee_money_total * staff_fee_per * 0.01)

                sql_con = sql_config.mz_sql_con()
                with sql_con:
                    sql = """
                    INSERT INTO sql_sum_store (
                        fis_cd,
                        keijyo_nendo,
                        keijyo_date,
                        cat_cd,
                        coltd_cd,
                        kind_cd_main,
                        kind_cd_sub,
                        keiyaku_cd,
                        syoken_cd_main,
                        syoken_cd_sub,
                        siki_date,
                        manki_date,
                        ido_kai_date,
                        mikeika_month,
                        pay_num_cd,
                        res_hoken_kikan_year,
                        res_hoken_ryo,
                        res_hoken_ryo_year,
                        res_hoken_ryo_total,
                        fee_ritu,
                        res_fee_money,
                        res_fee_money_year,
                        res_fee_money_total,
                        hojin_kojin_cd,
                        cust_new_old_cd,
                        kei_name,
                        kei_name_nospace,
                        section_cd,
                        staff_kind,
                        staff_email,
                        staff_fee_per,
                        gyotei_cd,
                        create_email
                    ) VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    );
                    """
                    cur = sql_con.cursor()
                    cur.execute(
                        sql,
                        (
                            fis_cd,
                            keijyo_nendo,
                            keijyo_date,
                            cat_cd,
                            coltd_cd,
                            kind_cd_main,
                            kind_cd_sub,
                            keiyaku_cd,
                            syoken_cd_main,
                            syoken_cd_sub,
                            siki_date,
                            manki_date,
                            ido_kai_date,
                            mikeika_month,
                            pay_num_cd,
                            res_hoken_kikan_year,
                            res_hoken_ryo,
                            res_hoken_ryo_year,
                            res_hoken_ryo_total,
                            fee_ritu,
                            res_fee_money,
                            res_fee_money_year,
                            res_fee_money_total,
                            hojin_kojin_cd,
                            cust_new_old_cd,
                            kei_name,
                            kei_name_nospace,
                            section_cd,
                            staff_kind,
                            staff_email,
                            staff_fee_per,
                            gyotei_cd,
                            create_email,
                        ),
                    )
                    sql_con.commit()
                    exe_cnt += 1
                    insert_exe = "no"
    return exe_cnt
