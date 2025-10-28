from _mod import sql_config
from firebase_admin import firestore


# mysql
def style_data():
    return sql_config.mz_sql("SELECT * FROM com_style ORDER BY sort;")


# firestore
def fs_style_data():
    db = firestore.client()
    query = db.collection("com_style").order_by("sort")
    docs = query.get()

    fs_data = []
    if docs:
        for doc in docs:
            d = doc.to_dict()
            if d is not None:
                d["id"] = doc.id
                fs_data.append(d)

    return fs_data
