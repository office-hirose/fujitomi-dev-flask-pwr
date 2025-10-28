import html
import logging
import sys
from firebase_admin import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from _mod import sql_config
from . import utils


def com_lb():
    # すべてのドキュメントを削除
    utils.delete_all_documents("com_lb")

    sql_data = sql_config.mz_sql("SELECT * FROM com_lb;")
    db = firestore.client()
    for dt in sql_data:
        data = {
            "sort": int(dt["sort"]),
            "device_cd": int(dt["device_cd"]),
            "onoff_cd": int(dt["onoff_cd"]),
            "level_cd": int(dt["level_cd"]),
            "link_cat_cd": int(dt["link_cat_cd"]),
            "link_type_cd": int(dt["link_type_cd"]),
            "link_url": html.escape(dt["link_url"]),
            "head_title": html.escape(dt["head_title"]),
            "title": html.escape(dt["title"]),
            "detail": html.escape(dt["detail"]),
            "style_border": html.escape(dt["style_border"]),
            "material_icon": html.escape(dt["material_icon"]),
            "search_con": html.escape(dt["search_con"]),
            "update_email": html.escape(dt["update_email"]),
            "update_time": SERVER_TIMESTAMP,
        }
        db.collection("com_lb").add(data)
    logging.info("%s: SQL to FS - データ変換正常完了。処理件数: %s", sys._getframe().f_code.co_name, str(len(sql_data)))
    return
