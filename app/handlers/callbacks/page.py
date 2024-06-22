from app.helpers.verified import isVerified
from app.helpers.retrive import retrive

from firebase_admin import firestore

db = firestore.client()

users_collection = db.collection("users")
files_collection = db.collection("files")

def page(callback, user):
    if user:
        current_folder_id = user.get("current")

        page = int(callback.data.split("_")[-1])

        retrive(callback.message, current_folder_id, page)