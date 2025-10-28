import sys
from flask import request
from _mod import mod_base, mod_firestore


def sample_get_collection():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # firestore
    fs_collection_data = mod_firestore.get_all_collections_fields()

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "fs_collection_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "fs_collection_data": fs_collection_data,
        }
    return dic
