from _mod import sql_config, mod_lm_level
from firebase_admin import firestore


# mysql
def lm_data():
    return sql_config.mz_sql("SELECT * FROM com_lm ORDER BY sort;")


# firestore
def lm_cd_name(google_account_email):
    temp = fs_lm_data()
    temp = list(filter(lambda x: x["onoff_cd"] == 1, temp))
    temp = list(filter(lambda x: x["lm_email"] == google_account_email, temp))

    if len(temp) == 0:
        login_level_cd = 1  # Guest
        login_level_name = "1.Guest"
    else:
        # level_cd, level_name
        login_level_cd = temp[0]["level_cd"]
        temp_level = mod_lm_level.fs_lm_level_data()
        temp_level = list(filter(lambda x: x["level_cd"] == login_level_cd, temp_level))
        login_level_name = temp_level[0]["level_name"]

    return login_level_cd, login_level_name


# firestore
def fs_lm_data():
    db = firestore.client()
    query = db.collection("com_lm").order_by("sort")
    docs = query.get()

    fs_data = []
    if docs:
        for doc in docs:
            d = doc.to_dict()
            if d is not None:
                d["id"] = doc.id
                fs_data.append(d)

    return fs_data
