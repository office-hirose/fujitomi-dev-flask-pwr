import sys
from flask import request
from _mod import mod_base, sql_config


def space_fee():
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
            "space_fee_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "space_fee_data_all": space_fee_data_sql(),
        }
    return dic


def space_fee_data_sql():
    sql = """
        select
        *
        from
        sql_fee_store
        where
        syoken_cd_main like '%　%'
        or
        syoken_cd_main like '% %'
        or
        syoken_cd_sub like '%　%'
        or
        syoken_cd_sub like '% %'
        ;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data
