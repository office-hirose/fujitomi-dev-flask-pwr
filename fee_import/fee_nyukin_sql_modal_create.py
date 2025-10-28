from _mod import sql_config


# 入金金額のフィールド作成
def mz_create(nyu_date, coltd_cd):

    # SQL
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = """
        INSERT INTO sql_fee_nyukin (
            sort,
            nyu_date,
            cat_cd,
            coltd_cd,
            section_cd,
            nyukin_cd,
            kazei_hikazei
        ) VALUES (
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

        # 取得したデータを使ってSQLインサートを行う
        select = f"""
            SELECT *
            FROM
                sql_fee_nyukin_basic
            WHERE
                coltd_cd = '{coltd_cd}'
            ORDER BY
                sort;
        """
        nk_data_basic = sql_config.mz_sql(select)

        i = 0
        for dt in nk_data_basic:
            i += 1
            cur.execute(
                sql,
                (
                    i,
                    int(nyu_date),
                    dt["cat_cd"],
                    dt["coltd_cd"],
                    dt["section_cd"],
                    int(dt["nyukin_cd"]),
                    int(dt["kazei_hikazei"]),
                ),
            )

        sql_con.commit()

    return
