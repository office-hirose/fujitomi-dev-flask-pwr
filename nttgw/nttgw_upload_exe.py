# ------------------------------------------------------------------------
#  nttgw_upload_exe.py
#  |--nttgw_upload_exe      - 画面作成
#  |--nttgw_upload_exe_exe  - 実行する
# ------------------------------------------------------------------------
import io
import sys
from flask import request
from _mod import fs_config, mod_base, mod_fnc, sql_config
from google.cloud import storage
import csv


def nttgw_upload_exe():
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


def nttgw_upload_exe_exe():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # init
    upload_result = ""
    old_file_name = ""
    new_file_name = ""

    error_list = []
    error_row = 0
    success_cnt = 0

    # get file data
    flask_file = request.files["file_data"]

    # init
    project_name = fs_dic["project_name"]
    bucket_name = fs_dic["upload_gcs_bucket"]
    user_email = "admin@fujitomi.jp"

    # file empty chk
    if flask_file is None:
        upload_result = "empty"
    else:
        # file name
        old_file_name = flask_file.filename
        fnc_values = mod_fnc.mz_fnc(old_file_name)
        new_file_name = fnc_values["file_name_full_new"]

        # file name unique check
        file_chk_res = mz_nttgw_upload_imp_file_name_chk(old_file_name)

        #  csv file only
        if flask_file.mimetype == "text/csv" and file_chk_res == "ok":
            # 1. 空白行を除外するために、ファイルをメモリ内の一時バッファに読み込む
            temp_buffer = io.StringIO()
            temp_buffer.write(flask_file.read().decode("utf-8"))
            temp_buffer.seek(0)

            # 2. 空白行を除外するために、空白行をスキップして新しい一時バッファに書き込む
            filtered_buffer = io.StringIO()
            for row in temp_buffer:
                if row.strip():  # 空白行ではない場合
                    filtered_buffer.write(row)
            filtered_buffer.seek(0)

            # 3. UTF-8でエンコードし、BytesIOオブジェクトに変換
            encoded_buffer = io.BytesIO()
            encoded_buffer.write(filtered_buffer.getvalue().encode("utf-8"))
            encoded_buffer.seek(0)

            # 4. 新しいバッファをGCSにアップロードする
            new_file_name_path = "files/" + new_file_name
            client = storage.Client(project_name)
            bucket = client.get_bucket(bucket_name)
            blob = bucket.blob(new_file_name_path)
            blob.upload_from_file(encoded_buffer, content_type="text/csv")

            # 5. load file from GCS
            str_data = storage.Blob(new_file_name_path, bucket)
            str_data = str_data.download_as_string()
            str_data = str_data.decode("utf-8")
            str_data = io.StringIO(str_data)
            str_data = csv.reader(str_data, delimiter="|")

            # import data
            for dt in str_data:
                try:
                    error_row += 1

                    con_exe_sta = "import"
                    con_imp_file_name = old_file_name
                    con_temp_text = dt[0]
                    con_create_email = user_email

                    sql_con = sql_config.mz_sql_con()
                    with sql_con:
                        sql = """
                        INSERT INTO sql_nttgw_dat (
                            exe_sta,
                            imp_file_name,
                            temp_text,
                            create_email
                        ) VALUES (
                            %s,
                            %s,
                            %s,
                            %s
                        );
                        """
                        cur = sql_con.cursor()
                        cur.execute(
                            sql,
                            (
                                con_exe_sta,
                                con_imp_file_name,
                                con_temp_text,
                                con_create_email,
                            ),
                        )
                        sql_con.commit()

                    success_cnt += 1
                except Exception as e:
                    error_list.append(str(error_row) + "行目エラー：" + f"{e}" + "：" + str(dt))

            upload_result = "ok"
        else:
            upload_result = "file_error"

        if file_chk_res == "error":
            upload_result = "already_import"

        # エラーなしの場合、sql_nttgw_imp_file_name_chkにファイル名を書き込む
        if len(error_list) == 0 and upload_result == "ok":
            mz_nttgw_upload_imp_file_name_insert(old_file_name, user_email)

    # dic
    dic = {
        "level_error": "",
        "upload_result": upload_result,
        "old_file_name": old_file_name,
        "new_file_name": new_file_name,
        "error_list": error_list,
        "error_row": error_row,
        "success_cnt": success_cnt,
    }
    return dic


def mz_nttgw_upload_imp_file_name_chk(old_file_name):
    # init
    file_chk_res = ""
    sql_data = []
    sql_data_cnt = 0

    sql = "SELECT * FROM sql_nttgw_imp_file_name_chk" + " WHERE imp_file_name = " + '"' + old_file_name + '"' + ";"
    sql_data = sql_config.mz_sql(sql)
    sql_data_cnt = len(sql_data)

    # check
    if sql_data_cnt == 0:
        file_chk_res = "ok"
    else:
        file_chk_res = "error"

    return file_chk_res


def mz_nttgw_upload_imp_file_name_insert(old_file_name, user_email):
    # init
    con_imp_file_name = old_file_name
    con_create_email = user_email

    sql_con = sql_config.mz_sql_con()
    with sql_con:
        sql = """
        INSERT INTO sql_nttgw_imp_file_name_chk (
            imp_file_name,
            create_email
        ) VALUES (
            %s,
            %s
        );
        """
        cur = sql_con.cursor()
        cur.execute(sql, (con_imp_file_name, con_create_email))
        sql_con.commit()

    return
