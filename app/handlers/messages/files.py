from app import bot
from app.helpers.verified import isVerified
from app.helpers.constants import CHANNELS

from firebase_admin import firestore

from datetime import datetime

db = firestore.client()

users_collection = db.collection("users")
files_collection = db.collection("files")
folders_collection = db.collection("folders")

ALLOWED_FILES = ['document', 'photo', 'video', 'audio', 'voice']

@bot.message_handler(content_types=ALLOWED_FILES)
def upload_files(message):
    user = users_collection.document(str(message.chat.id)).get()

    if not isVerified(message):
        return
    
    if message.content_type != "document":
        bot.reply_to(message, "Please send it as documents to save.")
        return

    file_name = message.document.file_name
    file_id = message.document.file_id
    file_path = bot.get_file(file_id).file_path
            
    for channel in CHANNELS:
        bot.forward_message(channel, message.chat.id, message.message_id)

    current_folder_id = user.get("current")
    current_folder = folders_collection.document(current_folder_id)

    file_id = files_collection.add({
        "owner": str(message.chat.id),
        "previous": current_folder_id,
        "name": file_name,
        "created": datetime.now(),
        "file_id": file_id,
    })[1].id

    current_folder.update({"files": firestore.ArrayUnion([file_id])})

    bot.reply_to(message, "File saved successfully!")