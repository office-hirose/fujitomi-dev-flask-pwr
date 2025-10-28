import sys
import io
from flask import request
from _mod import fs_config, mod_base, mod_fnc, sql_config
from google.cloud import storage
import csv


def google_upload():
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


def google_upload_exe():
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
    flask_file = request.files.get("file_data")  # dictionaryを使う

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
            # sql truncate
            sql = "TRUNCATE com_google_account;"
            sql_con = sql_config.mz_sql_con()
            cur = sql_con.cursor()
            cur.execute(sql)
            sql_con.commit()

            # save file to GCS
            new_file_name_path = "files/" + new_file_name
            client = storage.Client(project_name)
            bucket = client.get_bucket(bucket_name)
            blob = bucket.blob(new_file_name_path)
            blob.upload_from_file(flask_file)

            # load file from GCS
            str_data = storage.Blob(new_file_name_path, bucket)
            str_data = str_data.download_as_string()
            str_data = str_data.decode("utf-8")
            str_data = io.StringIO(str_data)
            str_data = csv.reader(str_data)

            # import data
            next(str_data)  # 1件目のタイトルをパス
            for row_index, dt in enumerate(str_data, start=2):  # エラー行特定のため
                try:
                    error_row += 1

                    first_name = str(dt[0])
                    last_name = str(dt[1])
                    email_address = str(dt[2])
                    password = str(dt[3])
                    password_hash_function = str(dt[4])
                    org_unit_path = str(dt[5])
                    new_primary_email = str(dt[6])
                    status = str(dt[7])
                    last_sign_in = str(dt[8])
                    recovery_email = str(dt[9])
                    home_secondary_email = str(dt[10])
                    work_secondary_email = str(dt[11])
                    recovery_phone = str(dt[12])
                    work_phone = str(dt[13])
                    home_phone = str(dt[14])
                    mobile_phone = str(dt[15])
                    work_address = str(dt[16])
                    home_address = str(dt[17])
                    employee_id = str(dt[18])
                    employee_type = str(dt[19])
                    employee_title = str(dt[20])
                    manager_email = str(dt[21])
                    department = str(dt[22])
                    cost_center = str(dt[23])
                    two_sv_enrolled = str(dt[24])
                    two_sv_enforced = str(dt[25])
                    building_id = str(dt[26])
                    floor_name = str(dt[27])
                    floor_section = str(dt[28])
                    email_usage = str(dt[29])
                    drive_usage = str(dt[30])
                    photos_usage = str(dt[31])
                    storage_limit = str(dt[32])
                    storage_used = str(dt[33])
                    change_password_at_next_signin = str(dt[34])
                    new_status = str(dt[35])
                    # licenses = str(dt[36])
                    # new_licenses = str(dt[37])
                    # advanced_protection_program_enrollment = str(dt[38])

                    sql_con = sql_config.mz_sql_con()
                    with sql_con:
                        sql = """
                        INSERT INTO com_google_account (
                            first_name,
                            last_name,
                            email_address,
                            password,
                            password_hash_function,
                            org_unit_path,
                            new_primary_email,
                            status,
                            last_sign_in,
                            recovery_email,
                            home_secondary_email,
                            work_secondary_email,
                            recovery_phone,
                            work_phone,
                            home_phone,
                            mobile_phone,
                            work_address,
                            home_address,
                            employee_id,
                            employee_type,
                            employee_title,
                            manager_email,
                            department,
                            cost_center,
                            two_sv_enrolled,
                            two_sv_enforced,
                            building_id,
                            floor_name,
                            floor_section,
                            email_usage,
                            drive_usage,
                            photos_usage,
                            storage_limit,
                            storage_used,
                            change_password_at_next_signin,
                            new_status
                        ) VALUES (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
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
                                first_name,
                                last_name,
                                email_address,
                                password,
                                password_hash_function,
                                org_unit_path,
                                new_primary_email,
                                status,
                                last_sign_in,
                                recovery_email,
                                home_secondary_email,
                                work_secondary_email,
                                recovery_phone,
                                work_phone,
                                home_phone,
                                mobile_phone,
                                work_address,
                                home_address,
                                employee_id,
                                employee_type,
                                employee_title,
                                manager_email,
                                department,
                                cost_center,
                                two_sv_enrolled,
                                two_sv_enforced,
                                building_id,
                                floor_name,
                                floor_section,
                                email_usage,
                                drive_usage,
                                photos_usage,
                                storage_limit,
                                storage_used,
                                change_password_at_next_signin,
                                new_status,
                            ),
                        )
                        sql_con.commit()

                    success_cnt += 1
                except IndexError as e:
                    # CSVファイルの列数が足りない場合の処理
                    error_list.append(f"{row_index}行目: 列数が足りません。 - {e}")
                except ValueError as e:
                    # データの型変換エラー時の処理
                    error_list.append(f"{row_index}行目: データの型が不正です。 - {e}")
                except Exception as e:
                    # その他の例外発生時の処理
                    error_list.append(f"{row_index}行目: エラーが発生しました。 - {e}")

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
        "error_row": error_row,
        "success_cnt": success_cnt,
    }
    return dic
