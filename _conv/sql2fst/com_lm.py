import html
import logging
import sys
from firebase_admin import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from _mod import sql_config
from . import utils


def com_lm():
    # すべてのドキュメントを削除
    utils.delete_all_documents("com_lm")

    sql_data = sql_config.mz_sql("SELECT * FROM com_lm;")
    db = firestore.client()
    for dt in sql_data:
        data = {
            "sort": int(dt["sort"]),
            "onoff_cd": int(dt["onoff_cd"]),
            "level_cd": int(dt["level_cd"]),
            "lm_section_cd": int(dt["lm_section_cd"]),
            "lm_email": html.escape(dt["lm_email"]),
            "lm_name": html.escape(dt["lm_name"]),
            "update_email": html.escape(dt["update_email"]),
            "update_time": SERVER_TIMESTAMP,
        }
        db.collection("com_lm").add(data)
    logging.info("%s: SQL to FS - データ変換正常完了。処理件数: %s", sys._getframe().f_code.co_name, str(len(sql_data)))
    return
