from firebase_admin import firestore


# firestore
def fs_dic():
    try:
        db = firestore.client()
        fs_docs = db.collection("com_config").get()
        if fs_docs and len(fs_docs) > 0:
            return fs_docs[0].to_dict()
        else:
            return {}
    except Exception as e:
        print(f"Firestore error: {e}")
        return {}
