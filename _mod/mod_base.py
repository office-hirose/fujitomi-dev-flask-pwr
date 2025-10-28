import jwt
from flask import request
from _mod import fs_config, mod_lm, mod_que, mod_datetime
from user_agents import parse


def mz_base(acc_level, jwtg, acc_page_name):
    # firestore
    fs_dic = fs_config.fs_dic()

    if fs_dic is None:
        # This indicates a server configuration error. Returning default/error values.
        return {
            "level_error": "error",
            "last_update_time": mod_datetime.mz_tnow("for_datetime"),
            "login_level_cd": 0,  # Or appropriate default/error value
            "login_level_name": "Error",  # Or appropriate default/error value
            "google_account_email": "Error",  # Or appropriate default/error value
        }

    # jwt decode
    jwt_key = fs_dic["jwt_key"]
    jwt_dic = jwt.decode(jwtg, jwt_key, algorithms=["HS256"])
    google_account_email = jwt_dic["google_account_email"]

    # user_mail
    if google_account_email is None or google_account_email == "":
        google_account_email = "Guest"

    # login_level_cd, login_level_name
    login_level_cd, login_level_name = mod_lm.lm_cd_name(google_account_email)

    # level error
    if acc_level > login_level_cd:
        level_error = "error"
    else:
        level_error = ""

    # last update time str
    last_update_time = mod_datetime.mz_tnow("for_datetime")

    # user agent
    ua_string = request.headers.get("User-Agent")
    user_agent = parse(ua_string)
    str_user_agent = str(user_agent)

    # user ip
    ip_tmp = request.headers.getlist("X-Forwarded-For")[0]
    ip_tmp_list = ip_tmp.split(",")
    user_ip = ip_tmp_list[0]

    # task
    que_project = fs_dic["project_name"]
    que_location = fs_dic["que_location"]
    que_id = fs_dic["que_id"]
    que_url = fs_dic["que_site"] + "/setting/al_task"
    que_body = {
        "acc_page_name": acc_page_name,
        "user_agent": str_user_agent,
        "user_ip": user_ip,
        "create_email": google_account_email,
    }
    mod_que.mz_que(que_project, que_location, que_id, que_url, que_body)

    base_data = {
        "level_error": level_error,
        "last_update_time": last_update_time,
        "login_level_cd": login_level_cd,
        "login_level_name": login_level_name,
        "google_account_email": google_account_email,
    }
    return base_data
