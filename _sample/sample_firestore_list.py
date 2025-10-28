import sys
from flask import request
from _mod import mod_base
from google.cloud import firestore


def sample_firestore_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "fs_data": [],
        }
    else:

        # Firestore サービスの初期化
        db = firestore.Client()

        # コレクションリファレンスの取得
        collections = db.collections()

        # 空のリストを初期化
        fs_data = []

        # コレクションリファレンスのリストをループ処理
        for collection in collections:
            # 各コレクションのIDを使用して辞書を作成し、リストに追加
            fs_data.append({"name": collection.id})

        dic = {
            "level_error": level_error,
            "fs_data": fs_data,
        }
    return dic
