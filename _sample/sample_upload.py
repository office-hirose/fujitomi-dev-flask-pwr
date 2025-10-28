from flask import request
from _mod import fs_config, mod_fnc
from google.cloud import storage


def sample_file_upload_csv():
    # firestore
    fs_dic = fs_config.fs_dic()

    upload_result = ""
    new_file_name = ""
    old_file_name = ""

    if fs_dic is None:
        file = request.files.get("file_data")
        return {
            "upload_result": "config_error",
            "old_file_name": file.filename if file else "N/A",
            "new_file_name": "N/A",
        }

    upload_result = ""
    new_file_name = ""

    # file data
    file_data = request.files["file_data"]

    # file empty chk
    if file_data is None:
        upload_result = "empty"
    else:
        # file name
        old_file_name = file_data.filename
        fnc_values = mod_fnc.mz_fnc(old_file_name)
        new_file_name = fnc_values["file_name_full_new"]

        # set flag
        file_name_ext_flag = "csv" in fnc_values["file_name_ext"]

        #  csv file only(True = 1)
        if file_name_ext_flag == 1:
            # GCS
            project_name = fs_dic["project_name"]
            bucket_name = fs_dic["upload_gcs_bucket"]

            client = storage.Client(project_name)
            bucket = client.get_bucket(bucket_name)
            blob = bucket.blob(new_file_name)
            blob.upload_from_file(file_data)

            upload_result = "ok"
        else:
            upload_result = "file_type_error"

    # dic
    dic = {
        "upload_result": upload_result,
        "old_file_name": old_file_name,
        "new_file_name": new_file_name,
    }
    return dic


def sample_file_upload_all():
    # firestore
    fs_dic = fs_config.fs_dic()

    if fs_dic is None:
        file = request.files.get("file_data")
        return {
            "upload_result": "config_error",
            "old_file_name": file.filename if file else "N/A",
            "new_file_name": "N/A",
        }

    upload_result = ""
    new_file_name = ""

    # file data
    file_data = request.files["file_data"]

    # file empty chk
    if file_data is None:
        upload_result = "empty"
    else:
        # file name
        old_file_name = file_data.filename
        fnc_values = mod_fnc.mz_fnc(old_file_name)
        new_file_name = fnc_values["file_name_full_new"]

        # GCS
        project_name = fs_dic["project_name"]
        bucket_name = fs_dic["upload_gcs_bucket"]

        client = storage.Client(project_name)
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(new_file_name)
        blob.upload_from_file(file_data)

        upload_result = "ok"

    # dic
    dic = {
        "upload_result": upload_result,
        "old_file_name": old_file_name,
        "new_file_name": new_file_name,
    }
    return dic
