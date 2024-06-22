from app import bot
from app.helpers.verified import isVerified
from app.helpers.path import getPath

from firebase_admin import firestore

db = firestore.client()

users_collection = db.collection("users")
files_collection = db.collection("files")
folders_collection = db.collection("folders")

@bot.message_handler(commands=["back"])
def back(message):    
    user_doc = users_collection.document(str(message.chat.id))
    user = isVerified(message)

    if user:
        current_folder_id = user.get("current")

        if current_folder_id == "Home":
            bot.reply_to(message, "You're already at the root folder.")
            return
        
        current_folder = folders_collection.document(current_folder_id).get()

        previous = current_folder.get("previous")

        user_doc.update({"current": previous})

        bot.send_message(message.chat.id, f"In {getPath(previous)}")