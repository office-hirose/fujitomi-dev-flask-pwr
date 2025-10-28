from _mod import sql_config


# delete fee_future
def mz_del_fee_future():
    sql = "TRUNCATE sql_fee_future;"
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        cur.execute(
            sql,
        )
        sql_con.commit()
    return


# delete fee_future_cnt
def mz_del_fee_future_cnt():
    sql = "TRUNCATE sql_fee_future_cnt;"
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        cur.execute(
            sql,
        )
        sql_con.commit()
    return


# last_year, last2_year, last_month
def mz_last_year_month(nyu_date_int):
    # last year
    last_year = nyu_date_int - 100

    # last2 year
    last2_year = nyu_date_int - 200

    # last month
    year = str(nyu_date_int)
    month = str(nyu_date_int)
    yy = year[0:4]
    mm = month[4:6]

    if mm == "01":
        res_mm = "12"
        last_month = int(str(int(yy) - 1) + res_mm)
    else:
        res_mm = (str(int(mm) - 1)).zfill(2)
        last_month = int(yy + res_mm)

    return last_month, last_year, last2_year


# insert, sql_fee_future_cnt
def mz_cnt_tbl_cre(last2_year):
    sql = (
        "INSERT INTO sql_fee_future_cnt(syoken_cd_main, cnt)"
        + " SELECT min(syoken_cd_main) as syoken_cd_main, COUNT(*) as cnt FROM"
        + " ("
        + " SELECT min(syoken_cd_main) as syoken_cd_main FROM sql_fee_order_store"
        + " WHERE cat_cd = '1' AND nyu_date >= "
        + str(last2_year)
        + " GROUP BY nyu_date, syoken_cd_main"
        + " ) as temp"
        + " GROUP BY syoken_cd_main;"
    )
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        cur = sql_con.cursor()
        cur.execute(sql)
        sql_con.commit()
    return


# ---------------------------------------------------------------------------------
# 損保
# ---------------------------------------------------------------------------------


# 月払い/前月の月払いをそのままコピー
def mz_sonpo_last_month_01_06(last_month):
    sql = (
        "SELECT * FROM sql_fee_order_store"
        + " WHERE nyu_date = "
        + str(last_month)
        + " AND"
        + " cat_cd = '2'"
        + " AND"
        + " (pay_num_cd = '01' OR pay_num_cd = '06')"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 年払い/1年前の年払いをそのままコピー
def mz_sonpo_last_year_15(last_year):
    sql = (
        "SELECT * FROM sql_fee_order_store"
        + " WHERE nyu_date = "
        + str(last_year)
        + " AND"
        + " cat_cd = '2'"
        + " AND"
        + " pay_num_cd = '15'"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 一時払い/1年前の一括払いで、保険期間が1年をそのままコピー
def mz_sonpo_last_year_00(last_year):
    sql = (
        "SELECT * FROM sql_fee_order_store"
        + " WHERE nyu_date = "
        + str(last_year)
        + " AND"
        + " cat_cd = '2'"
        + " AND"
        + " pay_num_cd = '00'"
        + " AND"
        + " syoken_cd_main != 'balance'"
        + " AND"
        + " hoken_kikan_cd = '1'"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# ---------------------------------------------------------------------------------
# 生保
# ---------------------------------------------------------------------------------


# 前月が月払いで次年度/前月の月払いをそのままコピー
def mz_seiho_last_month_01_06(last_month):
    sql = (
        "SELECT * FROM sql_fee_order_store"
        + " WHERE nyu_date = "
        + str(last_month)
        + " AND"
        + " cat_cd = '1'"
        + " AND"
        + " (pay_num_cd = '01' OR pay_num_cd = '06')"
        + " AND"
        + " first_next_year = 2;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 前月が月払いで初年度で既に支払が11回以下/前月の月払いをそのままコピー
def mz_seiho_last_month_01_06_11under(last_month):
    sql = (
        "SELECT fos.*, ffc.cnt FROM sql_fee_order_store as fos"
        + " LEFT JOIN sql_fee_future_cnt as ffc on fos.syoken_cd_main = ffc.syoken_cd_main"
        + " WHERE fos.nyu_date = "
        + str(last_month)
        + " AND"
        + " fos.cat_cd = '1'"
        + " AND"
        + " (fos.pay_num_cd = '01' OR fos.pay_num_cd = '06')"
        + " AND"
        + " fos.first_next_year = 1"
        + " AND"
        + " ffc.cnt <= 11;"
    )
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 生保の次年度手数料をセレクト
def mz_seiho_fee_seiho_next(coltd_cd, syoken_cd_main):
    fee_seiho_next = 0
    sql = (
        "SELECT * FROM sql_order_store WHERE coltd_cd = "
        + "'"
        + coltd_cd
        + "'"
        + " AND syoken_cd_main = "
        + "'"
        + syoken_cd_main
        + "'"
        + " AND keiyaku_cd = '2'"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)
    for dt in sql_data:
        fee_seiho_next = dt["fee_seiho_next"]
    return fee_seiho_next


# 前月が月払い/初年度/既に支払が12回/契約データから次年度以降を出して算出する。5Lなどの場合で6年目は0円になる処理はされていない。
def mz_seiho_last_month_01_06_12equal(last_month):
    sql = (
        "SELECT fos.*, ffc.cnt FROM sql_fee_order_store as fos"
        + " LEFT JOIN sql_fee_future_cnt as ffc on fos.syoken_cd_main = ffc.syoken_cd_main"
        + " WHERE fos.nyu_date = "
        + str(last_month)
        + " AND"
        + " fos.cat_cd = '1'"
        + " AND"
        + " (fos.pay_num_cd = '01' OR fos.pay_num_cd = '06')"
        + " AND"
        + " fos.first_next_year = 1"
        + " AND"
        + " ffc.cnt = 12;"
    )
    sql_data = sql_config.mz_sql(sql)

    # 1年を過ぎた業務提携は考慮していない
    new_list = []
    error_list = []
    for dt in sql_data:
        # 次年度手数料
        fee_seiho_next = mz_seiho_fee_seiho_next(dt["coltd_cd"], dt["syoken_cd_main"])

        if fee_seiho_next == 0:
            error_list.append(dt["syoken_cd_main"])
        else:
            new_fee_num = round(fee_seiho_next / 12)
            new_pay_fee_yen = round((dt["pay_fee_per"] * new_fee_num) / 100)
            temp_dic = {
                "id": dt["id"],
                "nyu_nendo": dt["nyu_nendo"],
                "nyu_date": dt["nyu_date"],
                "kind_cd": dt["kind_cd"],
                "cat_cd": dt["cat_cd"],
                "coltd_cd": dt["coltd_cd"],
                "siki_date": dt["siki_date"],
                "manki_date": dt["manki_date"],
                "kind_cd_main": dt["kind_cd_main"],
                "kind_cd_sub": dt["kind_cd_sub"],
                "pay_num_cd": dt["pay_num_cd"],
                "hoken_kikan_cd": dt["hoken_kikan_cd"],
                "hoken_kikan_year": dt["hoken_kikan_year"],
                "syoken_cd_main": dt["syoken_cd_main"],
                "syoken_cd_sub": dt["syoken_cd_sub"],
                "hoken_ryo": dt["hoken_ryo"],
                "fee_num": new_fee_num,
                "section_cd": dt["section_cd"],
                "section_cd_email": dt["section_cd_email"],
                "pay_person_kind": dt["pay_person_kind"],
                "pay_person_cd": dt["pay_person_cd"],
                "pay_person_email": dt["pay_person_email"],
                "pay_fee_per": dt["pay_fee_per"],
                "pay_fee_yen": new_pay_fee_yen,
                "pay_gyotei_cd": dt["pay_gyotei_cd"],
                "kei_name": dt["kei_name"],
                "pay_gyotei_1year_over": dt["pay_gyotei_1year_over"],
                "kaime": dt["kaime"],
                "fee_memo": dt["fee_memo"],
                "first_next_year": dt["first_next_year"],
            }
            new_list.append(temp_dic)
    return new_list


# 年払い/初年度/1年前の年払いを出して、契約データから次年度以降を引き出し算出する。
def mz_seiho_last_year_15(last_year):
    sql = (
        "SELECT * FROM sql_fee_order_store"
        + " WHERE nyu_date = "
        + str(last_year)
        + " AND"
        + " cat_cd = '1'"
        + " AND"
        + " pay_num_cd = '00'"
        + ";"
    )
    sql_data = sql_config.mz_sql(sql)

    # 1年を過ぎた業務提携は考慮していない
    new_list = []
    error_list = []
    for dt in sql_data:
        # 次年度手数料
        fee_seiho_next = mz_seiho_fee_seiho_next(dt["coltd_cd"], dt["syoken_cd_main"])

        if fee_seiho_next == 0:
            error_list.append(dt["syoken_cd_main"])
        else:
            new_fee_num = fee_seiho_next
            new_pay_fee_yen = round((dt["pay_fee_per"] * new_fee_num) / 100)
            temp_dic = {
                "id": dt["id"],
                "nyu_nendo": dt["nyu_nendo"],
                "nyu_date": dt["nyu_date"],
                "kind_cd": dt["kind_cd"],
                "cat_cd": dt["cat_cd"],
                "coltd_cd": dt["coltd_cd"],
                "siki_date": dt["siki_date"],
                "manki_date": dt["manki_date"],
                "kind_cd_main": dt["kind_cd_main"],
                "kind_cd_sub": dt["kind_cd_sub"],
                "pay_num_cd": dt["pay_num_cd"],
                "hoken_kikan_cd": dt["hoken_kikan_cd"],
                "hoken_kikan_year": dt["hoken_kikan_year"],
                "syoken_cd_main": dt["syoken_cd_main"],
                "syoken_cd_sub": dt["syoken_cd_sub"],
                "hoken_ryo": dt["hoken_ryo"],
                "fee_num": new_fee_num,
                "section_cd": dt["section_cd"],
                "section_cd_email": dt["section_cd_email"],
                "pay_person_kind": dt["pay_person_kind"],
                "pay_person_cd": dt["pay_person_cd"],
                "pay_person_email": dt["pay_person_email"],
                "pay_fee_per": dt["pay_fee_per"],
                "pay_fee_yen": new_pay_fee_yen,
                "pay_gyotei_cd": dt["pay_gyotei_cd"],
                "kei_name": dt["kei_name"],
                "pay_gyotei_1year_over": dt["pay_gyotei_1year_over"],
                "kaime": dt["kaime"],
                "fee_memo": dt["fee_memo"],
                "first_next_year": dt["first_next_year"],
            }
            new_list.append(temp_dic)
    return sql_data


# ---------------------------------------------------------------------------------
# データ作成
# ---------------------------------------------------------------------------------
def mz_insert(sql_data):
    sql_con = sql_config.mz_sql_con()

    with sql_con:
        for dt in sql_data:
            sql = """
                INSERT INTO sql_fee_future (
                    nyu_nendo,
                    nyu_date,
                    kind_cd,
                    cat_cd,
                    coltd_cd,
                    siki_date,
                    manki_date,
                    kind_cd_main,
                    kind_cd_sub,
                    pay_num_cd,
                    hoken_kikan_cd,
                    hoken_kikan_year,
                    syoken_cd_main,
                    syoken_cd_sub,
                    hoken_ryo,
                    fee_num,
                    section_cd,
                    section_cd_email,
                    pay_person_kind,
                    pay_person_cd,
                    pay_person_email,
                    pay_fee_per,
                    pay_fee_yen,
                    pay_gyotei_cd,
                    kei_name,
                    pay_gyotei_1year_over,
                    kaime,
                    fee_memo
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
                    %s
                );
                """
            cur = sql_con.cursor()
            cur.execute(
                sql,
                (
                    dt["nyu_nendo"],
                    dt["nyu_date"],
                    dt["kind_cd"],
                    dt["cat_cd"],
                    dt["coltd_cd"],
                    dt["siki_date"],
                    dt["manki_date"],
                    dt["kind_cd_main"],
                    dt["kind_cd_sub"],
                    dt["pay_num_cd"],
                    dt["hoken_kikan_cd"],
                    dt["hoken_kikan_year"],
                    dt["syoken_cd_main"],
                    dt["syoken_cd_sub"],
                    dt["hoken_ryo"],
                    dt["fee_num"],
                    dt["section_cd"],
                    dt["section_cd_email"],
                    dt["pay_person_kind"],
                    dt["pay_person_cd"],
                    dt["pay_person_email"],
                    dt["pay_fee_per"],
                    dt["pay_fee_yen"],
                    dt["pay_gyotei_cd"],
                    dt["kei_name"],
                    dt["pay_gyotei_1year_over"],
                    dt["kaime"],
                    dt["fee_memo"],
                ),
            )
            sql_con.commit()

    return


# 入金日付を変更する
def mz_date_update(last_year, last_month, nyu_date_int):
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = (
            "UPDATE sql_fee_future SET"
            + " nyu_date = "
            + str(nyu_date_int)
            + ","
            + " nyu_nendo = 0"
            + " WHERE"
            + " nyu_date = "
            + str(last_year)
            + " OR"
            + " nyu_date = "
            + str(last_month)
            + ";"
        )
        cur = sql_con.cursor()
        cur.execute(sql)
        sql_con.commit()
    return


# 件数カウント
def mz_cnt(nyu_date_int):
    sql = "SELECT * FROM sql_fee_future" + " WHERE nyu_date = " + str(nyu_date_int) + ";"
    sql_data = sql_config.mz_sql(sql)
    sql_data_cnt = len(sql_data)
    return sql_data_cnt
