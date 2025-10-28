import sys
from flask import request
from _mod import mod_base
from manki import chk_sql


# モーダル用チェックコメントデータ読み込み
def load_comment():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    coltd_cd = obj["coltd_cd"]
    syoken_cd_main = obj["syoken_cd_main"]
    syoken_cd_sub = obj["syoken_cd_sub"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "modal_comment_data": [],
        }
    else:
        # sql
        modal_comment_data = chk_sql.load_comment_sql(coltd_cd, syoken_cd_main, syoken_cd_sub)
        dic = {
            "level_error": level_error,
            "modal_comment_data": modal_comment_data,
        }
    return dic


# モーダル用チェックコメントデータ追加
def add_comment():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    coltd_cd = obj["coltd_cd"]
    syoken_cd_main = obj["syoken_cd_main"]
    syoken_cd_sub = obj["syoken_cd_sub"]
    manki_chk_cd = obj["manki_chk_cd"]
    manki_comment = obj["manki_comment"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    google_account_email = base_data["google_account_email"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "modal_comment_data": [],
        }
    else:
        # sql
        modal_comment_data = chk_sql.add_comment_sql(
            coltd_cd, syoken_cd_main, syoken_cd_sub, manki_chk_cd, manki_comment, google_account_email
        )
        dic = {
            "level_error": level_error,
            "modal_comment_data": modal_comment_data,
        }
    return dic
