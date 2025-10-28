# ------------------------------------------------------------------------
#  nttgw_upload_chk.py
#  |--nttgw_upload_chk      - 画面作成
#  |--nttgw_upload_chk_exe  - 実行する
# ------------------------------------------------------------------------
import io
import sys
from flask import request
from _mod import fs_config, mod_base, mod_fnc
from google.cloud import storage
import csv


def nttgw_upload_chk():
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


def nttgw_upload_chk_exe():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # init
    upload_result = ""
    old_file_name = ""
    new_file_name = ""

    error_list = []
    error_row = 0
    success_cnt = 0
    chk_temp_text = ""

    # get file data
    flask_file = request.files["file_data"]

    # init
    project_name = fs_dic["project_name"]
    bucket_name = fs_dic["upload_gcs_bucket"]

    # file empty chk
    if flask_file is None:
        upload_result = "empty"
    else:
        # file name
        old_file_name = flask_file.filename
        fnc_values = mod_fnc.mz_fnc(old_file_name)
        new_file_name = fnc_values["file_name_full_new"]

        #  csv file only
        if flask_file.mimetype == "text/csv":
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

            # check data
            for dt in str_data:
                try:
                    error_row += 1
                    chk_temp_text = dt[0]
                    success_cnt += 1
                except Exception as e:
                    error_list.append(str(error_row) + "行目エラー：" + f"{e}" + "：" + str(dt))

            upload_result = "ok"
        else:
            upload_result = "file_error"

    # dic
    dic = {
        "level_error": "",
        "upload_result": upload_result,
        "old_file_name": old_file_name,
        "new_file_name": new_file_name,
        "error_list": error_list,
        "success_cnt": success_cnt,
        # 下記は使用しない
        "chk_temp_text": chk_temp_text,
    }
    return dic
