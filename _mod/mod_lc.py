from _mod import sql_config
from firebase_admin import firestore


# mysql
def lc_data():
    return sql_config.mz_sql("SELECT * FROM com_lc ORDER BY sort;")


def flt_level(login_level_cd):
    temp = fs_lc_data()
    temp = list(filter(lambda x: x["onoff_cd"] == 1, temp))
    temp = list(filter(lambda x: x["level_cd"] <= login_level_cd, temp))
    return temp


# firestore
def fs_lc_data():
    db = firestore.client()
    query = db.collection("com_lc").order_by("sort")
    docs = query.get()

    fs_data = []
    if docs:
        for doc in docs:
            d = doc.to_dict()
            if d is not None:
                d["id"] = doc.id
                fs_data.append(d)

    return fs_data
