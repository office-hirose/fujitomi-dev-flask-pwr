import logging
import sys
from firebase_admin import firestore
from _mod import sql_config
from .utils import truncate_table


def com_style():
    sql_con = None
    try:
        table_name = "com_style"
        truncate_table(table_name)

        sql = """
        INSERT INTO com_style (
            sort,
            onoff_cd,
            cat,
            style_name,
            style_data
        ) VALUES (
            %s,
            %s,
            %s,
            %s,
            %s
        );
        """
        db = firestore.client()
        firestore_data = db.collection("com_style").get()
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
                        int(dt.get("sort", 0)),
                        int(dt.get("onoff_cd", 0)),
                        dt.get("cat", ""),
                        dt.get("style_name", ""),
                        dt.get("style_data", ""),
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
