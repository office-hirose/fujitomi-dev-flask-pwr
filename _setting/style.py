import sys
import html
from flask import request
from _mod import mod_base, mod_onoff, mod_style
from firebase_admin import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP


# start
def style():
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
            "onoff_data": [],
            "style_data_list": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "onoff_data": mod_onoff.fs_onoff_data(),
            "style_data_list": mod_style.fs_style_data(),
        }
    return dic


def style_modal_exe():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    dic_exe = obj["dic_exe"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    google_account_email = base_data["google_account_email"]

    # chk, sql write
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "style_data_list": [],
        }
    else:
        # firestore
        mz_style_modal_exe_fs(dic_exe, google_account_email, jwtg)

        dic = {
            "level_error": level_error,
            "style_data_list": mod_style.fs_style_data(),
        }
    return dic


# firestore
def mz_style_modal_exe_fs(dic_exe, google_account_email, jwtg):
    data = {
        "sort": int(dic_exe["sort"]),
        "onoff_cd": int(dic_exe["onoff_cd"]),
        "cat": html.escape(dic_exe["cat"]),
        "style_name": html.escape(dic_exe["style_name"]),
        "style_data": html.escape(dic_exe["style_data"]),
        "update_email": google_account_email,
        "update_time": SERVER_TIMESTAMP,
    }

    # edit
    if dic_exe["exe_sta"] == "edit":
        db = firestore.client()
        ref = db.collection("com_style").document(dic_exe["id"])
        ref.set(data, merge=True)

    # add
    if dic_exe["exe_sta"] == "add":
        db = firestore.client()
        db.collection("com_style").add(data)

    # del
    if dic_exe["exe_sta"] == "del":
        db = firestore.client()
        db.collection("com_style").document(dic_exe["id"]).delete()

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name + "_" + dic_exe["exe_sta"]
    mod_base.mz_base(9, jwtg, acc_page_name)

    return
