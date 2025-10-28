import sys
import json
import datetime
from _mod import sql_config, mod_datetime
from _mod_fis import mod_fis_cd, mod_common, mod_order_store_log, mod_memo_json


def mz_fee_chk_imp(nyu_date_int):
    # init
    sql_data = []
    update_cnt = 0

    # select
    sql1 = """
        SELECT
        min(cat_cd) AS cat_cd,
        min(coltd_cd) AS coltd_cd,
        min(syoken_cd_main) AS syoken_cd_main,
        min(syoken_cd_sub) AS syoken_cd_sub
        FROM
        (
        SELECT
        fee.cat_cd AS cat_cd,
        fee.coltd_cd AS coltd_cd,
        fee.syoken_cd_main AS syoken_cd_main,
        fee.syoken_cd_sub AS syoken_cd_sub
        FROM
    """

    sql2 = " ( SELECT * FROM sql_fee_store WHERE nyu_date = " + str(nyu_date_int) + ") AS fee "

    sql3 = """
        LEFT JOIN (
        SELECT
        min(cat_cd) AS cat_cd,
        min(coltd_cd) AS coltd_cd,
        min(syoken_cd_main) AS syoken_cd_main,
        min(syoken_cd_sub) AS syoken_cd_sub
        FROM
        sql_order_store
        GROUP BY
        sql_order_store.cat_cd,
        sql_order_store.coltd_cd,
        sql_order_store.syoken_cd_main,
        sql_order_store.syoken_cd_sub
        ) AS os ON
        fee.cat_cd = os.cat_cd
        AND fee.coltd_cd = os.coltd_cd
        AND fee.syoken_cd_main = os.syoken_cd_main
        AND fee.syoken_cd_sub = os.syoken_cd_sub
        WHERE
        os.cat_cd IS NULL
        ) AS res
        GROUP BY
        res.cat_cd,
        res.coltd_cd,
        res.syoken_cd_main,
        res.syoken_cd_sub
        ORDER BY
        cat_cd,
        coltd_cd,
        syoken_cd_main,
        syoken_cd_sub
        ;
    """

    sql = sql1 + sql2 + sql3
    sql_data = sql_config.mz_sql(sql)

    # insert
    for dt in sql_data:
        # fis番号生成
        fis_cd = mod_fis_cd.mz_fis_cd("admin@fujitomi.jp")

        # today create date
        today_num = mod_datetime.mz_now_date_num()
        create_date = today_num

        # keijyo_date = 202501  # 社内計上月
        keijyo_date = nyu_date_int  # 社内計上月

        keiyaku_cd = "2"  # 新規
        syoken_cd_main = dt["syoken_cd_main"]
        syoken_cd_sub = dt["syoken_cd_sub"]
        old_syoken_cd_main = ""
        old_syoken_cd_sub = ""
        mosikomi_cd = ""
        hoken_ryo = 0
        hoken_ryo_year = 0
        pay_num_cd = "00"  # 一時払(全期前納含む)
        hoken_kikan_cd = "99"
        hoken_kikan_year = 0
        section_cd = "7777"  # 不明
        staff1_cd = "empty@fumei"
        staff2_cd = "empty@fumei"
        staff3_cd = "empty@fumei"
        gyotei1_cd = "99990001"
        gyotei2_cd = "99990001"
        gyotei3_cd = "99990001"
        fee_staff1 = 100
        fee_staff2 = 0
        fee_staff3 = 0
        fee_gyotei1 = 0
        fee_gyotei2 = 0
        fee_gyotei3 = 0
        fee_memo = ""
        cat_cd = dt["cat_cd"]
        coltd_cd = dt["coltd_cd"]

        if cat_cd == "1":
            kind_cd_main = "AA"
            kind_cd_sub = "01"

            fee_seiho_kikan = 0
            fee_seiho_first = 0
            fee_seiho_next = 0

            fee_cd = "101"
            fee_cd_all = "1-9999-01-101"
            fee_cat = "1"
            fee_ritu = 0

        if cat_cd == "2":
            kind_cd_main = "01"
            kind_cd_sub = "01"

            fee_seiho_kikan = 0
            fee_seiho_first = 0
            fee_seiho_next = 0

            fee_cd = "101"
            fee_cd_all = "2-9999-01-101"
            fee_cat = "1"
            fee_ritu = 21

        if cat_cd == "3":  # 正しくないがとりあえず損保と同じにした、後に修正必要
            kind_cd_main = "01"
            kind_cd_sub = "01"

            fee_seiho_kikan = 0
            fee_seiho_first = 0
            fee_seiho_next = 0

            fee_cd = "101"
            fee_cd_all = "2-9999-01-101"
            fee_cat = "1"
            fee_ritu = 21

        exe_sta = "hand"

        ngw_keijyo_date = 0
        siki_date = 20010101
        manki_date = 0
        # siki_date = dt['siki_date']
        # manki_date = dt['manki_date']
        ido_kai_hoken_ryo = 0
        ido_kai_date = 0
        hojin_kojin_cd = "0"
        kei_name = "不明"
        kei_name_hira = ""
        kei_post = ""
        kei_address = ""
        kei_tel = ""
        cust_new_old_cd = "0"

        memo = "手数料リンクのためシステムが作成"
        temp = []
        memo_json = json.dumps(temp)
        memo, memo_json = mod_memo_json.mz_memo_json("admin@fujitomi.jp", memo, memo_json)

        search_text = mod_common.mz_search_text_conv(syoken_cd_main, old_syoken_cd_main, kei_name, kei_name_hira)
        kei_name_nospace = mod_common.mz_kei_name_nospace_conv(kei_name)
        valid_cd = "valid"
        create_email = "admin@fujitomi.jp"
        update_email = "admin@fujitomi.jp"
        regi_email = "admin@fujitomi.jp"
        regi_time = datetime.datetime.now() + datetime.timedelta(hours=9)

        # sql insert
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = """
            INSERT INTO sql_order_store (
                create_date,
                fis_cd,
                keijyo_date,
                keiyaku_cd,
                syoken_cd_main,
                syoken_cd_sub,
                old_syoken_cd_main,
                old_syoken_cd_sub,
                mosikomi_cd,
                hoken_ryo,
                hoken_ryo_year,
                pay_num_cd,
                hoken_kikan_cd,
                hoken_kikan_year,
                section_cd,
                staff1_cd,
                staff2_cd,
                staff3_cd,
                gyotei1_cd,
                gyotei2_cd,
                gyotei3_cd,
                fee_staff1,
                fee_staff2,
                fee_staff3,
                fee_gyotei1,
                fee_gyotei2,
                fee_gyotei3,
                fee_memo,
                cat_cd,
                coltd_cd,
                kind_cd_main,
                kind_cd_sub,
                fee_seiho_kikan,
                fee_seiho_first,
                fee_seiho_next,
                fee_cd,
                fee_cd_all,
                fee_cat,
                fee_ritu,
                exe_sta,
                ngw_keijyo_date,
                siki_date,
                manki_date,
                ido_kai_hoken_ryo,
                ido_kai_date,
                hojin_kojin_cd,
                kei_name,
                kei_name_hira,
                kei_post,
                kei_address,
                kei_tel,
                cust_new_old_cd,
                memo,
                memo_json,
                search_text,
                kei_name_nospace,
                valid_cd,
                create_email,
                update_email,
                regi_email,
                regi_time
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
                    create_date,
                    fis_cd,
                    keijyo_date,
                    keiyaku_cd,
                    syoken_cd_main,
                    syoken_cd_sub,
                    old_syoken_cd_main,
                    old_syoken_cd_sub,
                    mosikomi_cd,
                    hoken_ryo,
                    hoken_ryo_year,
                    pay_num_cd,
                    hoken_kikan_cd,
                    hoken_kikan_year,
                    section_cd,
                    staff1_cd,
                    staff2_cd,
                    staff3_cd,
                    gyotei1_cd,
                    gyotei2_cd,
                    gyotei3_cd,
                    fee_staff1,
                    fee_staff2,
                    fee_staff3,
                    fee_gyotei1,
                    fee_gyotei2,
                    fee_gyotei3,
                    fee_memo,
                    cat_cd,
                    coltd_cd,
                    kind_cd_main,
                    kind_cd_sub,
                    fee_seiho_kikan,
                    fee_seiho_first,
                    fee_seiho_next,
                    fee_cd,
                    fee_cd_all,
                    fee_cat,
                    fee_ritu,
                    exe_sta,
                    ngw_keijyo_date,
                    siki_date,
                    manki_date,
                    ido_kai_hoken_ryo,
                    ido_kai_date,
                    hojin_kojin_cd,
                    kei_name,
                    kei_name_hira,
                    kei_post,
                    kei_address,
                    kei_tel,
                    cust_new_old_cd,
                    memo,
                    memo_json,
                    search_text,
                    kei_name_nospace,
                    valid_cd,
                    create_email,
                    update_email,
                    regi_email,
                    regi_time,
                ),
            )
            sql_con.commit()
            update_cnt += 1

        # order_store_log
        mod_order_store_log.mz_insert_log(sys._getframe().f_code.co_name, fis_cd)

    return update_cnt
