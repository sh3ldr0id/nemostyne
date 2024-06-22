from app import bot
from app.helpers.verified import isVerified
from app.helpers.folder_name import sanitize

from firebase_admin import firestore

from datetime import datetime

db = firestore.client()

users_collection = db.collection("users")
files_collection = db.collection("files")
folders_collection = db.collection("folders")

@bot.message_handler()
def create_folder(message):
    user = isVerified(message)

    if user and user.get("listening") == "folder_name":
        user_doc = users_collection.document(str(message.chat.id))
        current_folder_id = user.get("current")

        name = sanitize(message, current_folder_id)

        if name:
            current_folder = folders_collection.document(current_folder_id)

            folder_id = folders_collection.add({
                "previous": current_folder_id,
                "name": name,
                "files": [],
                "folders": [],
                "created": datetime.now(),
                "by": str(message.chat.id)
            })[1].id

            current_folder.update({"folders": firestore.ArrayUnion([folder_id])})

            user_doc.update({"listening": None})

            bot.reply_to(message, f"Done! Created '{message.text}' in '{current_folder.get().get('name')}'")