from app.helpers.retrive import retrive

from firebase_admin import firestore

db = firestore.client()

users_collection = db.collection("users")
folders_collection = db.collection("folders")

def open_folder(callback):
    current_folder_id = callback.data.split("_")[-1]

    if retrive(callback.message, current_folder_id):
        user = users_collection.document(str(callback.message.chat.id))
        user.update({"current": current_folder_id})