import sys
from flask import request
from _mod import mod_base, sql_config


def allocation():
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
            "allocation_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "allocation_data_all": allocation_data_sql(),
        }
    return dic


def allocation_data_sql():
    sql = """
        SELECT
        fis_cd,
        cat_cd,
        coltd_cd,
        syoken_cd_main,
        syoken_cd_sub,
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
        fee_gyotei3

        FROM sql_order_store
        WHERE
        (staff1_cd = 'empty@tokyo' and fee_staff1 != 0) OR
        (staff2_cd = 'empty@tokyo' and fee_staff2 != 0) OR
        (staff3_cd = 'empty@tokyo' and fee_staff3 != 0) OR

        (staff1_cd = 'empty@fukuoka' and fee_staff1 != 0) OR
        (staff2_cd = 'empty@fukuoka' and fee_staff2 != 0) OR
        (staff3_cd = 'empty@fukuoka' and fee_staff3 != 0) OR

        (staff1_cd = 'empty@kumamoto1' and fee_staff1 != 0) OR
        (staff2_cd = 'empty@kumamoto1' and fee_staff2 != 0) OR
        (staff3_cd = 'empty@kumamoto1' and fee_staff3 != 0) OR

        (staff1_cd = 'empty@kumamoto2' and fee_staff1 != 0) OR
        (staff2_cd = 'empty@kumamoto2' and fee_staff2 != 0) OR
        (staff3_cd = 'empty@kumamoto2' and fee_staff3 != 0) OR

        (staff1_cd = 'empty@kyuto' and fee_staff1 != 0) OR
        (staff2_cd = 'empty@kyuto' and fee_staff2 != 0) OR
        (staff3_cd = 'empty@kyuto' and fee_staff3 != 0) OR

        (gyotei1_cd = '99990001' AND fee_gyotei1 != 0) OR
        (gyotei2_cd = '99990001' AND fee_gyotei2 != 0) OR
        (gyotei3_cd = '99990001' AND fee_gyotei3 != 0);
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data
