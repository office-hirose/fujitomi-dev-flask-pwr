import logging
import sys
from firebase_admin import firestore
from _mod import sql_config
from .utils import truncate_table


def com_device():
    sql_con = None
    try:
        table_name = "com_device"
        truncate_table(table_name)

        sql = """
        INSERT INTO com_device (
            sort,
            device_cd,
            device_name
        ) VALUES (
            %s,
            %s,
            %s
        );
        """
        db = firestore.client()
        firestore_data = db.collection("com_device").get()
        sql_con = sql_config.mz_sql_con()

        with sql_con.cursor() as cur:
            data_list = []
            for doc in firestore_data:
                dt = doc.to_dict()
                if dt is None:
                    logging.warning("ドキュメントデータがNoneです。ドキュメントIDをスキップします: %s", str(doc.id))
                    continue
                try:
                    data = (
                        dt.get("sort", ""),
                        dt.get("device_cd", ""),
                        dt.get("device_name", ""),
                    )
                    data_list.append(data)
                except Exception as e:
                    logging.error("%s: データ変換エラー: %s - %s", sys._getframe().f_code.co_name, str(dt), str(e))
            cur.executemany(sql, data_list)
        sql_con.commit()
        logging.info(
            "%s: FS to SQL - データ変換正常完了。処理件数: %s", sys._getframe().f_code.co_name, str(len(data_list))
        )
    except Exception as e:
        logging.error("%s: エラー発生: %s", sys._getframe().f_code.co_name, str(e))
        if sql_con:
            sql_con.rollback()
    finally:
        if sql_con:
            sql_con.close()
    return
