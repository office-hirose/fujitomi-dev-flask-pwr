from _mod import sql_config


# sql_fee_kakutei, sql_fee_store
def mz_list(nyu_date_int):
    sql = f"""
        SELECT
            id,
            nyu_date,
            cat_cd,
            coltd_cd,
            coltd_name,
            fk_notax,
            fs_notax,
            bal_notax,
            fk_notax - fs_notax - bal_notax AS sai_notax,
            fk_keiri_notax,
            fk_keiri_withtax,
            cnt
        FROM
        (
        SELECT
            fk.id,
            fk.nyu_date,
            fk.cat_cd,
            fk.coltd_cd,
            coltd.name_simple AS coltd_name,
            fk.fee_notax_total AS fk_notax,

            fk.fee_notax AS fk_keiri_notax,
            fk.fee_withtax_total AS fk_keiri_withtax,

            CASE
                WHEN fs_fee.sum_fee_notax IS NULL THEN 0
                ELSE CAST(fs_fee.sum_fee_notax AS DECIMAL)
            END AS fs_notax,

            bal.sum_fee_notax AS bal_notax,

            CASE
                WHEN cnt.cnt IS NULL THEN 0
                ELSE cnt.cnt
            END AS cnt

        FROM
            sql_fee_kakutei AS fk

        LEFT JOIN
            sql_coltd AS coltd ON fk.coltd_cd = coltd.coltd_cd

        LEFT JOIN
            (
            SELECT
                min(coltd_cd) AS coltd_cd,
                SUM(fee_notax) AS sum_fee_notax
            FROM
                sql_fee_store
            WHERE
                nyu_date = {nyu_date_int} AND
                syoken_cd_main != 'balance'
            GROUP BY
                sql_fee_store.coltd_cd
            ) AS fs_fee
        ON fk.coltd_cd = fs_fee.coltd_cd

        LEFT JOIN
            (
            SELECT
                min(coltd_cd) AS coltd_cd,
                SUM(fee_notax) AS sum_fee_notax
            FROM
                sql_fee_store
            WHERE
                nyu_date = {nyu_date_int}
                AND syoken_cd_main = 'balance'
            GROUP BY
                sql_fee_store.coltd_cd
            ) AS bal
        ON fk.coltd_cd = bal.coltd_cd

        LEFT JOIN
            (
            SELECT
                min(coltd_cd) AS coltd_cd,
                COUNT(*) AS cnt
            FROM
                sql_fee_store
            WHERE
                nyu_date = {nyu_date_int}
                AND syoken_cd_main != 'balance'
            GROUP BY
                sql_fee_store.coltd_cd
            ) AS cnt
        ON fk.coltd_cd = cnt.coltd_cd

        WHERE
            fk.nyu_date = {nyu_date_int}
        ORDER BY
            fk.cat_cd, fk.coltd_cd
        ) AS main;
    """
    sql_data = sql_config.mz_sql(sql)
    return sql_data


# リストの下に表示する金額合計、比較用Excel出力用
# def mz_total(nyu_date_int):
#     # fk_total
#     fk_total = 0
#     sql = f"""
#         SELECT
#             CASE
#                 WHEN sum(fee_notax_total) IS NULL THEN 0
#                 ELSE sum(fee_notax_total)
#             END AS fk_total
#         FROM
#             sql_fee_kakutei
#         WHERE
#             nyu_date = {nyu_date_int};
#     """
#     sql_data = sql_config.mz_sql(sql)
#     for dt in sql_data:
#         fk_total = int(dt["fk_total"])

#     # fs_total
#     fs_total = 0
#     sql = f"""
#         SELECT
#             CASE
#                 WHEN sum(fee_notax) IS NULL THEN 0
#                 ELSE sum(fee_notax)
#             END AS fs_total
#         FROM
#             sql_fee_store
#         WHERE
#             nyu_date = {nyu_date_int} AND
#             syoken_cd_main != 'balance';
#     """
#     sql_data = sql_config.mz_sql(sql)
#     for dt in sql_data:
#         fs_total = int(dt["fs_total"])

#     # bal_total
#     bal_total = 0
#     sql = f"""
#         SELECT
#             CASE
#                 WHEN sum(fee_notax) IS NULL THEN 0
#                 ELSE sum(fee_notax)
#             END AS bal_total
#         FROM
#             sql_fee_store
#         WHERE
#             nyu_date = {nyu_date_int} AND
#             syoken_cd_main = 'balance';
#     """
#     sql_data = sql_config.mz_sql(sql)
#     for dt in sql_data:
#         bal_total = int(dt["bal_total"])

#     # sai_total
#     sai_total = fk_total - fs_total - bal_total

#     # fk_total_keiri_notax
#     fk_total_keiri_notax = 0
#     sql = f"""
#         SELECT
#             CASE
#                 WHEN sum(fee_notax) IS NULL THEN 0
#                 ELSE sum(fee_notax)
#             END AS fk_total_keiri_notax
#         FROM
#             sql_fee_kakutei
#         WHERE
#             nyu_date = {nyu_date_int};
#     """
#     sql_data = sql_config.mz_sql(sql)
#     for dt in sql_data:
#         fk_total_keiri_notax = int(dt["fk_total_keiri_notax"])

#     # fk_total_keiri_withtax
#     fk_total_keiri_withtax = 0
#     sql = f"""
#         SELECT
#             CASE
#                 WHEN sum(fee_withtax_total) IS NULL THEN 0
#                 ELSE sum(fee_withtax_total)
#             END AS fk_total_keiri_withtax
#         FROM
#             sql_fee_kakutei
#         WHERE
#             nyu_date = {nyu_date_int};
#     """
#     sql_data = sql_config.mz_sql(sql)
#     for dt in sql_data:
#         fk_total_keiri_withtax = int(dt["fk_total_keiri_withtax"])

#     return (
#         fk_total,
#         fs_total,
#         bal_total,
#         sai_total,
#         fk_total_keiri_notax,
#         fk_total_keiri_withtax,
#     )
