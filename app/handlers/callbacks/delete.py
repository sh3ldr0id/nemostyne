from app import bot
from app.helpers.constants import FILE, FOLDER

from firebase_admin import firestore

db = firestore.client()

files_collection = db.collection("files")
folders_collection = db.collection("folders")

def delete_folder(folder_doc):
    folder = folder_doc.get()

    folders = folder.get("folders")
    files = folder.get("files")

    for fileId in files:
        files_collection.document(fileId).delete()

    for folderId in folders:
        delete_folder(folders_collection.document(folderId))

    folder_doc.delete()

def delete(callback):
    file_or_folder = callback.data.split("_")[1]
    item_id = callback.data.split("_")[2]

    if file_or_folder == FOLDER:
        folder_doc = folders_collection.document(item_id)
        folder = folder_doc.get()

        if not folder.exists or item_id == "Home":
            bot.reply_to(callback.message, "Folder doesn't exist!")
            return

        previous = folder.get("previous")
        folders_collection.document(previous).update({"folders": firestore.ArrayRemove([item_id])}) 

        delete_folder(folder_doc)

        bot.reply_to(callback.message, f"Deleted 📁 {folder.get('name')}")

    elif file_or_folder == FILE:
        file_doc = files_collection.document(item_id)
        file = file_doc.get()

        if not file.exists:
            bot.reply_to(callback.message, "File doesn't exist!")
            return

        previous = file.get("previous")
        folders_collection.document(previous).update({"files": firestore.ArrayRemove([item_id])}) 

        file_doc.delete()

        bot.reply_to(callback.message, f"Deleted 📄 {file.get('name')}")

    bot.delete_message(callback.message.chat.id, callback.message.message_id)