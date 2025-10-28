import sys
from decimal import Decimal
from flask import request
from _mod import mod_base, sql_config
from _mod_fis import mod_common, mod_meisai, mod_nttgw_modal


def store_modal_select():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    fis_cd = obj["fis_cd"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "dic_modal": [],
        }
    else:
        # sql
        store_data = store_modal_select_sql(fis_cd)

        # dic_modal
        dic_modal = {}
        dic_modal["meisai_data_showhide"] = "hide"
        dic_modal["meisai_data"] = ""

        # 日付はjson変換でエラーが出るため
        for key, value in store_data[0].items():
            if key == "create_time":
                dic_modal[key] = mod_common.mz_datetime_view(value)
            elif key == "update_time":
                dic_modal[key] = mod_common.mz_datetime_view(value)
            elif key == "regi_time":
                dic_modal[key] = mod_common.mz_datetime_view(value)

            # elif key == 'hoken_kikan_cd':
            #     dic_modal[key] = value
            #     if value == '9999':
            #         dic_modal['hoken_kikan_year_showhide'] = 'show'
            #     else:
            #         dic_modal['hoken_kikan_year_showhide'] = 'hide'

            else:
                dic_modal[key] = value

        # fee_total
        dic_modal["fee_total"] = str(
            Decimal(dic_modal["fee_staff1"])
            + Decimal(dic_modal["fee_staff2"])
            + Decimal(dic_modal["fee_staff3"])
            + Decimal(dic_modal["fee_gyotei1"])
            + Decimal(dic_modal["fee_gyotei2"])
            + Decimal(dic_modal["fee_gyotei3"])
        )

        dic = {
            "level_error": level_error,
            "dic_modal": dic_modal,
        }
    return dic


def store_modal_select_sql(fis_cd):
    sql = "SELECT * FROM sql_order_store WHERE fis_cd = " + str(fis_cd) + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


def store_modal_meisai():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    syoken_cd_main = obj["syoken_cd_main"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "meisai_data": [],
        }
    else:
        meisai_data = mod_meisai.mz_meisai_data(syoken_cd_main)
        dic = {
            "level_error": level_error,
            "meisai_data": meisai_data,
        }
    return dic


def store_modal_nttgw():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    cat_cd = obj["cat_cd"]
    syoken_cd_main = obj["syoken_cd_main"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "nttgw_data": [],
        }
    else:
        nttgw_data = ""

        # nttgw_data
        if syoken_cd_main != "":
            nttgw_data = mod_nttgw_modal.mz_nttgw_search(cat_cd, syoken_cd_main)

        dic = {
            "level_error": level_error,
            "nttgw_data": nttgw_data,
        }
    return dic


def store_modal_nttgw_import():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    id = obj["id"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "nttgw_import": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "nttgw_import": mod_nttgw_modal.mz_nttgw_import(id),
        }
    return dic
