# ------------------------------------------------------------------------
#  nttgw_update.py
#  |--nttgw_update      - 画面作成
#  |--nttgw_update_cnt  - カウント表示
#  |--nttgw_update_exe  - 実行する
#  |--nttgw_update_task - task que
# ------------------------------------------------------------------------
import sys
import json
from flask import request
from _mod import fs_config, mod_base, mod_que, mod_datetime, sql_config
from _mod_fis import mod_nttgw_conv
import jaconv
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, To


def nttgw_update():
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


def nttgw_update_cnt():
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

        dic = {
            "level_error": level_error,
            "import_cnt": import_cnt,
            "update_cnt": update_cnt,
            "store_cnt": store_cnt,
            "not_store_cnt": not_store_cnt,
            "all_cnt": all_cnt,
        }
    return dic


def nttgw_update_exe():
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
        que_url = fs_dic["que_site"] + "/nttgw/update_task"
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


def nttgw_update_task():
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

    # update
    execute_cnt = mz_nttgw_update_update(user_email)

    # sendgrid subject/body
    end_time = mod_datetime.mz_tnow("for_datetime")
    subject_data = "nttgw_dat, update"
    body_data = ""
    body_data += "\n"
    body_data += "nttgw_dat, update = " + str(execute_cnt) + "\n\n"
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


def mz_nttgw_update_update(user_email):
    # init
    sql_data = []
    execute_cnt = 0
    exe_sta = "import"

    sql = "SELECT * FROM sql_nttgw_dat WHERE exe_sta = " + '"' + exe_sta + '"' + ";"
    sql_data = sql_config.mz_sql(sql)

    for dt in sql_data:
        id = dt["id"]
        temp_text = dt["temp_text"]
        exe_sta = "update"

        # init_tei_cd, init=初期データ、その他は定期データでそれぞれのCD
        init_tei_cd_temp = temp_text[0:1]  # 0-1char
        if init_tei_cd_temp == " ":
            init_tei_cd = "init"
        else:
            init_tei_cd = init_tei_cd_temp

        # kind_cd_main, kind_cd_sub
        kind_cd_main = temp_text[1:3]  # 2-2char 保険種目(kind main, AA=生保の判断)
        kind_cd_sub = temp_text[21:23]  # 22-2char 保険種類(kind sub)

        # seiho
        if kind_cd_main == "AA":
            cat_cd = "1"  # 生保

            old_syoken_cd_main = ""
            old_syoken_cd_sub = ""

            kei_name_start = 1132
            kei_address = (temp_text[1078:1128]).replace(" ", "")  # 1079-50char 契約者住所漢字
            kei_name = (temp_text[1131:1161]).replace(" ", "")  # 1132-30char 契約者氏名漢字

            bosyu_cd = (temp_text[846:859]).replace(" ", "")  # 847-13char 募集人CD 生保
            bosyu_cd_start = 847
            bosyu_cd_len = 13
            hoken_kin_jisin = 0
            hoken_ryo_jisin = 0

        # seiho/sonpo
        if kind_cd_main != "AA":
            cat_cd = "2"  # 損保

            old_syoken_cd_main = (temp_text[1069:1081]).replace(" ", "")  # 1070-12char 旧証券番号main
            old_syoken_cd_sub = (temp_text[1082:1086]).replace(
                " ", ""
            )  # 1082-5char 旧証券番号sub マニュアル意味不明なので正しくは、1083-4char

            kei_name_start = 1253
            kei_address = (temp_text[1199:1249]).replace(" ", "")  # 1200-50char 契約者住所漢字
            kei_name = (temp_text[1252:1282]).replace(" ", "")  # 1253-30char 契約者氏名漢字

            bosyu_cd = (temp_text[347:357]).replace(" ", "")  # 348-10char 募集人CD 損保
            bosyu_cd_start = 348
            bosyu_cd_len = 10
            hoken_kin_jisin_str = (temp_text[426:433]).replace(" ", "")  # 427-7char 種目が[火災]、地震保険金
            hoken_ryo_jisin_str = (temp_text[433:442]).replace(" ", "")  # 434-9char 種目が[火災]、地震保険料
            hoken_kin_jisin = (mod_nttgw_conv.mz_nttgw_fugo_conv(hoken_kin_jisin_str)) * 10000  # 万円単位
            hoken_ryo_jisin = mod_nttgw_conv.mz_nttgw_fugo_conv(hoken_ryo_jisin_str)

        # pay_num_cd
        pay_num_cd = temp_text[311:313]  # 312-2char 払込方法(分割種類)

        # hoken_ryo
        bun_temp = (temp_text[301:311]).replace(
            " ", ""
        )  # 302-10char 分割払契約1回分保険料　ZEROの場合一時払契約、符号なし
        if bun_temp == "":
            bun = 0
        else:
            bun = int(bun_temp)

        # hoken_ryo_year
        total_temp = (temp_text[70:80]).replace(" ", "")  # 71-10char  合計保険料2、符号あり
        if total_temp == "":
            total = 0
        else:
            total = mod_nttgw_conv.mz_nttgw_fugo_conv(total_temp)

        hoken_ryo, hoken_ryo_year = mod_nttgw_conv.mz_hoken_ryo_conv(pay_num_cd, bun, total)

        # syoken_cd
        syoken_cd_main = (temp_text[4:16]).replace(" ", "")  # 5-12char 証券番号main
        syoken_cd_sub = (temp_text[17:21]).replace(" ", "")  # 17-5char 証券番号sub スペースがあるので、18-4char
        syoken_cd_main, syoken_cd_sub = mod_nttgw_conv.mz_syoken_cd_conv("xxx", syoken_cd_main, syoken_cd_sub)
        old_syoken_cd_main, old_syoken_cd_sub = mod_nttgw_conv.mz_syoken_cd_conv(
            kind_cd_main, old_syoken_cd_main, old_syoken_cd_sub
        )

        # coltd_cd
        coltd_cd = temp_text[382:384]  # 383-2char 保険会社コード

        # 申込年月日、計上年月、始期年月日、満期年月日、異動解約日
        mousikomi_date = (temp_text[124:130]).replace(" ", "")  # 125-6char 申込年月日
        mousikomi_date = mod_nttgw_conv.mz_gene_date_conv(mousikomi_date)

        keijyo_date = (temp_text[378:382]).replace(" ", "")  # 379-4char 計上年月
        keijyo_date = mod_nttgw_conv.mz_gene_date_conv(keijyo_date)

        siki_date = (temp_text[100:106]).replace(" ", "")  # 101-6char 始期年月日
        siki_date = mod_nttgw_conv.mz_gene_date_conv(siki_date)

        manki_date = (temp_text[106:112]).replace(" ", "")  # 107-6char 満期年月日
        manki_date = mod_nttgw_conv.mz_gene_date_conv(manki_date)

        ido_kai_date = (temp_text[112:118]).replace(" ", "")  # 113-6char 異動解約日
        ido_kai_date = mod_nttgw_conv.mz_gene_date_conv(ido_kai_date)

        # 異動・解約保険料、異動・解約保険料の符号
        ido_kai_hoken_ryo_temp = (temp_text[1004:1014]).replace(" ", "")  # 1005-10char  異動・解約保険料
        ido_kai_hoken_ryo = mod_nttgw_conv.mz_nttgw_fugo_conv(ido_kai_hoken_ryo_temp)

        # 契約者情報

        # 法人個人区分、信用できないので一旦全て '0'にセットする場合
        # hojin_kojin_cd = '0'

        hojin_kojin_cd_temp = (temp_text[1002:1003]).replace(
            " ", ""
        )  # 1003-1char  法人・個人区分　法人＝'1'、個人＝'2'、不明＝'0'(FIS独自)
        if hojin_kojin_cd_temp == "":
            hojin_kojin_cd = "0"
        else:
            hojin_kojin_cd = hojin_kojin_cd_temp

        kei_post = (temp_text[83:90]).replace(" ", "")  # 84-7char 契約者郵便番号
        kei_tel = (temp_text[219:231]).replace(" ", "")  # 220-12char 契約者電話番号
        kei_name_kata = (temp_text[231:301]).replace(" ", "")  # 232-70char 契約者氏名カタカナ(カタカナは使用しない)
        kei_name_kata = jaconv.h2z(kei_name_kata)  # 契約者氏名カタカナ 半角カナ to 全角カナ
        kei_name_hira = jaconv.kata2hira(kei_name_kata)  # 契約者氏名ひらがな 全角カナ to 全角かな
        ido_reason = temp_text[347:349]  # 348-2char 異動理由
        keiyaku_cd = mod_nttgw_conv.mz_keiyaku_conv(init_tei_cd, old_syoken_cd_main + old_syoken_cd_sub, ido_reason)
        update_email = user_email

        # sql
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = (
                "UPDATE sql_nttgw_dat SET "
                + " exe_sta = %s,"
                + " init_tei_cd = %s,"
                + " keiyaku_cd = %s,"
                + " cat_cd = %s,"
                + " coltd_cd = %s,"
                + " kind_cd_main = %s,"
                + " kind_cd_sub = %s,"
                + " pay_num_cd = %s,"
                + " hoken_ryo = %s,"
                + " hoken_ryo_year = %s,"
                + " syoken_cd_main = %s,"
                + " syoken_cd_sub = %s,"
                + " old_syoken_cd_main = %s,"
                + " old_syoken_cd_sub = %s,"
                + " mousikomi_date = %s,"
                + " keijyo_date = %s,"
                + " siki_date = %s,"
                + " manki_date = %s,"
                + " ido_kai_date = %s,"
                + " ido_kai_hoken_ryo = %s,"
                + " hojin_kojin_cd = %s,"
                + " kei_post = %s,"
                + " kei_address = %s,"
                + " kei_name = %s,"
                + " kei_name_hira = %s,"
                + " kei_tel = %s,"
                + " kei_name_start = %s,"
                + " bosyu_cd = %s,"
                + " bosyu_cd_start = %s,"
                + " bosyu_cd_len = %s,"
                + " hoken_kin_jisin = %s,"
                + " hoken_ryo_jisin = %s,"
                + " ido_reason = %s,"
                + " update_email = %s"
                + " WHERE"
                + " id = "
                + str(id)
                + ";"
            )
            cur = sql_con.cursor()
            cur.execute(
                sql,
                (
                    exe_sta,
                    init_tei_cd,
                    keiyaku_cd,
                    cat_cd,
                    coltd_cd,
                    kind_cd_main,
                    kind_cd_sub,
                    pay_num_cd,
                    hoken_ryo,
                    hoken_ryo_year,
                    syoken_cd_main,
                    syoken_cd_sub,
                    old_syoken_cd_main,
                    old_syoken_cd_sub,
                    mousikomi_date,
                    keijyo_date,
                    siki_date,
                    manki_date,
                    ido_kai_date,
                    ido_kai_hoken_ryo,
                    hojin_kojin_cd,
                    kei_post,
                    kei_address,
                    kei_name,
                    kei_name_hira,
                    kei_tel,
                    kei_name_start,
                    bosyu_cd,
                    bosyu_cd_start,
                    bosyu_cd_len,
                    hoken_kin_jisin,
                    hoken_ryo_jisin,
                    ido_reason,
                    update_email,
                ),
            )
            sql_con.commit()
            execute_cnt += 1

    return execute_cnt
