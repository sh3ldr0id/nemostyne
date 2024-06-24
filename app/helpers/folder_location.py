from app.helpers.consts import FOLDERS

from firebase_admin import firestore

db = firestore.client()

folders_collection = db.collection(FOLDERS)

def getLocation(folder_id):
    if folder_id == "Home":
        return [{"id": "Home", "name": "Home"}]
    path = []
    current_folder_id = folder_id

    # Include the details for the current folder
    while True:
        doc_ref = folders_collection.document(current_folder_id)
        doc = doc_ref.get()

        if doc.exists:
            folder_data = doc.to_dict()
            folder_id = doc.id
            folder_name = folder_data.get('name', '')

            path.insert(0, {'id': folder_id, 'name': folder_name})

            current_folder_id = folder_data.get('previous', 'Home')

            if current_folder_id == 'Home':
                break
        else:
            break

    # Include the "Home" folder details explicitly at the start
    path.insert(0, {'id': 'Home', 'name': 'Home'})

    return path