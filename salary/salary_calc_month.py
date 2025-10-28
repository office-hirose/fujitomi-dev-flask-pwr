from salary import salary_calc_sql

# from decimal import Decimal


# calc
def mz_update(salary_date_int):

    # データの読み込み
    sql_data = salary_calc_sql.mz_sql_salary_store(salary_date_int)

    if len(sql_data) != 0:
        for dt in sql_data:
            # id
            id = dt["id"]

            # 担当email
            staff_email = dt["staff_email"]

            # 取得済みのデータから手数料を取得（データがない場合は0）
            pay_fee_total = salary_calc_sql.mz_sql_fee_order_store(salary_date_int, staff_email)

            # fee_kotei 固定月額
            fee_kotei = dt["fee_kotei"]

            # fee_pay_ritu 支払率
            # fee_pay_ritu = dt["fee_pay_ritu"] * Decimal("0.01")

            # fee_hirei_no_tax  成績比例分税抜
            fee_hirei_no_tax = int((pay_fee_total * dt["fee_pay_ritu"]) / 100)

            # fee_hirei_tax_ritu 成績比例分税率
            # fee_hirei_tax_ritu = dt["fee_hirei_tax_ritu"] * Decimal("0.01")

            # fee_hirei_tax 成績比例分消費税
            fee_hirei_tax = int((fee_hirei_no_tax * dt["fee_hirei_tax_ritu"]) / 100)

            # fee_hirei_tax_20 成績比例分消費税20%
            fee_hirei_tax_20 = int((fee_hirei_tax * 20) / 100)

            # fee_total 合計額
            fee_total = int(fee_kotei + fee_hirei_no_tax + fee_hirei_tax_20)

            # fee_total_sagaku手数料との差額
            fee_total_sagaku = pay_fee_total - fee_total

            # 更新処理
            salary_calc_sql.mz_sql_salary_store_update(
                id,
                pay_fee_total,
                fee_hirei_no_tax,
                fee_hirei_tax,
                fee_hirei_tax_20,
                fee_total,
                fee_total_sagaku,
            )
    return
