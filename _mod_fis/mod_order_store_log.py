import json
from decimal import Decimal
from _mod import sql_config
from _mod_fis import mod_common


def mz_insert_log(insert_mode, fis_cd):
    dic_log = {}
    # temp = []
    sql = "SELECT * FROM sql_order_store WHERE fis_cd = " + str(fis_cd) + ";"
    sql_data = sql_config.mz_sql(sql)

    # 日付,Decimalはjson変換でエラーが出るため
    for key, value in sql_data[0].items():
        if key == "fee_staff1":
            dic_log[key] = str(Decimal(value))
        elif key == "fee_staff2":
            dic_log[key] = str(Decimal(value))
        elif key == "fee_staff3":
            dic_log[key] = str(Decimal(value))
        elif key == "fee_gyotei1":
            dic_log[key] = str(Decimal(value))
        elif key == "fee_gyotei2":
            dic_log[key] = str(Decimal(value))
        elif key == "fee_gyotei3":
            dic_log[key] = str(Decimal(value))

        elif key == "create_time":
            dic_log[key] = mod_common.mz_datetime_view(value)
        elif key == "update_time":
            dic_log[key] = mod_common.mz_datetime_view(value)
        elif key == "regi_time":
            dic_log[key] = mod_common.mz_datetime_view(value)

        # elif key == "memo_json":
        #     print(type(value))
        #     dic_log[key] = temp.append({})

        else:
            dic_log[key] = value

    # debug
    # temp = []
    # temp.append({"user_email": "admin@fujitomi.jp", "create_time": "2022-10-10 00:00:00", "text": "あいうえお"})
    # temp.append({"user_email": "hirose.t@fujitomi.jp", "create_time": "2022-10-10 00:00:00", "text": "かきくけこ"})
    # dic_log["memo_json"] = temp

    # json
    store_json = json.dumps(dic_log)

    # insert
    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = """
        INSERT INTO sql_order_store_log (
            insert_mode,
            fis_cd,
            store_json
        ) VALUES (
            %s,
            %s,
            %s
        );
        """
        cur = sql_con.cursor()
        cur.execute(
            sql,
            (
                insert_mode,
                fis_cd,
                store_json,
            ),
        )
        sql_con.commit()

    return
