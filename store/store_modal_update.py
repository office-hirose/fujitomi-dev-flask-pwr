import sys
from decimal import Decimal
import datetime
from flask import request
from _mod import mod_base, sql_config
from _mod_fis import mod_common, mod_valid_cd, mod_order_store_log, mod_memo_json
from store import store_sql


# exe
def store_modal_update():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    dic_modal = obj["dic_modal"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    user_email = base_data["google_account_email"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "store_data": [],
        }
    else:
        fnd_status = obj["fnd_status"]
        cat_cd = obj["cat_cd"]
        keijyo_date = int(obj["keijyo_date"])
        section_cd = obj["section_cd"]
        staff_cd = obj["staff_cd"]
        keiyaku_cd = obj["keiyaku_cd"]
        coltd_cd = obj["coltd_cd"]
        search_text = obj["search_text"]

        # sql update
        store_modal_update_sql(dic_modal, user_email, jwtg)

        # list or search
        if fnd_status == "list":
            store_data = store_sql.list_sql(cat_cd, keijyo_date, section_cd, staff_cd, keiyaku_cd, coltd_cd)
        if fnd_status == "search":
            if search_text == "":
                store_data = ""
            else:
                store_data = store_sql.search_sql(cat_cd, search_text)

        dic = {
            "level_error": level_error,
            "store_data": store_data,
        }
    return dic


def store_modal_update_sql(dic_modal, user_email, jwtg):
    fis_cd = dic_modal["fis_cd"]

    ido_kai_date = mod_common.mz_ido_kai_date_conv(dic_modal["ido_kai_date"])
    siki_date = mod_common.mz_siki_date_conv(dic_modal["siki_date"])
    manki_date = mod_common.mz_manki_date_conv(dic_modal["manki_date"])

    kei_name = mod_common.mz_kei_name_conv(dic_modal["kei_name"])
    kei_name_hira = mod_common.mz_kei_name_conv(dic_modal["kei_name_hira"])

    search_text = mod_common.mz_search_text_conv(
        dic_modal["syoken_cd_main"],
        dic_modal["old_syoken_cd_main"],
        kei_name,
        kei_name_hira,
    )
    kei_name_nospace = mod_common.mz_kei_name_nospace_conv(kei_name)
    valid_cd = mod_valid_cd.mz_valid_cd_create(
        dic_modal["keiyaku_cd"],
        dic_modal["coltd_cd"],
        dic_modal["syoken_cd_main"],
        dic_modal["syoken_cd_sub"],
    )
    memo, memo_json = mod_memo_json.mz_memo_json(user_email, dic_modal["memo"], dic_modal["memo_json"])

    # sql
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = (
            "UPDATE sql_order_store SET "
            + "keijyo_date = %s, "
            + "ngw_keijyo_date = %s, "
            + "keiyaku_cd = %s, "
            + "syoken_cd_main = %s, "
            + "syoken_cd_sub = %s, "
            + "old_syoken_cd_main = %s, "
            + "old_syoken_cd_sub = %s, "
            + "mosikomi_cd = %s, "
            + "hoken_ryo = %s, "
            + "hoken_ryo_year = %s, "
            + "ido_kai_hoken_ryo = %s, "
            + "ido_kai_date = %s, "
            + "pay_num_cd = %s, "
            + "siki_date = %s, "
            + "manki_date = %s, "
            + "hoken_kikan_cd = %s, "
            + "hoken_kikan_year = %s, "
            + "section_cd = %s, "
            + "staff1_cd = %s, "
            + "staff2_cd = %s, "
            + "staff3_cd = %s, "
            + "gyotei1_cd = %s, "
            + "gyotei2_cd = %s, "
            + "gyotei3_cd = %s, "
            + "fee_staff1 = %s, "
            + "fee_staff2 = %s, "
            + "fee_staff3 = %s, "
            + "fee_gyotei1 = %s, "
            + "fee_gyotei2 = %s, "
            + "fee_gyotei3 = %s, "
            + "fee_memo = %s, "
            + "cat_cd = %s, "
            + "coltd_cd = %s, "
            + "kind_cd_main = %s, "
            + "kind_cd_sub = %s, "
            + "fee_cd = %s, "
            + "fee_cat = %s, "
            + "fee_ritu = %s, "
            + "fee_seiho_kikan = %s, "
            + "fee_seiho_first = %s, "
            + "fee_seiho_next = %s, "
            + "kei_name = %s, "
            + "kei_name_hira = %s, "
            + "kei_post = %s, "
            + "kei_address = %s, "
            + "kei_tel = %s, "
            + "memo = %s, "
            + "memo_json = %s, "
            + "bosyu_cd = %s, "
            + "search_text = %s, "
            + "kei_name_nospace = %s, "
            + "update_email = %s, "
            + "regi_email = %s, "
            + "regi_time = %s, "
            + "valid_cd = %s "
            + "WHERE fis_cd = "
            + '"'
            + fis_cd
            + '"'
            + ";"
        )
        cur = sql_con.cursor()
        cur.execute(
            sql,
            (
                int(dic_modal["keijyo_date"]),
                int(dic_modal["ngw_keijyo_date"]),
                dic_modal["keiyaku_cd"],
                dic_modal["syoken_cd_main"],
                dic_modal["syoken_cd_sub"],
                dic_modal["old_syoken_cd_main"],
                dic_modal["old_syoken_cd_sub"],
                dic_modal["mosikomi_cd"],
                int(dic_modal["hoken_ryo"]),
                int(dic_modal["hoken_ryo_year"]),
                int(dic_modal["ido_kai_hoken_ryo"]),
                ido_kai_date,
                dic_modal["pay_num_cd"],
                siki_date,
                manki_date,
                dic_modal["hoken_kikan_cd"],
                int(dic_modal["hoken_kikan_year"]),
                dic_modal["section_cd"],
                dic_modal["staff1_cd"],
                dic_modal["staff2_cd"],
                dic_modal["staff3_cd"],
                dic_modal["gyotei1_cd"],
                dic_modal["gyotei2_cd"],
                dic_modal["gyotei3_cd"],
                Decimal(dic_modal["fee_staff1"]),
                Decimal(dic_modal["fee_staff2"]),
                Decimal(dic_modal["fee_staff3"]),
                Decimal(dic_modal["fee_gyotei1"]),
                Decimal(dic_modal["fee_gyotei2"]),
                Decimal(dic_modal["fee_gyotei3"]),
                dic_modal["fee_memo"],
                dic_modal["cat_cd"],
                dic_modal["coltd_cd"],
                dic_modal["kind_cd_main"],
                dic_modal["kind_cd_sub"],
                dic_modal["fee_cd"],
                dic_modal["fee_cat"],
                int(dic_modal["fee_ritu"]),
                int(dic_modal["fee_seiho_kikan"]),
                int(dic_modal["fee_seiho_first"]),
                int(dic_modal["fee_seiho_next"]),
                dic_modal["kei_name"],
                dic_modal["kei_name_hira"],
                dic_modal["kei_post"],
                dic_modal["kei_address"],
                dic_modal["kei_tel"],
                memo,
                memo_json,
                dic_modal["bosyu_cd"],
                search_text,
                kei_name_nospace,
                user_email,  # update_email
                user_email,  # regi_email
                datetime.datetime.now() + datetime.timedelta(hours=9),  # regi_time
                valid_cd,
            ),
        )
        sql_con.commit()

    # order_store_log
    mod_order_store_log.mz_insert_log(sys._getframe().f_code.co_name, fis_cd)

    # base - level 2 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(2, jwtg, acc_page_name)

    return
