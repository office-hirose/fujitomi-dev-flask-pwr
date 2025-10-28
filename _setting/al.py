import sys

# import datetime
from flask import request
from _mod import mod_base, mod_lm, mod_lm_section, mod_datetime
from firebase_admin import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP, Query


# start
def al():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    calendar_s = str(obj["calendar_s"])
    calendar_e = str(obj["calendar_e"])
    lm_email = obj["lm_email"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # start日付, end日付
    # datetime_now = datetime.datetime.now()
    # datetime_s = datetime_now - datetime.timedelta(hours=9, days=30)
    # datetime_e = datetime_now + datetime.timedelta(hours=9, days=0)
    # calendar_s = mod_datetime.mz_dt2str_yymmdd_slash(datetime_s)
    # calendar_e = mod_datetime.mz_dt2str_yymmdd_slash(datetime_e)

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "lm_section_data": [],
            "lm_data": [],
            "al_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "lm_section_data": mod_lm_section.fs_lm_section_data(),
            "lm_data": mod_lm.fs_lm_data(),
            "al_data": fs_al_data(calendar_s, calendar_e, lm_email),
        }
    return dic


def al_list():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    calendar_s = str(obj["calendar_s"])
    calendar_e = str(obj["calendar_e"])
    lm_email = obj["lm_email"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "al_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "al_data": fs_al_data(calendar_s, calendar_e, lm_email),
        }
    return dic


def fs_al_data(calendar_s, calendar_e, lm_email):
    # calendar_s, calendar_e, lm_email
    calendar_s_conv = mod_datetime.mz_str2dt_slash(calendar_s + " 00:00:00")
    calendar_e_conv = mod_datetime.mz_str2dt_slash(calendar_e + " 23:59:59")

    try:
        db = firestore.client()

        if lm_email == "all" or lm_email is None:
            # 全ユーザーの場合：日付範囲のみでクエリ
            query = (
                db.collection("com_al")
                .where("create_time", ">=", calendar_s_conv)
                .where("create_time", "<=", calendar_e_conv)
                .order_by("create_time", direction=Query.DESCENDING)
                .limit(300)
            )
        else:
            # 特定ユーザーの場合：日付範囲とメールアドレスでクエリ
            query = (
                db.collection("com_al")
                .where("create_time", ">=", calendar_s_conv)
                .where("create_time", "<=", calendar_e_conv)
                .where("create_email", "==", lm_email)
                .order_by("create_time", direction=Query.DESCENDING)
                .limit(300)
            )

        docs = query.get()

        fs_data = []
        if docs:
            for doc in docs:
                if doc is not None:
                    d = doc.to_dict()
                    if d is not None:
                        d["id"] = doc.id
                        fs_data.append(d)

        return fs_data

    except Exception as e:
        print(f"Firestore query error: {e}")
        # エラーが発生した場合は、より単純なクエリを試行
        try:
            db = firestore.client()
            # 日付範囲のみでクエリ（メールアドレスフィルタなし）
            query = (
                db.collection("com_al")
                .where("create_time", ">=", calendar_s_conv)
                .where("create_time", "<=", calendar_e_conv)
                .order_by("create_time", direction=Query.DESCENDING)
                .limit(300)
            )

            docs = query.get()

            fs_data = []
            if docs:
                for doc in docs:
                    if doc is not None:
                        d = doc.to_dict()
                        if d is not None:
                            d["id"] = doc.id
                            # クライアント側でメールアドレスフィルタリング
                            if lm_email == "all" or lm_email is None or d.get("create_email") == lm_email:
                                fs_data.append(d)

            return fs_data

        except Exception as e2:
            print(f"Fallback query error: {e2}")
            return []


def al_del():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    key_dict = obj["key_array"]
    calendar_s = obj["calendar_s"]
    calendar_e = obj["calendar_e"]
    lm_email = obj["lm_email"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "al_data": [],
        }
    else:
        # sql
        al_del_exe(key_dict)

        dic = {
            "level_error": level_error,
            "al_data": fs_al_data(calendar_s, calendar_e, lm_email),
        }
    return dic


def al_del_exe(key_dict):
    for id in key_dict:
        db = firestore.client()
        db.collection("com_al").document(id).delete()
    return


def al_task():
    # json
    obj = request.get_json()

    data = {
        "acc_page_name": obj["acc_page_name"],
        "user_agent": obj["user_agent"],
        "user_ip": obj["user_ip"],
        "create_email": obj["create_email"],
        "create_time": SERVER_TIMESTAMP,
    }

    # insert
    db = firestore.client()
    db.collection("com_al").add(data)

    dic = {}
    return dic
