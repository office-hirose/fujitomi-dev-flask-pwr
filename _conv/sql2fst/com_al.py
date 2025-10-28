import html
import logging
import sys
from firebase_admin import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from _mod import sql_config
from . import utils


def com_al():
    # すべてのドキュメントを削除
    utils.delete_all_documents("com_al")

    sql_data = sql_config.mz_sql("SELECT * FROM com_al;")
    db = firestore.client()
    for dt in sql_data:
        data = {
            "acc_page_name": html.escape(dt["acc_page_name"]),
            "user_agent": html.escape(dt["user_agent"]),
            "user_ip": html.escape(dt["user_ip"]),
            "create_email": html.escape(dt["create_email"]),
            "create_time": SERVER_TIMESTAMP,
        }
        db.collection("com_al").add(data)
    logging.info("%s: SQL to FS - データ変換正常完了。処理件数: %s", sys._getframe().f_code.co_name, str(len(sql_data)))
    return
