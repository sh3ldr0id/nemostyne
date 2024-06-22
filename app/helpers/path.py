from firebase_admin import firestore

db = firestore.client()

folders_collection = db.collection('folders')

def getPath(folder_id):
    path = []
    current_folder_id = folder_id

    while current_folder_id != 'Home':
        doc_ref = folders_collection.document(current_folder_id)
        doc = doc_ref.get()

        if doc.exists:
            folder_data = doc.to_dict()
            folder_name = folder_data.get('name', '')

            path.insert(0, folder_name)

            current_folder_id = folder_data.get('previous', 'Home')

        else:
            break

    return '\\' + '\\'.join(path)