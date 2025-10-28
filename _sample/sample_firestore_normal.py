import sys
from flask import request
from _mod import mod_base
from firebase_admin import firestore


def sample_firestore_normal():
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
        # データベースから取得 ageでソート
        db = firestore.client()
        ref = db.collection("sample_users")
        query = ref.order_by("age")
        docs = query.get()

        fs_data = []
        if docs:
            for doc in docs:
                d = doc.to_dict()
                if d is not None:
                    d["id"] = doc.id
                    fs_data.append(d)

        dic = {
            "level_error": level_error,
            "fs_data": fs_data,
        }
    return dic
