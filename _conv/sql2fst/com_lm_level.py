import html
import logging
import sys
from firebase_admin import firestore

from _mod import sql_config
from . import utils


def com_lm_level():
    # すべてのドキュメントを削除
    utils.delete_all_documents("com_lm_level")

    sql_data = sql_config.mz_sql("SELECT * FROM com_lm_level;")
    db = firestore.client()
    for dt in sql_data:
        data = {
            "level_cd": int(dt["level_cd"]),
            "level_name_en1char": html.escape(dt["level_name_en1char"]),
            "level_name": html.escape(dt["level_name"]),
            "style_color": html.escape(dt["style_color"]),
        }
        db.collection("com_lm_level").add(data)
    logging.info("%s: SQL to FS - データ変換正常完了。処理件数: %s", sys._getframe().f_code.co_name, str(len(sql_data)))
    return
