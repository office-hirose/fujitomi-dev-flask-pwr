import sys
from flask import request
from _mod import mod_base, mod_onoff, mod_lm_level, mod_lc
from firebase_admin import firestore


# firestore あいまい検索
def sample_firestore_like():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    search_word = obj["search_word"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "onoff_data": [],
            "level_data": [],
            "lc_data": [],
            "fs_data": [],
        }
    else:
        print(search_word)
        print(search_word + "\uf8ff")

        db = firestore.client()
        query = (
            db.collection("com_lb")
            .order_by("search_con")
            .where("search_con", ">=", search_word)
            .where("search_con", "<=", search_word + "\uf8ff")
        )
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
            "onoff_data": mod_onoff.fs_onoff_data(),
            "level_data": mod_lm_level.fs_lm_level_data(),
            "lc_data": mod_lc.fs_lc_data(),
            "fs_data": fs_data,
        }

    return dic
