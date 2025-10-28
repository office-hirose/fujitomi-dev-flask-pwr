import sys
from flask import request
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
from _mod import (
    fs_config,
    mod_base,
    mod_datetime,
    mod_lm,
    mod_lb,
    mod_lc,
)


def google_signin():
    # firestore
    fs_dic = fs_config.fs_dic()

    if fs_dic is None:
        # Consider logging the error here for debugging purposes
        return {"error": "サーバー設定の読み込みに失敗しました。"}

    # リクエストのJSONデータを安全に取得
    request_data = request.get_json()
    if not request_data:
        return {"error": "JSONデータが見つかりません"}

    front_key = request_data.get("front_key")
    credential = request_data.get("credential")

    if not front_key or not credential:
        return {"error": "必須パラメータが不足しています"}

    google_signin_client_id = fs_dic.get("google_signin_client_id")
    if not google_signin_client_id:
        return {"error": "Google sign-in client IDが設定されていません"}

    # init error
    dic = {
        "jwtg": "error",
    }

    # sv key check
    if fs_dic.get("sv_key") == front_key:

        # get idinfo
        idinfo = id_token.verify_oauth2_token(credential, requests.Request(), google_signin_client_id)

        # login_level_cd, login_level_name, last_update_time
        login_level_cd, login_level_name = mod_lm.lm_cd_name(idinfo["email"])
        last_update_time = mod_datetime.mz_tnow("for_datetime")

        # now year month
        # now_date_int = mod_datetime.mz_now_date_num()
        # now_year_int = mod_datetime.mz_num2yy(now_date_int)
        # now_month_int = mod_datetime.mz_num2mm(now_date_int)
        # year_month_int = int(str(now_year_int) + str(now_month_int).zfill(2))

        # chk
        if login_level_cd >= 2:

            # jwt encode
            jwt_key = fs_dic.get("jwt_key")
            if not jwt_key:
                return {"error": "JWTキーが設定されていません"}

            payload = {
                "google_account_email": idinfo["email"],
            }
            jwtg = jwt.encode(payload, jwt_key, algorithm="HS256")

            # success
            dic = {
                "jwtg": jwtg,
                "google_account_name": idinfo["name"],
                "google_account_email": idinfo["email"],
                "google_account_pic": idinfo["picture"],
                "last_update_time": last_update_time,
                "login_level_cd": login_level_cd,
                "login_level_name": login_level_name,
                "lb_data": mod_lb.flt_level(login_level_cd),
                "lc_data": mod_lc.flt_level(login_level_cd),
            }
    return dic


def google_signout():
    # session remove
    # session.pop("google_account_email", None)

    # pause xx seconds
    # time.sleep(1.0)

    # dic
    dic = {}
    return dic


def update_local_storage():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    login_level_cd = base_data["login_level_cd"]
    last_update_time = base_data["last_update_time"]

    # now year month
    # now_date_int = mod_datetime.mz_now_date_num()
    # now_year_int = mod_datetime.mz_num2yy(now_date_int)
    # now_month_int = mod_datetime.mz_num2mm(now_date_int)
    # year_month_int = int(str(now_year_int) + str(now_month_int).zfill(2))

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "last_update_time": last_update_time,
            "lb_data": [],
            "lc_data": [],
        }
    else:
        dic = {
            "level_error": level_error,
            "last_update_time": last_update_time,
            "lb_data": mod_lb.flt_level(login_level_cd),
            "lc_data": mod_lc.flt_level(login_level_cd),
        }
    return dic
