from app import bot
from app.helpers.verified import isVerified
from app.helpers.constants import MAIN_CHANNEL, BACKUP_CHANNEL

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
            
    main_message_id = bot.forward_message(MAIN_CHANNEL, message.chat.id, message.message_id).message_id
    backup_message_id = bot.forward_message(BACKUP_CHANNEL, message.chat.id, message.message_id).message_id

    current_folder_id = user.get("current")
    current_folder = folders_collection.document(current_folder_id)

    file_id = files_collection.add({
        "owner": str(message.chat.id),
        "previous": current_folder_id,
        "name": file_name,
        "date": datetime.now(),
        "main": main_message_id,
        "backup": backup_message_id,
    })[1].id

    current_folder.update({"files": firestore.ArrayUnion([file_id])})

    bot.reply_to(message, "File saved successfully!")