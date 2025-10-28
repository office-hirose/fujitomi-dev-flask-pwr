import sys
from _mod import sql_config
from _mod_fis import mod_order_store_log


# valid_cd、同じ番号の証券番号、有効無効セット
def mz_valid_cd_create(keiyaku_cd, coltd_cd, syoken_cd_main, syoken_cd_sub):
    # 引数を有効/無効にセット
    if (
        keiyaku_cd == "1"
        or keiyaku_cd == "4"
        or keiyaku_cd == "6"
        or keiyaku_cd == "8"
        or keiyaku_cd == "9"
        or keiyaku_cd == "9999"
    ):
        valid_cd = "invalid"
    else:
        valid_cd = "valid"

    # 同じ証券番号も有効/無効にする
    sql = (
        "SELECT * FROM sql_order_store"
        + " WHERE"
        + " coltd_cd = "
        + '"'
        + str(coltd_cd)
        + '"'
        + " AND"
        + " syoken_cd_main = "
        + '"'
        + str(syoken_cd_main)
        + '"'
        + " AND"
        + " syoken_cd_sub = "
        + '"'
        + str(syoken_cd_sub)
        + '"'
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        fis_cd = dt["fis_cd"]

        # valid_cdの値が同じならば更新しない
        if dt["valid_cd"] != valid_cd:
            # update
            sql_con = sql_config.mz_sql_con()
            with sql_con:
                sql = "UPDATE sql_order_store SET " + "valid_cd = %s " + "WHERE fis_cd = " + '"' + fis_cd + '"' + ";"
                cur = sql_con.cursor()
                cur.execute(
                    sql,
                    (valid_cd,),
                )
                sql_con.commit()

            # order_store_log
            mod_order_store_log.mz_insert_log(sys._getframe().f_code.co_name, fis_cd)

    return valid_cd
