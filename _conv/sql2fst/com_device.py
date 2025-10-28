import logging
import sys
from firebase_admin import firestore

from _mod import sql_config
from . import utils


def com_device():
    # すべてのドキュメントを削除
    utils.delete_all_documents("com_device")

    sql_data = sql_config.mz_sql("SELECT * FROM com_device;")
    db = firestore.client()
    for dt in sql_data:
        data = {
            "sort": dt["sort"],
            "device_cd": dt["device_cd"],
            "device_name": dt["device_name"],
        }
        db.collection("com_device").add(data)
    logging.info("%s: SQL to FS - データ変換正常完了。処理件数: %s", sys._getframe().f_code.co_name, str(len(sql_data)))
    return
