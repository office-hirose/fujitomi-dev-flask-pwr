import sys
import html
from flask import request
from _mod import mod_base, mod_onoff, mod_lm_level, mod_lm, mod_lm_section
from firebase_admin import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP


# start
def lm():
    # json
    obj = request.get_json()
    jwtg = obj.get("jwtg", None)

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "onoff_data": [],
            "level_data": [],
            "section_data": [],
            "lm_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "onoff_data": mod_onoff.fs_onoff_data(),
            "level_data": mod_lm_level.fs_lm_level_data(),
            "section_data": mod_lm_section.fs_lm_section_data(),
            "lm_data": mod_lm.fs_lm_data(),
        }
    return dic


def lm_modal_exe():
    # json
    obj = request.get_json()
    jwtg = obj.get("jwtg", None)
    dic_exe = obj.get("dic_exe", None)

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    google_account_email = base_data["google_account_email"]

    # chk, sql write
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "lm_data": [],
        }
    else:
        # sql
        mz_lm_modal_exe_fs(dic_exe, google_account_email, jwtg)

        dic = {
            "level_error": level_error,
            "lm_data": mod_lm.fs_lm_data(),
        }
    return dic


# firestore
def mz_lm_modal_exe_fs(dic_exe, google_account_email, jwtg):
    data = {
        "sort": int(dic_exe["sort"]),
        "onoff_cd": int(dic_exe["onoff_cd"]),
        "level_cd": int(dic_exe["level_cd"]),
        "lm_section_cd": int(dic_exe["lm_section_cd"]),
        "lm_email": html.escape(dic_exe["lm_email"]),
        "lm_name": html.escape(dic_exe["lm_name"]),
        "update_email": google_account_email,
        "update_time": SERVER_TIMESTAMP,
    }

    # edit
    if dic_exe["exe_sta"] == "edit":
        db = firestore.client()
        ref = db.collection("com_lm").document(dic_exe["id"])
        ref.set(data, merge=True)

    # add
    if dic_exe["exe_sta"] == "add":
        db = firestore.client()
        db.collection("com_lm").add(data)

    # del
    if dic_exe["exe_sta"] == "del":
        db = firestore.client()
        db.collection("com_lm").document(dic_exe["id"]).delete()

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name + "_" + dic_exe["exe_sta"]
    mod_base.mz_base(9, jwtg, acc_page_name)

    return
