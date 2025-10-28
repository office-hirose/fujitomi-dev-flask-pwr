# ------------------------------------------------------------------------
#  |-- create_file_start - 画面作成
#  |-- upload_zip_exe
#  |-- count_file_exe
#  |-- move_file_exe
#  |-- create_file_exe
#  |-- backup_delete_exe
# ------------------------------------------------------------------------
import sys
import json
from flask import request
from _mod import fs_config, mod_base, mod_que

from nttgw.nttgw_create_file_upload_zip import main_upload_zip
from nttgw.nttgw_create_file_count_file import main_count_file
from nttgw.nttgw_create_file_backup_delete import main_backup_delete
from nttgw.nttgw_create_file_empty_trash import main_empty_trash
import mimetypes
from werkzeug.utils import secure_filename


# start
def create_file_start():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    dic = {
        "level_error": level_error,
    }
    return dic


# upload zip
def upload_zip_exe():
    # jwtg
    jwtg = request.form.get("jwtg")
    if jwtg:
        try:
            jwtg = json.loads(jwtg)
        except json.JSONDecodeError as e:
            print(f"Error in json.loads(jwtg): {e}")
            jwtg = None
    else:
        jwtg = None

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "upload_zip_result": "",
        }
    else:
        # zip file
        zip_file = request.files.get("file_data")
        if zip_file and zip_file.filename:
            filename = secure_filename(zip_file.filename)
            mimetype, dmy = mimetypes.guess_type(filename)

            if mimetype != "application/zip":
                upload_zip_result = "エラー！ ZIPファイルが見つかりませんでした"
            else:
                upload_zip_result = main_upload_zip(zip_file)
        else:
            upload_zip_result = "エラー！ ファイルが選択されていません"

        dic = {
            "level_error": level_error,
            "upload_zip_result": upload_zip_result,
        }
    return dic


# counf file
def count_file_exe():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "count_file_result": "",
        }
    else:
        # exe
        count_file_result, trash_url = main_count_file()

        dic = {
            "level_error": level_error,
            "count_file_result": count_file_result,
            "trash_url": trash_url,
        }
    return dic


# move file
def move_file_exe():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    user_email = base_data["google_account_email"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "move_file_result_send_email": "",
        }
    else:
        # task que
        que_project = fs_dic["project_name"]
        que_location = fs_dic["que_location"]
        que_id = fs_dic["que_id"]
        que_site = fs_dic["que_site"]
        que_url = que_site + "/nttgw/move_file_task"
        que_body = {
            "js_obj": json.loads(request.data.decode("utf-8")),
            "project_name": fs_dic["project_name"],
            "sender_email": fs_dic["sender_email"],
            "service": fs_dic["project_name"],
            "user_email": user_email,
        }
        mod_que.mz_que(que_project, que_location, que_id, que_url, que_body)

        dic = {
            "level_error": level_error,
            "move_file_result_send_email": user_email,
        }
    return dic


# create csv
def create_file_exe():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    user_email = base_data["google_account_email"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "create_file_result_send_email": "",
        }
    else:
        # task que
        que_project = fs_dic["project_name"]
        que_location = fs_dic["que_location"]
        que_id = fs_dic["que_id"]
        que_site = fs_dic["que_site"]
        que_url = que_site + "/nttgw/create_file_task"
        que_body = {
            "js_obj": json.loads(request.data.decode("utf-8")),
            "project_name": fs_dic["project_name"],
            "sender_email": fs_dic["sender_email"],
            "service": fs_dic["project_name"],
            "user_email": user_email,
        }
        mod_que.mz_que(que_project, que_location, que_id, que_url, que_body)

        dic = {
            "level_error": level_error,
            "create_file_result_send_email": user_email,
        }
    return dic


# backup_delete
def backup_delete_exe():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "backup_delete_result": "",
        }
    else:
        # exe
        backup_delete_result = main_backup_delete()

        dic = {
            "level_error": level_error,
            "backup_delete_result": backup_delete_result,
        }
    return dic


# empty_trash
def empty_trash_exe():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    if level_error == "error":
        dic = {
            "level_error": level_error,
            "empty_trash_result": "",
        }
    else:
        # exe
        empty_trash_result = main_empty_trash()

        dic = {
            "level_error": level_error,
            "empty_trash_result": empty_trash_result,
        }
    return dic
