import logging
import sys
from firebase_admin import firestore

from _mod import sql_config


def com_config():
    # すべてのドキュメントを削除、configは念の為削除しない、追加される
    # delete_all_documents("com_config")

    sql_data = sql_config.mz_sql("SELECT * FROM com_config;")
    db = firestore.client()
    for dt in sql_data:
        data = {
            "mysql_unix_socket": dt["mysql_unix_socket"],
            "mysql_database": dt["mysql_database"],
            "mysql_user": dt["mysql_user"],
            "mysql_password": dt["mysql_password"],
            "google_signin_client_id": dt["google_signin_client_id"],
            "sv_key": dt["sv_key"],
            "sendgrid_api_key": dt["sendgrid_api_key"],
            "jwt_key": dt["jwt_key"],
            "upload_gcs_bucket": dt["upload_gcs_bucket"],
            "sender_email": dt["sender_email"],
            "project_name": dt["project_name"],
            "que_location": dt["que_location"],
            "que_site": dt["que_site"],
            "que_id": dt["que_id"],
            # fisプロジェクトのみ
            "oauth_key_gcs_bucket": dt["oauth_key_gcs_bucket"],
            "upload_folder_id": dt["upload_folder_id"],
            "dat_folder_id": dt["dat_folder_id"],
            "fee_folder_id": dt["fee_folder_id"],
            "processed_folder_id": dt["processed_folder_id"],
            "result_folder_id": dt["result_folder_id"],
            "backup_folder_id": dt["backup_folder_id"],
            "trash_url": dt["trash_url"],
            "google_drive_oauth_key_json": dt["google_drive_oauth_key_json"],
        }
        db.collection("com_config").add(data)
    logging.info("%s: SQL to FS - データ変換正常完了。処理件数: %s", sys._getframe().f_code.co_name, str(len(sql_data)))
    return
