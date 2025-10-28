import sys
from flask import request
from _mod import mod_base, sql_config


def oyaeda():
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
            "oyaeda_data_all": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "oyaeda_data_all": oyaeda_data_sql(),
        }
    return dic


# 親番・枝番で担当・提携が合致しているか
# 損保のみ、生保の場合は枝番が存在しないので別のクエリが必要
# PythonでFORで回す必要があるかもしれない
def oyaeda_data_sql():
    sql = """
        SELECT
            max( eda_syoken_main ) AS syoken_cd_main
        FROM
            (
            SELECT
                eda.syoken_cd_main AS eda_syoken_main,
                eda.syoken_cd_sub AS eda_syoken_sub,
                eda.staff1_cd AS eda_staff1,
                eda.staff2_cd AS eda_staff2,
                eda.staff3_cd AS eda_staff3,
                eda.gyotei1_cd AS eda_gyotei1,
                eda.gyotei2_cd AS eda_gyotei2,
                eda.gyotei3_cd AS eda_gyotei3,
                eda.fee_staff1 AS eda_fee_staff1,
                eda.fee_staff2 AS eda_fee_staff2,
                eda.fee_staff3 AS eda_fee_staff3,
                eda.fee_gyotei1 AS eda_fee_gyotei1,
                eda.fee_gyotei2 AS eda_fee_gyotei2,
                eda.fee_gyotei3 AS eda_fee_gyotei3,
                oya.syoken_cd_main AS oya_syoken_main,
                oya.syoken_cd_sub AS oya_syoken_sub,
                oya.staff1_cd AS oya_staff1,
                oya.staff2_cd AS oya_staff2,
                oya.staff3_cd AS oya_staff3,
                oya.gyotei1_cd AS oya_gyotei1,
                oya.gyotei2_cd AS oya_gyotei2,
                oya.gyotei3_cd AS oya_gyotei3,
                oya.fee_staff1 AS oya_fee_staff1,
                oya.fee_staff2 AS oya_fee_staff2,
                oya.fee_staff3 AS oya_fee_staff3,
                oya.fee_gyotei1 AS oya_fee_gyotei1,
                oya.fee_gyotei2 AS oya_fee_gyotei2,
                oya.fee_gyotei3 AS oya_fee_gyotei3
            FROM
                ( SELECT * FROM sql_order_store WHERE cat_cd = '2' AND syoken_cd_sub != '0000' ) AS eda
                LEFT JOIN
                ( SELECT * FROM sql_order_store WHERE cat_cd = @cat_cd AND syoken_cd_sub = '0000' ) AS oya
                ON eda.syoken_cd_main = oya.syoken_cd_main
            ORDER BY
                eda.syoken_cd_main,
                eda.syoken_cd_sub
            ) AS total
        WHERE
            eda_staff1 != oya_staff1 OR
            eda_staff2 != oya_staff2 OR
            eda_staff3 != oya_staff3 OR
            eda_gyotei1 != oya_gyotei1 OR
            eda_gyotei2 != oya_gyotei2 OR
            eda_gyotei3 != oya_gyotei3 OR
            eda_fee_staff1 != oya_fee_staff1 OR
            eda_fee_staff2 != oya_fee_staff2 OR
            eda_fee_staff3 != oya_fee_staff3 OR
            eda_fee_gyotei1 != oya_fee_gyotei1 OR
            eda_fee_gyotei2 != oya_fee_gyotei2 OR
            eda_fee_gyotei3 != oya_fee_gyotei3
        GROUP BY
            eda_syoken_main;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data
