from _mod import sql_config
from firebase_admin import firestore


# mysql
def device_data():
    return sql_config.mz_sql("SELECT * FROM com_device ORDER BY sort;")


# firestore
def fs_device_data():
    db = firestore.client()
    query = db.collection("com_device").order_by("sort")
    docs = query.get()

    fs_data = []
    if docs:
        for doc in docs:
            d = doc.to_dict()
            if d is not None:
                d["id"] = doc.id
                fs_data.append(d)

    return fs_data
