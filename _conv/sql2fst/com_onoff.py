import html
import logging
import sys
from firebase_admin import firestore

from _mod import sql_config
from . import utils


def com_onoff():
    # すべてのドキュメントを削除
    utils.delete_all_documents("com_onoff")

    sql_data = sql_config.mz_sql("SELECT * FROM com_onoff;")
    db = firestore.client()
    for dt in sql_data:
        data = {
            "onoff_cd": int(dt["onoff_cd"]),
            "onoff_name": html.escape(dt["onoff_name"]),
            "onoff_name_admin": html.escape(dt["onoff_name_admin"]),
            "open_close_name": html.escape(dt["open_close_name"]),
            "link_type_name": html.escape(dt["link_type_name"]),
            "style_color": html.escape(dt["style_color"]),
        }
        db.collection("com_onoff").add(data)
    logging.info("%s: SQL to FS - データ変換正常完了。処理件数: %s", sys._getframe().f_code.co_name, str(len(sql_data)))
    return
