from firebase_admin import firestore
import datetime


def get_all_collections_fields():
    """
    Firestore内のすべてのコレクションのフィールドとデータ型を取得する。
    各コレクションの最初のドキュメントを調べてフィールドと型を特定する。

    Returns:
        dict: コレクション名をキー、{フィールド名: 型名} の辞書を値とする辞書。
              例: {'collection1': {'fieldA': 'str', 'fieldB': 'int'}, 'collection2': {'fieldC': 'Timestamp'}}
    """
    try:
        db = firestore.client()
        collections_info = {}

        # すべてのコレクションを取得
        collections = db.collections()

        for collection in collections:
            collection_id = collection.id
            fields_with_types = {}

            # 各コレクションの最初のドキュメントを取得
            docs = collection.limit(1).stream()
            first_doc = next(docs, None)

            if first_doc:
                # ドキュメントが存在すれば、各フィールドの型を取得
                for field_name, value in first_doc.to_dict().items():
                    field_type = type(value).__name__
                    # FirestoreのTimestampはdatetime.datetimeに変換されるため、分かりやすい名前にする
                    if isinstance(value, datetime.datetime):
                        field_type = "Timestamp"
                    fields_with_types[field_name] = field_type

                collections_info[collection_id] = fields_with_types
            else:
                # ドキュメントが存在しない場合は空の辞書をセット
                collections_info[collection_id] = {}

        return collections_info

    except Exception as e:
        print(f"Firestore error while getting all collections fields: {e}")
        return {}
