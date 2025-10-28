import logging
import sys
from firebase_admin import firestore
from _mod import sql_config
from .utils import truncate_table


def com_lb():
    sql_con = None
    try:
        table_name = "com_lb"
        truncate_table(table_name)

        sql = """
        INSERT INTO com_lb (
            sort,
            device_cd,
            onoff_cd,
            level_cd,
            link_cat_cd,
            link_type_cd,
            link_url,
            head_title,
            title,
            detail,
            style_border,
            material_icon,
            search_con,
            update_email
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
            %s
        );
        """
        db = firestore.client()
        firestore_data = db.collection("com_lb").get()
        sql_con = sql_config.mz_sql_con()

        # URLの最大長さを設定（SQLのカラム定義に合わせる）
        # 実際のlink_urlカラムの長さに合わせて調整してください
        max_url_length = 255

        with sql_con.cursor() as cur:
            data_list = []
            error_records = []
            for doc in firestore_data:
                dt = doc.to_dict()
                if dt is None:
                    logging.warning("ドキュメントデータがNoneです。ドキュメントIDをスキップします: %s", str(doc.id))
                    continue
                try:
                    # リンクURLの長さをチェックして切り捨て
                    link_url = dt.get("link_url", "")
                    if len(link_url) > max_url_length:
                        logging.warning(
                            "URLが長すぎるため切り捨てます: %s... (元の長さ: %s)", link_url[:50], str(len(link_url))
                        )
                        # 長すぎるURLを記録
                        error_records.append({"doc_id": doc.id, "original_url": link_url})
                        link_url = link_url[:max_url_length]

                    data = (
                        int(dt.get("sort", 0)),
                        int(dt.get("device_cd", 0)),
                        int(dt.get("onoff_cd", 0)),
                        int(dt.get("level_cd", 0)),
                        int(dt.get("link_cat_cd", 0)),
                        int(dt.get("link_type_cd", 0)),
                        link_url,  # 切り捨てたURLを使用
                        dt.get("head_title", ""),
                        dt.get("title", ""),
                        dt.get("detail", ""),
                        dt.get("style_border", ""),
                        dt.get("material_icon", ""),
                        dt.get("search_con", ""),
                        dt.get("update_email", ""),
                    )
                    data_list.append(data)
                except Exception as e:
                    logging.error("%s: データ変換エラー: %s - %s", sys._getframe().f_code.co_name, str(dt), str(e))

            # エラーがあった場合のログ出力
            if error_records:
                logging.warning(
                    "URLが長すぎるレコードが %s 件ありました。切り捨てて処理しました。", str(len(error_records))
                )

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
