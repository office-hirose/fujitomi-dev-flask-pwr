import html
import logging
import sys
from firebase_admin import firestore

from _mod import sql_config
from . import utils


def com_style():
    # すべてのドキュメントを削除
    utils.delete_all_documents("com_style")

    sql_data = sql_config.mz_sql("SELECT * FROM com_style;")
    db = firestore.client()
    for dt in sql_data:
        data = {
            "sort": int(dt["sort"]),
            "onoff_cd": int(dt["onoff_cd"]),
            "cat": html.escape(dt["cat"]),
            "style_name": html.escape(dt["style_name"]),
            "style_data": html.escape(dt["style_data"]),
        }
        db.collection("com_style").add(data)
    logging.info("%s: SQL to FS - データ変換正常完了。処理件数: %s", sys._getframe().f_code.co_name, str(len(sql_data)))
    return
