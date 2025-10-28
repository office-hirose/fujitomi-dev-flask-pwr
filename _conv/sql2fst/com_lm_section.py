import html
import logging
import sys
from firebase_admin import firestore

from _mod import sql_config
from . import utils


def com_lm_section():
    # すべてのドキュメントを削除
    utils.delete_all_documents("com_lm_section")

    sql_data = sql_config.mz_sql("SELECT * FROM com_lm_section;")
    db = firestore.client()
    for dt in sql_data:
        data = {
            "lm_section_cd": int(dt["lm_section_cd"]),
            "lm_section_name": html.escape(dt["lm_section_name"]),
        }
        db.collection("com_lm_section").add(data)
    logging.info("%s: SQL to FS - データ変換正常完了。処理件数: %s", sys._getframe().f_code.co_name, str(len(sql_data)))
    return
