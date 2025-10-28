# ------------------------------------------------------------------------
#  nttgw_store.py
#  |--nttgw_store      - 画面作成
#  |--nttgw_store_cnt  - カウント表示
#  |--nttgw_store_exe  - 実行する
#  |--nttgw_store_task - task que
# ------------------------------------------------------------------------
import sys
import json
import datetime
from flask import request
from _mod import fs_config, mod_base, mod_que, mod_datetime, sql_config
from _mod_fis import (
    mod_bosyu,
    mod_fee,
    mod_fis_cd,
    mod_common,
    mod_valid_cd,
    mod_order_store_log,
    mod_memo_json,
)
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, To


def nttgw_store():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    dic = {
        "level_error": level_error,
    }
    return dic


def nttgw_store_cnt():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "import_cnt": 0,
            "update_cnt": 0,
            "store_cnt": 0,
            "not_store_cnt": 0,
            "all_cnt": 0,
        }
    else:
        # init
        sql_data = []
        import_cnt = 0
        update_cnt = 0
        store_cnt = 0
        not_store_cnt = 0
        all_cnt = 0

        # sql
        sql = "SELECT min(exe_sta) AS exe_sta, count(*) AS count FROM sql_nttgw_dat GROUP BY exe_sta;"
        sql_data = sql_config.mz_sql(sql)

        for dt in sql_data:
            if dt["exe_sta"] == "import":
                import_cnt = dt["count"]

            if dt["exe_sta"] == "update":
                update_cnt = dt["count"]

            if dt["exe_sta"] == "store":
                store_cnt = dt["count"]

            if dt["exe_sta"] == "not_store":
                not_store_cnt = dt["count"]

        # all cnt
        all_cnt = import_cnt + update_cnt + store_cnt + not_store_cnt

        # dic
        dic = {
            "level_error": level_error,
            "import_cnt": import_cnt,
            "update_cnt": update_cnt,
            "store_cnt": store_cnt,
            "not_store_cnt": not_store_cnt,
            "all_cnt": all_cnt,
        }
    return dic


def nttgw_store_exe():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    user_email = base_data["google_account_email"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "send_email": "",
        }
    else:
        # task que
        que_project = fs_dic["project_name"]
        que_location = fs_dic["que_location"]
        que_id = fs_dic["que_id"]
        que_url = fs_dic["que_site"] + "/nttgw/store_task"

        que_body = {
            "js_obj": json.loads(request.data.decode("utf-8")),
            "project_name": fs_dic["project_name"],
            "bucket_name": fs_dic["upload_gcs_bucket"],
            "sender_email": fs_dic["sender_email"],
            "service": fs_dic["project_name"],
            "user_email": user_email,
        }
        mod_que.mz_que(que_project, que_location, que_id, que_url, que_body)

        dic = {
            "level_error": level_error,
            "send_email": user_email,
        }
    return dic


def nttgw_store_task():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # obj
    obj = request.get_json()
    js_obj = obj["js_obj"]
    jwtg = js_obj["jwtg"]

    # value
    user_email = obj["user_email"]
    start_time = mod_datetime.mz_tnow("for_datetime")
    from_email = obj["sender_email"]
    to_email = obj["user_email"]
    service = obj["service"]

    # exe
    today_num = mod_datetime.mz_now_date_num()
    execute_cnt = 0
    execute_cnt_all = 0

    # init -> 初期データ
    # 0 -> 新契約
    # 1 -> 既データ提供契約と今回提供契約とで相違がある場合
    # 2 -> 解約
    # 3 -> 新契約取消
    # 4 -> 異動取消
    # 5 -> 解約取消
    # 6 ->
    # 9 -> 強制削除
    # init_tei_list = ('init', '0', '1', '2', '3', '4', '5', '6', '9')

    init_tei_list = ("0", "1", "2")
    for init_tei_cd in init_tei_list:
        execute_cnt = mz_store(init_tei_cd, user_email, today_num)
        execute_cnt_all += execute_cnt

    # sendgrid subject/body
    end_time = mod_datetime.mz_tnow("for_datetime")
    subject_data = "nttgw_dat → order_store"
    body_data = ""
    body_data += "\n"
    body_data += "nttgw_dat, store = " + str(execute_cnt_all) + "\n\n"
    body_data += "処理開始時刻：" + start_time + "\n"
    body_data += "処理終了時刻：" + end_time + "\n"
    body_data += "service : " + service + "\n"
    body_data += "\n"

    # sendgrid
    from_email = Email(from_email)
    to_email = To(to_email)
    subject = subject_data
    content = Content("text/plain", body_data)
    mail_con = Mail(from_email, to_email, subject, content)

    # send
    sg = sendgrid.SendGridAPIClient(fs_dic["sendgrid_api_key"])
    sg.send(mail_con)

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(9, jwtg, acc_page_name)

    # dic
    dic = {}
    return dic


# [新規・更改・異動・解約]登録する
def mz_store(init_tei_cd, user_email, today_num):
    # init
    sql_data = []
    execute_cnt = 0

    sql = (
        "SELECT * FROM sql_nttgw_dat"
        + " WHERE"
        + " exe_sta = "
        + '"'
        + "update"
        + '"'
        + " AND"
        + " init_tei_cd = "
        + '"'
        + init_tei_cd
        + '"'
        + " ORDER BY mousikomi_date, ido_kai_date"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)

    for dt in sql_data:
        # 作成日付　社内計上年月　契約状況
        create_date = today_num
        keijyo_date = dt["keijyo_date"]
        keiyaku_cd = dt["keiyaku_cd"]

        # 証券番号
        syoken_cd_main = dt["syoken_cd_main"]
        syoken_cd_sub = dt["syoken_cd_sub"]

        # 旧証券番号
        old_syoken_cd_main = dt["old_syoken_cd_main"]
        old_syoken_cd_sub = dt["old_syoken_cd_sub"]
        mosikomi_cd = ""

        # pay num, hoken_ryo
        pay_num_cd = dt["pay_num_cd"].replace(" ", "")
        hoken_ryo = dt["hoken_ryo"]
        hoken_ryo_year = dt["hoken_ryo_year"]

        # 保険期間
        hoken_kikan_cd = "0"
        hoken_kikan_year = 0

        cat_cd = dt["cat_cd"]
        coltd_cd = dt["coltd_cd"]

        bosyu_cd = dt["bosyu_cd"]
        (
            section_cd,
            staff1_cd,
            staff2_cd,
            staff3_cd,
            gyotei1_cd,
            gyotei2_cd,
            gyotei3_cd,
        ) = mod_bosyu.mz_bosyu_section_staff(bosyu_cd)
        fee_staff1 = 100
        fee_staff2 = 0
        fee_staff3 = 0
        fee_gyotei1 = 0
        fee_gyotei2 = 0
        fee_gyotei3 = 0
        fee_memo = ""

        # kind, fee 作成中
        kind_cd_main = dt["kind_cd_main"]
        kind_cd_sub = dt["kind_cd_sub"].replace(" ", "")

        fee_cd, fee_cd_all, fee_cat, fee_ritu = mod_fee.mz_fee_conv(dt["cat_cd"], dt["kind_cd_main"])

        fee_cd = fee_cd
        fee_cd_all = fee_cd_all

        fee_cat = fee_cat
        fee_ritu = fee_ritu

        fee_seiho_kikan = 0
        fee_seiho_first = 0
        fee_seiho_next = 0

        memo = ""
        temp = []
        memo_json = json.dumps(temp)
        memo, memo_json = mod_memo_json.mz_memo_json("nttgw@fujitomi.jp", memo, memo_json)

        # nttgw
        exe_sta = "nttgw"

        ngw_keijyo_date = dt["keijyo_date"]
        siki_date = dt["siki_date"]
        manki_date = dt["manki_date"]
        ido_kai_date = dt["ido_kai_date"]
        ido_kai_hoken_ryo = dt["ido_kai_hoken_ryo"]

        hojin_kojin_cd = dt["hojin_kojin_cd"]
        kei_name = dt["kei_name"]
        kei_name_nospace = (kei_name.replace("　", "")).replace(" ", "")
        kei_name_hira = dt["kei_name_hira"]
        kei_post = dt["kei_post"]
        kei_address = dt["kei_address"]
        kei_tel = dt["kei_tel"]

        # 新規顧客・既存顧客・不明
        cust_new_old_cd = "0"

        # 検索用
        search_text = mod_common.mz_search_text_conv(
            dt["syoken_cd_main"],
            dt["old_syoken_cd_main"],
            dt["kei_name"],
            dt["kei_name_hira"],
        )

        valid_cd = mod_valid_cd.mz_valid_cd_create(keiyaku_cd, coltd_cd, syoken_cd_main, syoken_cd_sub)

        create_email = "nttgw@fujitomi.jp"
        update_email = "nttgw@fujitomi.jp"
        regi_email = "nttgw@fujitomi.jp"
        regi_time = datetime.datetime.now() + datetime.timedelta(hours=9)

        # 異動で０円は処理しない、fis番号も生成しない
        if keiyaku_cd == "7" and ido_kai_hoken_ryo == 0:
            pass
        else:
            # fis番号生成
            fis_cd = mod_fis_cd.mz_fis_cd(user_email)

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
                    fee_cd,
                    fee_cd_all,
                    fee_cat,
                    fee_ritu,
                    fee_seiho_kikan,
                    fee_seiho_first,
                    fee_seiho_next,
                    exe_sta,
                    ngw_keijyo_date,
                    siki_date,
                    manki_date,
                    ido_kai_hoken_ryo,
                    ido_kai_date,
                    hojin_kojin_cd,
                    kei_name,
                    kei_name_nospace,
                    kei_name_hira,
                    kei_post,
                    kei_address,
                    kei_tel,
                    cust_new_old_cd,
                    memo,
                    memo_json,
                    bosyu_cd,
                    search_text,
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
                        fee_cd,
                        fee_cd_all,
                        fee_cat,
                        fee_ritu,
                        fee_seiho_kikan,
                        fee_seiho_first,
                        fee_seiho_next,
                        exe_sta,
                        ngw_keijyo_date,
                        siki_date,
                        manki_date,
                        ido_kai_hoken_ryo,
                        ido_kai_date,
                        hojin_kojin_cd,
                        kei_name,
                        kei_name_nospace,
                        kei_name_hira,
                        kei_post,
                        kei_address,
                        kei_tel,
                        cust_new_old_cd,
                        memo,
                        memo_json,
                        bosyu_cd,
                        search_text,
                        valid_cd,
                        create_email,
                        update_email,
                        regi_email,
                        regi_time,
                    ),
                )
                sql_con.commit()
                execute_cnt += 1

            # order_store_log
            mod_order_store_log.mz_insert_log(sys._getframe().f_code.co_name, fis_cd)

    # update exe_sta
    # 損保の場合、init_tei_cd
    # 「3 -> 新契約取消」
    # 「4 -> 異動取消」
    # これらを省略しているで、全てが更新されない
    sql = (
        "UPDATE sql_nttgw_dat SET"
        + " exe_sta = "
        + '"'
        + "store"
        + '"'
        + " WHERE"
        + " exe_sta = "
        + '"'
        + "update"
        + '"'
        + " AND"
        + " init_tei_cd = "
        + '"'
        + init_tei_cd
        + '"'
        + ";"
    )
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        cur.execute(
            sql,
        )
        sql_con.commit()

    return execute_cnt
