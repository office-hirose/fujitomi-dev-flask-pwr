import sys
import json
from decimal import Decimal
import datetime
from flask import request
from _mod import mod_base, mod_datetime, sql_config
from _mod_fis import (
    mod_common,
    mod_fis_cd,
    mod_valid_cd,
    mod_order_store_log,
    mod_memo_json,
)
from store import store_sql


def store_modal_insert():
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
        # sql update
        fis_cd = store_modal_insert_sql(dic_modal, user_email, jwtg)

        # list
        store_data = store_sql.fis_cd_sql(fis_cd)

        dic = {
            "level_error": level_error,
            "store_data": store_data,
        }
    return dic


def store_modal_insert_sql(dic_modal, user_email, jwtg):
    fis_cd = mod_fis_cd.mz_fis_cd(user_email)
    create_date = mod_datetime.mz_now_date_num()

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

    temp = []
    memo_json = json.dumps(temp)
    memo, memo_json = mod_memo_json.mz_memo_json(user_email, dic_modal["memo"], memo_json)

    # insert
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = """
        INSERT INTO sql_order_store (
            exe_sta,
            fis_cd,
            create_date,
            keijyo_date,
            ngw_keijyo_date,
            keiyaku_cd,
            syoken_cd_main,
            syoken_cd_sub,
            old_syoken_cd_main,
            old_syoken_cd_sub,
            mosikomi_cd,
            hoken_ryo,
            hoken_ryo_year,
            ido_kai_hoken_ryo,
            ido_kai_date,
            pay_num_cd,
            siki_date,
            manki_date,
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
            fee_cat,
            fee_ritu,
            fee_seiho_kikan,
            fee_seiho_first,
            fee_seiho_next,
            kei_name,
            kei_name_hira,
            kei_post,
            kei_address,
            kei_tel,
            memo,
            memo_json,
            bosyu_cd,
            search_text,
            kei_name_nospace,
            create_email,
            update_email,
            regi_email,
            regi_time,
            valid_cd
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
            %s
        );
        """
        cur = sql_con.cursor()
        cur.execute(
            sql,
            (
                "hand",
                fis_cd,
                create_date,
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
                user_email,  # create_email
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

    return fis_cd
