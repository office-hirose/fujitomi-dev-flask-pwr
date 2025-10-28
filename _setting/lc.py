import sys
import html
from flask import request
from _mod import (
    mod_base,
    mod_lm_level,
    mod_device,
    mod_onoff,
    mod_lc,
    mod_lb,
)
from firebase_admin import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP


# start
def lc():
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
            "device_data": [],
            "onoff_data": [],
            "level_data": [],
            "lc_data": [],
            "lb_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "device_data": mod_device.fs_device_data(),
            "onoff_data": mod_onoff.fs_onoff_data(),
            "level_data": mod_lm_level.fs_lm_level_data(),
            "lc_data": mod_lc.fs_lc_data(),
            "lb_data": mod_lb.fs_lb_data(),
        }
    return dic


def lc_modal_exe():
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
            "lc_data": [],
        }
    else:
        # sql
        lc_modal_exe_fs(dic_exe, google_account_email, jwtg)

        dic = {
            "level_error": level_error,
            "lc_data": mod_lc.fs_lc_data(),
        }
    return dic


# firestore
def lc_modal_exe_fs(dic_exe, google_account_email, jwtg):
    data = {
        "sort": int(dic_exe["sort"]),
        "device_cd": int(dic_exe["device_cd"]),
        "onoff_cd": int(dic_exe["onoff_cd"]),
        "level_cd": int(dic_exe["level_cd"]),
        "link_cat_cd": int(dic_exe["link_cat_cd"]),
        "link_cat_url": html.escape(dic_exe["link_cat_url"]),
        "link_cat_name": html.escape(dic_exe["link_cat_name"]),
        "link_cat_detail": html.escape(dic_exe["link_cat_detail"]),
        "material_icon": html.escape(dic_exe["material_icon"]),
        "q_bg_color": html.escape(dic_exe["q_bg_color"]),
        "q_border_color": html.escape(dic_exe["q_border_color"]),
        "q_text_color": html.escape(dic_exe["q_text_color"]),
        "update_email": google_account_email,
        "update_time": SERVER_TIMESTAMP,
    }

    # edit
    if dic_exe["exe_sta"] == "edit":
        db = firestore.client()
        ref = db.collection("com_lc").document(dic_exe["id"])
        ref.set(data, merge=True)

    # add
    if dic_exe["exe_sta"] == "add":
        db = firestore.client()
        db.collection("com_lc").add(data)

    # del
    if dic_exe["exe_sta"] == "del":
        db = firestore.client()
        db.collection("com_lc").document(dic_exe["id"]).delete()

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name + "_" + dic_exe["exe_sta"]
    mod_base.mz_base(9, jwtg, acc_page_name)

    return
