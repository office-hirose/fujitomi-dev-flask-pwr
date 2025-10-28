import logging
from firebase_admin import firestore
from _mod import sql_config
from .utils import truncate_table
import sys


def com_config():
    sql_con = None
    try:
        table_name = "com_config"
        truncate_table(table_name)

        sql = """
        INSERT INTO com_config (
            mysql_unix_socket,
            mysql_database,
            mysql_user,
            mysql_password,
            google_signin_client_id,
            sv_key,
            sendgrid_api_key,
            jwt_key,
            upload_gcs_bucket,
            sender_email,
            project_name,
            que_location,
            que_site,
            que_id,
            oauth_key_gcs_bucket,
            upload_folder_id,
            dat_folder_id,
            fee_folder_id,
            processed_folder_id,
            result_folder_id,
            backup_folder_id,
            trash_url,
            google_drive_oauth_key_json
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
            %s
        );
        """
        db = firestore.client()
        firestore_data = db.collection("com_config").get()
        sql_con = sql_config.mz_sql_con()

        with sql_con.cursor() as cur:
            data_list = []
            for doc in firestore_data:
                dt = doc.to_dict()
                if dt is None:
                    logging.warning("ドキュメントデータがNoneです。ドキュメントIDをスキップします: %s", str(doc.id))
                    continue
                try:
                    data = (
                        dt.get("mysql_unix_socket", ""),
                        dt.get("mysql_database", ""),
                        dt.get("mysql_user", ""),
                        dt.get("mysql_password", ""),
                        dt.get("google_signin_client_id", ""),
                        dt.get("sv_key", ""),
                        dt.get("sendgrid_api_key", ""),
                        dt.get("jwt_key", ""),
                        dt.get("upload_gcs_bucket", ""),
                        dt.get("sender_email", ""),
                        dt.get("project_name", ""),
                        dt.get("que_location", ""),
                        dt.get("que_site", ""),
                        dt.get("que_id", ""),
                        dt.get("oauth_key_gcs_bucket", ""),
                        dt.get("upload_folder_id", ""),
                        dt.get("dat_folder_id", ""),
                        dt.get("fee_folder_id", ""),
                        dt.get("processed_folder_id", ""),
                        dt.get("result_folder_id", ""),
                        dt.get("backup_folder_id", ""),
                        dt.get("trash_url", ""),
                        dt.get("google_drive_oauth_key_json", ""),
                    )
                    data_list.append(data)
                except Exception as e:
                    logging.error("%s: データ変換エラー: %s - %s", sys._getframe().f_code.co_name, str(dt), str(e))
            cur.executemany(sql, data_list)
        sql_con.commit()
        logging.info(
            "%s: FS to SQL - データ変換正常完了。処理件数: %s", sys._getframe().f_code.co_name, str(len(data_list))
        )
    except Exception as e:
        logging.error("%s: エラー発生: %s", sys._getframe().f_code.co_name, str(e))
        if sql_con:
            sql_con.rollback()
    finally:
        if sql_con:
            sql_con.close()
    return
