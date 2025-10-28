from _mod import sql_config
from firebase_admin import firestore


# mysql
def section_data():
    return sql_config.mz_sql("SELECT * FROM com_lm_section ORDER BY lm_section_cd;")


# firestore
def fs_lm_section_data():
    db = firestore.client()
    query = db.collection("com_lm_section").order_by("lm_section_cd")
    docs = query.get()

    fs_data = []
    if docs:
        for doc in docs:
            d = doc.to_dict()
            if d is not None:
                d["id"] = doc.id
                fs_data.append(d)

    return fs_data
