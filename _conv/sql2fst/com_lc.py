import html
import logging
import sys
from firebase_admin import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from _mod import sql_config
from . import utils


def com_lc():
    # すべてのドキュメントを削除
    utils.delete_all_documents("com_lc")

    sql_data = sql_config.mz_sql("SELECT * FROM com_lc;")
    db = firestore.client()
    for dt in sql_data:
        data = {
            "sort": int(dt["sort"]),
            "device_cd": int(dt["device_cd"]),
            "onoff_cd": int(dt["onoff_cd"]),
            "level_cd": int(dt["level_cd"]),
            "link_cat_cd": int(dt["link_cat_cd"]),
            "link_cat_url": html.escape(dt["link_cat_url"]),
            "link_cat_name": html.escape(dt["link_cat_name"]),
            "link_cat_detail": html.escape(dt["link_cat_detail"]),
            "material_icon": html.escape(dt["material_icon"]),
            "update_email": html.escape(dt["update_email"]),
            "update_time": SERVER_TIMESTAMP,
        }
        db.collection("com_lc").add(data)
    logging.info("%s: SQL to FS - データ変換正常完了。処理件数: %s", sys._getframe().f_code.co_name, str(len(sql_data)))
    return
