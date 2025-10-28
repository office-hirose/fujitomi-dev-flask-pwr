from _mod import sql_config


# manki list sql
def manki_list_sql(cat_cd, manki_date, section_cd, staff_cd, manki_chk_cd):

    # manki date, start, end
    manki_date_s = manki_date * 100
    manki_date_e = manki_date_s + 32

    # select_from
    select_from = "SELECT * FROM sql_order_store"

    # where1
    where1 = " WHERE cat_cd = " + '"' + cat_cd + '"'

    # where2
    where2 = " AND manki_date > " + str(manki_date_s) + " AND manki_date < " + str(manki_date_e)

    # where3 セクション
    where3 = " AND section_cd = " + '"' + section_cd + '"'

    # where4 担当者1
    if staff_cd == "0":
        where4 = ""
    else:
        where4 = " AND staff1_cd = " + '"' + staff_cd + '"'

    # where5
    if manki_chk_cd == 0:
        where5 = ""
    else:
        where5 = " AND manki_chk_cd = " + str(manki_chk_cd)

    # order1
    order1 = " ORDER BY coltd_cd, syoken_cd_main, syoken_cd_sub, keijyo_date;"

    # execute
    sql1 = select_from + where1 + where2 + where3 + where4 + where5 + order1

    sql_data1 = sql_config.mz_sql(sql1)
    sql_data = list(sql_data1)

    # sql_data2 = sql_config.mz_sql(sql2)
    # sql_data = list(sql_data1) + list(sql_data2)

    return sql_data


# load comment sql
def load_comment_sql(coltd_cd, syoken_cd_main, syoken_cd_sub):

    # syoken_cd_mainの最初の3文字を取得
    syoken_cd_main_3moji = syoken_cd_main[:3]
    if coltd_cd == "17" and syoken_cd_main_3moji == "980":
        pass
    else:
        syoken_cd_sub = "0000"

    # sql_manki_comment
    select_from1 = "SELECT * FROM sql_manki_comment"
    where1 = (
        " WHERE coltd_cd = "
        + '"'
        + coltd_cd
        + '"'
        + " AND syoken_cd_main = "
        + '"'
        + syoken_cd_main
        + '"'
        + " AND syoken_cd_sub = "
        + '"'
        + syoken_cd_sub
        + '"'
    )
    sql1 = select_from1 + where1
    sql_data1 = sql_config.mz_sql(sql1)

    return sql_data1


# add comment sql
def add_comment_sql(coltd_cd, syoken_cd_main, syoken_cd_sub, manki_chk_cd, manki_comment, update_email):

    # 前後の空白文字(全角スペースを含む)を削除し、空の場合は「コメントなし」にする
    manki_comment = manki_comment.strip()
    if manki_comment == "":
        manki_comment = "コメントなし"

    # syoken_cd_mainの最初の3文字を取得
    syoken_cd_main_3moji = syoken_cd_main[:3]
    if coltd_cd == "17" and syoken_cd_main_3moji == "980":
        # update sql_order_store 980の場合
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = """
            UPDATE sql_order_store
            SET manki_chk_cd = %s
            WHERE coltd_cd = %s AND syoken_cd_main = %s AND syoken_cd_sub = %s;
            """
            cur = sql_con.cursor()
            cur.execute(
                sql,
                (manki_chk_cd, coltd_cd, syoken_cd_main, syoken_cd_sub),
            )
            sql_con.commit()

    else:
        # update sql_order_store 980以外の場合
        syoken_cd_sub = "0000"
        sql_con = sql_config.mz_sql_con()
        with sql_con:
            sql = """
            UPDATE sql_order_store
            SET manki_chk_cd = %s
            WHERE coltd_cd = %s AND syoken_cd_main = %s;
            """
            cur = sql_con.cursor()
            cur.execute(
                sql,
                (manki_chk_cd, coltd_cd, syoken_cd_main),
            )
            sql_con.commit()

    # add sql_manki_comment
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = """
        INSERT INTO sql_manki_comment (
                coltd_cd,
                syoken_cd_main,
                syoken_cd_sub,
                manki_chk_cd,
                manki_comment,
                update_email
        ) VALUES (
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
            (coltd_cd, syoken_cd_main, syoken_cd_sub, manki_chk_cd, manki_comment, update_email),
        )
        sql_con.commit()

    # select sql_manki_comment
    select_from1 = "SELECT * FROM sql_manki_comment"
    where1 = (
        " WHERE coltd_cd = "
        + '"'
        + coltd_cd
        + '"'
        + " AND syoken_cd_main = "
        + '"'
        + syoken_cd_main
        + '"'
        + " AND syoken_cd_sub = "
        + '"'
        + syoken_cd_sub
        + '"'
    )
    order1 = " ORDER BY coltd_cd, syoken_cd_main, id;"
    sql1 = select_from1 + where1 + order1
    sql_data1 = sql_config.mz_sql(sql1)

    return sql_data1
