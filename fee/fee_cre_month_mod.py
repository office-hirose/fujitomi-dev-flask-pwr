from _mod import sql_config
from _mod_fis import mod_fee_common
from fee import fee_cre_month_sql


# delete
def mz_del(nyu_date_int):
    fee_cre_month_sql.mz_sql_fee_order_store_del(nyu_date_int)
    return


# create
def mz_cre(nyu_date_int):
    exe_cnt = 0
    sql_data = fee_cre_month_sql.mz_sql_fee_order_store(nyu_date_int)
    for dt in sql_data:
        # fee率、fee円を計算、ボーナスの場合の計算
        fee_send_dic = {
            "nyu_date_int": nyu_date_int,
            "cat_cd": dt["cat_cd"],
            "siki_date": dt["siki_date"],
            "fee_num": dt["fee_num"],
            "fee_staff1": dt["fee_staff1"],
            "fee_staff2": dt["fee_staff2"],
            "fee_staff3": dt["fee_staff3"],
            "fee_gyotei1": dt["fee_gyotei1"],
            "fee_gyotei2": dt["fee_gyotei2"],
            "fee_gyotei3": dt["fee_gyotei3"],
            "pay_kikan1": dt["pay_kikan1"],
            "pay_kikan2": dt["pay_kikan2"],
            "pay_kikan3": dt["pay_kikan3"],
            "first_next_year": dt["first_next_year"],
        }
        fee_rtn_dic = mod_fee_common.mz_fee_per_yen(fee_send_dic)

        nyu_nendo = int(dt["nyu_nendo"])
        nyu_date = int(dt["nyu_date"])
        kind_cd = int(dt["kind_cd"])
        cat_cd = dt["cat_cd"]
        coltd_cd = dt["coltd_cd"]
        siki_date = int(dt["siki_date"])
        manki_date = int(dt["manki_date"])
        kind_cd_main = dt["kind_cd_main"]
        kind_cd_sub = dt["kind_cd_sub"]
        pay_num_cd = dt["pay_num_cd"]
        hoken_kikan_cd = dt["hoken_kikan_cd"]
        hoken_kikan_year = dt["hoken_kikan_year"]
        syoken_cd_main = dt["syoken_cd_main"]
        syoken_cd_sub = dt["syoken_cd_sub"]
        hoken_ryo = int(dt["hoken_ryo"])
        fee_num = int(dt["fee_num"])
        section_cd = dt["section_cd"]

        staff1_cd = dt["staff1_cd"]
        staff2_cd = dt["staff2_cd"]
        staff3_cd = dt["staff3_cd"]
        gyotei1_cd = dt["gyotei1_cd"]
        gyotei2_cd = dt["gyotei2_cd"]
        gyotei3_cd = dt["gyotei3_cd"]
        staff1_email = dt["staff1_email"]
        staff2_email = dt["staff2_email"]
        staff3_email = dt["staff3_email"]
        fee_staff1 = dt["fee_staff1"]
        fee_staff2 = dt["fee_staff2"]
        fee_staff3 = dt["fee_staff3"]
        # fee_gyotei1 = dt['fee_gyotei1']
        # fee_gyotei2 = dt['fee_gyotei2']
        # fee_gyotei3 = dt['fee_gyotei3']
        kei_name = dt["kei_name"]
        pay_gyotei_1year_over = fee_rtn_dic["pay_gyotei_1year_over"]
        kaime = dt["kaime"]
        fee_memo = dt["fee_memo"]
        first_next_year = dt["first_next_year"]

        section_cd_email1 = dt["section_cd_email1"]
        section_cd_email2 = dt["section_cd_email2"]
        section_cd_email3 = dt["section_cd_email3"]

        stf_list = [1, 2, 3, 4, 5, 6]
        insert_exe = "no"

        for stf in stf_list:
            if stf == 1 and fee_staff1 != 0.0:
                insert_exe = "yes"
                pay_person_kind = "main"
                section_cd_email = section_cd_email1
                pay_person_cd = staff1_cd
                pay_person_email = staff1_email
                pay_fee_per = fee_rtn_dic["fee_staff1"]
                pay_fee_yen = fee_rtn_dic["fee_staff1_yen"]
                pay_gyotei_cd = 0
            if stf == 2 and fee_staff2 != 0.0:
                insert_exe = "yes"
                pay_person_kind = "sub"
                section_cd_email = section_cd_email2
                pay_person_cd = staff2_cd
                pay_person_email = staff2_email
                pay_fee_per = fee_rtn_dic["fee_staff2"]
                pay_fee_yen = fee_rtn_dic["fee_staff2_yen"]
                pay_gyotei_cd = 0
            if stf == 3 and fee_staff3 != 0.0:
                insert_exe = "yes"
                pay_person_kind = "sub"
                section_cd_email = section_cd_email3
                pay_person_cd = staff3_cd
                pay_person_email = staff3_email
                pay_fee_per = fee_rtn_dic["fee_staff3"]
                pay_fee_yen = fee_rtn_dic["fee_staff3_yen"]
                pay_gyotei_cd = 0
            if stf == 4 and gyotei1_cd != "99990001":
                insert_exe = "yes"
                pay_person_kind = "gyotei1"
                section_cd_email = section_cd_email1
                pay_person_cd = staff1_cd  # 提携の場合でも主担当をセット
                pay_person_email = staff1_email
                pay_fee_per = fee_rtn_dic["fee_gyotei1"]
                pay_fee_yen = fee_rtn_dic["fee_gyotei1_yen"]
                pay_gyotei_cd = gyotei1_cd
            if stf == 5 and gyotei2_cd != "99990001":
                insert_exe = "yes"
                pay_person_kind = "gyotei2"
                section_cd_email = section_cd_email1
                pay_person_cd = staff1_cd  # 提携の場合でも主担当をセット
                pay_person_email = staff1_email
                pay_fee_per = fee_rtn_dic["fee_gyotei2"]
                pay_fee_yen = fee_rtn_dic["fee_gyotei2_yen"]
                pay_gyotei_cd = gyotei2_cd
            if stf == 6 and gyotei3_cd != "99990001":
                insert_exe = "yes"
                pay_person_kind = "gyotei3"
                section_cd_email = section_cd_email1
                pay_person_cd = staff1_cd  # 提携の場合でも主担当をセット
                pay_person_email = staff1_email
                pay_fee_per = fee_rtn_dic["fee_gyotei3"]
                pay_fee_yen = fee_rtn_dic["fee_gyotei3_yen"]
                pay_gyotei_cd = gyotei3_cd

            # ------------------------------------------------------------------------------------------
            # insert sql
            if insert_exe == "yes":
                sql_con = sql_config.mz_sql_con()
                with sql_con:
                    sql = """
                    INSERT INTO sql_fee_order_store (
                        nyu_nendo,
                        nyu_date,
                        kind_cd,
                        cat_cd,
                        coltd_cd,
                        siki_date,
                        manki_date,
                        kind_cd_main,
                        kind_cd_sub,
                        pay_num_cd,
                        hoken_kikan_cd,
                        hoken_kikan_year,
                        syoken_cd_main,
                        syoken_cd_sub,
                        hoken_ryo,
                        fee_num,
                        section_cd,
                        section_cd_email,
                        pay_person_kind,
                        pay_person_cd,
                        pay_person_email,
                        pay_fee_per,
                        pay_fee_yen,
                        pay_gyotei_cd,
                        kei_name,
                        pay_gyotei_1year_over,
                        kaime,
                        fee_memo,
                        first_next_year
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
                        %s
                    );
                    """
                    cur = sql_con.cursor()
                    cur.execute(
                        sql,
                        (
                            nyu_nendo,
                            nyu_date,
                            kind_cd,
                            cat_cd,
                            coltd_cd,
                            siki_date,
                            manki_date,
                            kind_cd_main,
                            kind_cd_sub,
                            pay_num_cd,
                            hoken_kikan_cd,
                            hoken_kikan_year,
                            syoken_cd_main,
                            syoken_cd_sub,
                            hoken_ryo,
                            fee_num,
                            section_cd,
                            section_cd_email,
                            pay_person_kind,
                            pay_person_cd,
                            pay_person_email,
                            pay_fee_per,
                            pay_fee_yen,
                            pay_gyotei_cd,
                            kei_name,
                            pay_gyotei_1year_over,
                            kaime,
                            fee_memo,
                            first_next_year,
                        ),
                    )
                    sql_con.commit()
                    exe_cnt += 1
                    insert_exe = "no"
    return exe_cnt


# 回目を修正する
def mz_update_kaime(nyu_date_int):
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = (
            "UPDATE sql_fee_order_store AS fos1,"
            + "(SELECT * FROM sql_fee_order_store WHERE kind_cd = 1 AND nyu_date = %s) AS fos2"
            + " SET fos1.kaime = fos2.kaime"
            + " WHERE fos1.nyu_date = %s"
            + " AND fos1.kind_cd = 2"
            + " AND fos1.coltd_cd = fos2.coltd_cd"
            + " AND fos1.syoken_cd_main = fos2.syoken_cd_main"
            + ";"
        )
        cur = sql_con.cursor()
        cur.execute(sql, (nyu_date_int, nyu_date_int))
        sql_con.commit()
    return


# 回目を修正する。こちらは時間がかかるのでNG
# def mz_update_kaime(nyu_date_int):
#     # kind_cd 2のみ
#     sql = (
#         "SELECT"
#         + " min(nyu_date) AS nyu_date,"
#         + " min(coltd_cd) AS coltd_cd,"
#         + " min(syoken_cd_main) AS syoken_cd_main,"
#         + " min(kind_cd) AS kind_cd,"
#         + " min(kaime) AS kaime"
#         + " FROM sql_fee_store"
#         + " WHERE nyu_date = "
#         + str(nyu_date_int)
#         + " AND syoken_cd_main != 'balance'"
#         + " AND kind_cd = 2"
#         + " GROUP BY nyu_date, coltd_cd, syoken_cd_main, kind_cd;"
#     )
#     kind2data = sql_config.mz_sql(sql)

#     # kind_cd=1の回目を取り出す
#     for k2dt in kind2data:
#         sql = (
#             "SELECT * FROM sql_fee_order_store"
#             + " WHERE nyu_date = "
#             + str(nyu_date_int)
#             + " AND coltd_cd = "
#             + '"'
#             + k2dt["coltd_cd"]
#             + '"'
#             + " AND syoken_cd_main = "
#             + '"'
#             + k2dt["syoken_cd_main"]
#             + '"'
#             + " AND kind_cd = 1;"
#         )
#         kind1data = sql_config.mz_sql(sql)

#         if len(kind1data) != 0:

#             for k1dt in kind1data:
#                 kaime_main = k1dt["kaime"]

#             # sql_fee_order_storeの回目を更新する
#             sql_con = sql_config.mz_sql_con()
#             with sql_con:
#                 sql = (
#                     "UPDATE sql_fee_order_store"
#                     + " SET kaime = %s"
#                     + " WHERE nyu_date = "
#                     + str(nyu_date_int)
#                     + " AND coltd_cd = "
#                     + '"'
#                     + k2dt["coltd_cd"]
#                     + '"'
#                     + " AND syoken_cd_main = "
#                     + '"'
#                     + k2dt["syoken_cd_main"]
#                     + '"'
#                     + ";"
#                 )
#                 cur = sql_con.cursor()
#                 cur.execute(sql, (kaime_main,))
#                 sql_con.commit()

#     return
