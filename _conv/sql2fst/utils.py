from firebase_admin import firestore


def delete_all_documents(collection_name):
    db = firestore.client()
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()
    for doc in docs:
        doc.reference.delete()
