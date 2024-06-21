from app import bot
from app.helpers.folder_name import sanitize

from firebase_admin import firestore

from datetime import datetime

db = firestore.client()

users_collection = db.collection("users")
files_collection = db.collection("files")
folders_collection = db.collection("folders")

@bot.message_handler()
def create_folder(message):
    user_doc = users_collection.document(str(message.chat.id))
    user = user_doc.get()

    listening = user.get("listening")

    name = sanitize(message)

    if listening == "folder_name" and name:
        current_folder_id = user.get("current")
        current_folder = folders_collection.document(current_folder_id)

        folder_id = folders_collection.add({
            "by": str(message.chat.id),
            "previous": current_folder_id,
            "name": name,
            "files": [],
            "folders": [],
            "date": datetime.now()
        })[1].id

        current_folder.update({"folders": firestore.ArrayUnion([folder_id])})

        user_doc.update({"listening": None})

        bot.reply_to(message, f"Done! Created '{message.text}' in '{current_folder.get().get('name')}'")