from flask import request


def mz_ua(google_account_email):
    # user_mail
    if google_account_email is None or google_account_email == "":
        google_account_email = "Guest"

    # os, browser, ip
    user_os = str(request.user_agent.platform)
    user_browser = str(request.user_agent.browser) + ":" + str(request.user_agent.version)
    ip_tmp = request.headers.getlist("X-Forwarded-For")[0]
    ip_tmp_list = ip_tmp.split(",")
    user_ip = ip_tmp_list[0]

    ua = {
        "user_os": user_os,
        "user_browser": user_browser,
        "user_ip": user_ip,
        "create_email": google_account_email,
    }

    return ua
