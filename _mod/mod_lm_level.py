from _mod import sql_config
from firebase_admin import firestore


# mysql
def level_data():
    return sql_config.mz_sql("SELECT * FROM com_lm_level ORDER BY level_cd;")


# firestore
def fs_lm_level_data():
    db = firestore.client()
    query = db.collection("com_lm_level").order_by("level_cd")
    docs = query.get()

    fs_data = []
    if docs:
        for doc in docs:
            d = doc.to_dict()
            if d is not None:
                d["id"] = doc.id
                fs_data.append(d)

    return fs_data
