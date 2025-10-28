from _mod import sql_config, mod_datetime


# fis番号生成, seq number, check degit なし
def mz_fis_cd(user_email):
    fis_create_date = mod_datetime.mz_now_date()
    create_yy = fis_create_date[2:4]
    create_mm = fis_create_date[5:7]
    cat = 1

    sql = "SELECT * FROM sql_order_seq WHERE cat = " + str(cat) + ";"
    sql_data = sql_config.mz_sql(sql)

    for dt in sql_data:
        id = dt["id"]
        seq = dt["seq"]
        month = dt["month"]

    # 申込受付日の月とDBの月が相違していた場合、seqを1にする、月が変わった場合、1からスタート
    if int(create_mm) == month:
        # 同じ月の場合 seq + 1
        seq = seq + 1
    else:
        # 違う月の場合 1からスタート
        seq = 1

    # CDなしの番号作成、前ゼロで埋める str.zfill(n)
    fis_cd = create_yy + create_mm.zfill(2) + str(cat) + str(seq).zfill(6)

    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = (
            "UPDATE sql_order_seq SET"
            + " year = %s,"
            + " month = %s,"
            + " cat = %s,"
            + " seq = %s,"
            + " update_email = %s"
            + " WHERE"
            + " id = "
            + str(id)
            + ";"
        )
        cur = sql_con.cursor()
        cur.execute(sql, (int(create_yy), int(create_mm), cat, seq, user_email))
        sql_con.commit()

    return fis_cd
