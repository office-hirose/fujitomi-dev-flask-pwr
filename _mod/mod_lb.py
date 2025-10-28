from _mod import sql_config
from firebase_admin import firestore


# mysql
def lb_data():
    return sql_config.mz_sql("SELECT * FROM com_lb ORDER BY link_cat_cd, sort;")


def flt_level(login_level_cd):
    temp = fs_lb_data()
    temp = list(filter(lambda x: x["onoff_cd"] == 1, temp))
    temp = list(filter(lambda x: x["level_cd"] <= login_level_cd, temp))
    return temp


# firestore
def fs_lb_data():
    db = firestore.client()
    query = db.collection("com_lb").order_by("sort")
    docs = query.get()

    fs_data = []
    if docs:
        for doc in docs:
            d = doc.to_dict()
            if d is not None:
                d["id"] = doc.id
                fs_data.append(d)

    return fs_data
