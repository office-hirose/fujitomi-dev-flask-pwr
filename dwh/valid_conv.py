# ------------------------------------------------------------------------
#  valid_conv.py
#  |--valid_conv      - 画面作成
#  |--valid_conv_exe  - タスクを渡す
#  |--valid_conv_task - タスク処理、メール送信
#  |--valid_conv_task_exe - update
# ------------------------------------------------------------------------
import sys
import json
import base64
from email.mime.text import MIMEText
from flask import request
from _mod import fs_config, mod_base, mod_que, mod_datetime, sql_config, mod_gmail_api
from _mod_fis import mod_order_store_log


def valid_conv():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    user_email = base_data["google_account_email"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "user_email": "",
        }
    else:
        dic = {
            "level_error": level_error,
            "user_email": user_email,
        }
    return dic


def valid_conv_exe():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    to_email = base_data["google_account_email"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
        }
    else:
        # task que
        que_project = fs_dic["project_name"]
        que_location = fs_dic["que_location"]
        que_id = fs_dic["que_id"]
        que_url = fs_dic["que_site"] + "/dwh/valid_conv_task"
        que_body = {
            "jwtg": jwtg,
            "from_email": fs_dic["sender_email"],
            "to_email": to_email,
            "service": fs_dic["project_name"],
        }
        mod_que.mz_que(que_project, que_location, que_id, que_url, que_body)

        dic = {
            "level_error": level_error,
        }
    return dic


def valid_conv_task():
    # obj
    que_body = json.loads(request.data.decode("utf-8"))
    jwtg = que_body["jwtg"]
    from_email = que_body["from_email"]
    to_email = que_body["to_email"]
    service = que_body["service"]
    start_time = mod_datetime.mz_tnow("for_datetime")

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        pass
    else:
        # sql
        exe_data_cnt = valid_conv_task_exe(jwtg)

        # sendgrid subject/body
        end_time = mod_datetime.mz_tnow("for_datetime")
        subject_data = "有効無効修正処理-" + mod_datetime.mz_tnow("for_filename_yyyy_mmdd_hhmm")
        body_data = ""
        body_data += "\n"
        body_data += "処理　　：" + subject_data + "\n"
        body_data += "件数　　：" + str(exe_data_cnt) + "\n"
        body_data += "\n"
        body_data += "処理開始時刻：" + start_time + "\n"
        body_data += "処理終了時刻：" + end_time + "\n"
        body_data += "service : " + service + "\n"
        body_data += "\n"

        # Gmail APIでメール送信
        service_gmail = mod_gmail_api.get_gmail_service()
        if service_gmail is not None:
            # メールメッセージを作成
            message_obj = MIMEText(body_data, "plain", "utf-8")
            message_obj["to"] = to_email
            message_obj["from"] = from_email
            message_obj["subject"] = subject_data

            # Base64エンコード
            raw_message = base64.urlsafe_b64encode(message_obj.as_bytes()).decode("utf-8")

            # メール送信
            try:
                result = service_gmail.users().messages().send(userId="me", body={"raw": raw_message}).execute()
                print(f"valid_conv メール送信成功: {result}")
            except Exception as e:
                print(f"valid_conv メール送信エラー: {e}")
                import traceback

                print(f"valid_conv 詳細エラー: {traceback.format_exc()}")

        # base - level 9 - access log only
        acc_page_name = sys._getframe().f_code.co_name
        mod_base.mz_base(9, jwtg, acc_page_name)

    dic = {}
    return dic


def valid_conv_task_exe(jwtg):
    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    cnt = 0

    if level_error == "error":
        pass
    else:
        sql = """
            SELECT * FROM sql_order_store
            WHERE create_date <= 20221231 AND
            (
            keiyaku_cd = '1' OR
            keiyaku_cd = '4' OR
            keiyaku_cd = '6' OR
            keiyaku_cd = '8' OR
            keiyaku_cd = '9' OR
            keiyaku_cd = '9999'
            )
            ORDER BY fis_cd;
        """
        sql_data = sql_config.mz_sql(sql)

        for dt in sql_data:
            fis_cd = dt["fis_cd"]
            syoken_cd_main = dt["syoken_cd_main"]
            syoken_cd_sub = dt["syoken_cd_sub"]

            sql = (
                "UPDATE sql_order_store"
                + " SET valid_cd = 'invalid'"
                + " WHERE"
                + " syoken_cd_main = "
                + "'"
                + syoken_cd_main
                + "'"
                + " AND"
                + " syoken_cd_sub = "
                + "'"
                + syoken_cd_sub
                + "'"
                + " AND"
                + " valid_cd != 'invalid'"
                + ";"
            )
            con = sql_config.mz_sql_con()
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            con.close()

            cnt += 1

            # order_store_log
            mod_order_store_log.mz_insert_log(sys._getframe().f_code.co_name, fis_cd)

    # base - level 9 - access log only
    acc_page_name = sys._getframe().f_code.co_name
    mod_base.mz_base(9, jwtg, acc_page_name)

    return cnt
