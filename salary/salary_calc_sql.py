from _mod import sql_config


# 取得
def mz_sql_salary_store(salary_date_int):
    """
    指定された年月の給与ストアデータを取得する
    """
    sql = "SELECT * FROM sql_salary_store WHERE salary_year_month = " + str(salary_date_int) + ";"
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# 取得
def mz_sql_fee_order_store(salary_date_int, staff_email):
    """
    指定された年月の担当者分の手数料の合計を取得する
    """
    sql = f"""
        SELECT
            SUM(pay_fee_yen) AS pay_fee_total
        FROM
            sql_fee_order_store
        WHERE
            nyu_date = {salary_date_int}
            AND pay_person_email = '{staff_email}'
            AND pay_person_kind IN ('main', 'sub')
        GROUP BY
            pay_person_email;
    """
    sql_data = sql_config.mz_sql(sql)

    if len(sql_data) == 0:
        pay_fee_total = 0
    else:
        for dt in sql_data:
            pay_fee_total = dt["pay_fee_total"]

    return pay_fee_total


# 更新処理
def mz_sql_salary_store_update(
    id,
    pay_fee_total,
    fee_hirei_no_tax,
    fee_hirei_tax,
    fee_hirei_tax_20,
    fee_total,
    fee_total_sagaku,
):

    # sql
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        try:
            sql = (
                "UPDATE sql_salary_store SET "
                + "fee_no_tax = %s, "
                + "fee_hirei_no_tax = %s, "
                + "fee_hirei_tax = %s, "
                + "fee_hirei_tax_20 = %s, "
                + "fee_total = %s, "
                + "fee_total_sagaku = %s "
                + "WHERE id = "
                + str(id)
                + ";"
            )
            cur = sql_con.cursor()
            cur.execute(
                sql,
                (
                    int(pay_fee_total),
                    int(fee_hirei_no_tax),
                    int(fee_hirei_tax),
                    int(fee_hirei_tax_20),
                    int(fee_total),
                    int(fee_total_sagaku),
                ),
            )
            sql_con.commit()
        except Exception as e:
            print(f"更新エラー: {e}")  # エラーログ出力
            raise  # 必要に応じて再投与
    return
