from _mod import sql_config


# 入金金額/更新
def mz_update(modal_nk_data):
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        for dt in modal_nk_data:
            sql = """
            UPDATE
                sql_fee_nyukin
            SET
                nyukin_withtax = %s,
                nyukin_notax = %s,
                nyukin_tax_num = %s
            WHERE
                id = %s;
            """
            cur.execute(
                sql,
                (
                    int(dt["nyukin_withtax"]),
                    int(dt["nyukin_notax"]),
                    int(dt["nyukin_tax_num"]),
                    dt["id"],
                ),
            )
        sql_con.commit()
    return


# 入金金額/計算
def mz_calc(modal_nk_data):
    # init
    id = 0
    sum_nyukin_withtax = 0
    sum_nyukin_notax = 0
    sum_nyukin_tax_num = 0

    for dt in modal_nk_data:
        if dt["nyukin_cd"] == 11:
            id = dt["id"]
        else:
            if dt["nyukin_cd"] != 10:
                sum_nyukin_withtax += int(dt["nyukin_withtax"])
                sum_nyukin_notax += int(dt["nyukin_notax"])
                sum_nyukin_tax_num += int(dt["nyukin_tax_num"])

    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        sql = """
        UPDATE
            sql_fee_nyukin
        SET
            nyukin_withtax = %s,
            nyukin_notax = %s,
            nyukin_tax_num = %s
        WHERE
            id = %s;
        """
        cur.execute(
            sql,
            (
                sum_nyukin_withtax,
                sum_nyukin_notax,
                sum_nyukin_tax_num,
                id,
            ),
        )
        sql_con.commit()

    return
